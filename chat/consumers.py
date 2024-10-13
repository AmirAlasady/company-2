import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import PrivateRoom, PrivateMessage, Notification
from channels.db import database_sync_to_async
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtain room id from scope
        room_id = self.scope['url_route']['kwargs']['room_id']
        try:
            # Get room from DB
            self.room = await self.get_room(room_id)
            # If user is not in that room, close the connection
            if not await self.is_user_in_room(self.scope['user'], self.room):
                await self.close()
                return
        except PrivateRoom.DoesNotExist:
            await self.close()
            return

        # Construct room group name and add user to it
        self.room_group_name = f"chat_{room_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Send previous messages after accepting the connection
        await self.accept()
        messages = await self.get_messages(room_id)
        for message in messages:
            await self.send_message(message)

        # Add member to Redis
        await self.add_member(self.room_group_name, self.scope['user'].username)

    @database_sync_to_async
    def get_room(self, room_id):
        return PrivateRoom.objects.get(room_id=room_id)

    @database_sync_to_async
    def get_messages(self, room_id):
        return list(PrivateMessage.objects.filter(room__room_id=room_id).order_by('timestamp'))

    @database_sync_to_async
    def save_message(self, room, sender, message):
        return PrivateMessage.objects.create(room=room, sender=sender, message=message)

    @database_sync_to_async
    def is_user_in_room(self, user, room):
        return user in [room.user1, room.user2]

    @database_sync_to_async
    def get_recipient(self, sender, room):
        # Return the other user in the room who is not the sender
        return room.user1 if sender == room.user2 else room.user2

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.remove_member(self.room_group_name, self.scope['user'].username)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = self.scope['user']

        # Save the message to the database
        await self.save_message(self.room, sender, message)

        # Find the recipient
        recipient = await self.get_recipient(sender, self.room)

        # Check if the recipient is active in the chat room
        if not await self.is_user_active_in_room(recipient, self.room_group_name):
            # Create and send a notification if the recipient is not active
            notification = await self.create_notification(sender, recipient, message)
            await self.send_notification_to_recipient(recipient, notification)

        # Broadcast the message to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender
        }))

    async def send_message(self, message):
        # Ensure synchronous access for ORM-related attributes
        message_data = await self.get_message_data(message)
        await self.send(text_data=json.dumps(message_data))

    @database_sync_to_async
    def get_message_data(self, message):
        return {
            'message': message.message,
            'sender': message.sender.username,
            'timestamp': message.timestamp.isoformat()
        }

    async def is_user_active_in_room(self, user, room_group_name):
        members = await self.get_members(room_group_name)
        return user.username in members

    async def send_notification_to_recipient(self, recipient, notification):
        # Send the notification object itself
        await self.channel_layer.group_send(
            f"notifications_{recipient.username}",
            {
                "type": "send_notification",
                "notification": {
                    "description": notification.description,
                    "id": notification.id  # Ensure you're sending the id
                }
            }
        )

    @database_sync_to_async
    def create_notification(self, sender, recipient, message):
        # Logic to create a notification object
        return Notification.objects.create(
            description=f"New message from {sender.username}: {message}",
            sender=sender,
            recipient=recipient,
            timestamp=timezone.now()
        )

    async def add_member(self, room_group_name, username):
        redis_channel_layer = self.channel_layer
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        key = f'channel_members:{room_group_name}'
        redis_client.sadd(key, username)

    async def remove_member(self, room_group_name, username):
        redis_channel_layer = self.channel_layer
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        key = f'channel_members:{room_group_name}'
        redis_client.srem(key, username)

    async def get_members(self, room_group_name):
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        key = f'channel_members:{room_group_name}'
        members = redis_client.smembers(key)
        return [str(member, 'utf-8') for member in members]








class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Each user gets their own notifications group
        self.user = self.scope['user']
        self.notifications_group_name = f"notifications_{self.user.username}"

        # Add this connection to the user's notifications group
        await self.channel_layer.group_add(
            self.notifications_group_name,
            self.channel_name
        )

        await self.accept()
        notifications_list = await self.notifications_obtain(self.user)
        for note in notifications_list:
            await self.note_send(note)


    @database_sync_to_async
    def notifications_obtain(self, user_id):
        return list(Notification.objects.filter(recipient=self.user).order_by('timestamp'))

    
    async def note_send(self, note):
        # Ensure synchronous access for ORM-related attributes
        message_data = await self.get_note_data(note)
        await self.send(text_data=json.dumps(message_data))


    @database_sync_to_async
    def get_note_data(self, note):
        #print('--------------------------------------------------')
        #print(note.id)
        return {
            #'message': note.description,
            # f"New message from {note.sender.username}: {note.description}"
            'notification': note.description,
            'main_id': int(note.id),
            'is_new':False
        }


    async def disconnect(self, close_code):
        # Remove this connection from the user's notifications group
        await self.channel_layer.group_discard(
            self.notifications_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        notification_data = event["notification"]
        notification_description = notification_data["description"]
        notification_id = notification_data["id"]
        #print('--------------------------------------------------')
        #print(notification_id)
        await self.send(text_data=json.dumps({
            "notification": notification_description,
            "main_id": int(notification_id),   
            "is_new":True         
        }))
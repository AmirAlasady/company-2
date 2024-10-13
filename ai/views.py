from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import Chat
from django.utils import timezone
from langchain import HuggingFaceHub
from groq import Groq
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import markdown

def ask_model2(x, context=None):
    key = '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'
    client = Groq(api_key=key)

    if context is None:
        context = []

    context.append({
        "role": "user",
        "content": x,
    })

    chat_completion = client.chat.completions.create(
        messages=context,
        model="llama3-70b-8192",
        temperature=0,
    )

    content = chat_completion.choices[0].message.content
    response = {
        "content": content,
        "role": "assistant",
    }
    
    context.append(response)

    # Convert markdown to HTML
    html_content = markdown.markdown(content)

    return html_content

def kero(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('login')
    
    chats = Chat.objects.filter(user=request.user)
    
    if request.method == 'POST':
        message = request.POST.get('message')

        context = []
        for chat in chats:
            context.append({
                "role": "assistant",
                "content": chat.response,
            })
            print(chat.response)

        # Pass the context here
        response_html = ask_model2(message, context)

        chat = Chat(user=request.user, message=message, response=response_html, created_at=timezone.now())
        chat.save()

        return JsonResponse({'message': message, 'response': response_html})
    
    return render(request, 'kero.html', {'chats': chats})

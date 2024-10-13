import secrets
import string


# main generator class
class Generator:
    def __init__(self):
        self.counter = 0

    def generate_username(self):
        self.counter += 1
        return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(10))+str(self.counter)

    def generate_email(self):
        self.counter += 1
        return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(12)) + str(self.counter) + '@example.com'

    def generate_first_name(self):
        return "First"

    def generate_last_name(self):
        return "Last"

    def generate_password(self):
        return secrets.token_urlsafe(12)

    def generate_re_password(self, password):
        return password

    def generate_data(self):
        username = self.generate_username()
        email = self.generate_email()
        first_name = self.generate_first_name()
        last_name = self.generate_last_name()
        password = self.generate_password()
        re_password = self.generate_re_password(password)

        return {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            're_password': re_password
        }

generator = Generator()
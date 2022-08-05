class User:
    users = []

    def __init__(self, username, email, password_hash):
        self.user = {
            'id': len(User.users) + 1,
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'active': True
        }
        User.add(self.user)

    @staticmethod
    def add(user):
        User.users.append(
            user
        )
        return User.users[-1]

    @staticmethod
    def get(id):
        return next((user for user in User.users if user['id'] == int(id)), None)

    @staticmethod
    def get_by_email(email):
        return next((user for user in User.users if user['email'] == email), None)

    def is_authenticated(self):
        return self.user['authenticated']

    def is_active(self):
        return self.user['active']

    def is_anonymous(self):
        try:
            return True if self.user else False
        except:
            return False

    def get_id(self):
        return str(self.user['id'])

    def __repr__(self):
        return f'<User {self.email}>'
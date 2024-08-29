from .models import User

def load_users(user_id):
    return User.get(user_id)
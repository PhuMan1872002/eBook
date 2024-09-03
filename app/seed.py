from .dao import create_user
from .models import RoleEnum

def seed_admin():
    create_user(
        username="Admin", 
        email="admin@gmail.com", 
        password="123", 
        role=RoleEnum.ADMIN
    )
    print("Successfully created admin user.")
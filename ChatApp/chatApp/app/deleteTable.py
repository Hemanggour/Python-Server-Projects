from models import User, Chat
try:
    print(Chat.objects.filter(id=1))
    print(User.objects.filter(id=1))
except Exception as e:
    print(f"Error in deleteTable: {e}")
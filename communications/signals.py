from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ChatRoom
from accounts.models import User

@receiver(post_save, sender=User)
def create_user_chatroom(sender, instance, created, **kwargs):
    if created:
        ChatRoom.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_chatroom(sender, instance, **kwargs):
    instance.chatroom.save()

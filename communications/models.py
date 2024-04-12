from accounts.models import User
from django.db import models
from django.utils.text import slugify

class PrivateConversation(models.Model):
    participants = models.ManyToManyField(User, related_name='private_conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participant_names = ', '.join([user.username for user in self.participants.all()])
        return f"Private Conversation ({participant_names})"

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

class ChatRoom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username + "'s Chat Room"

class Message(models.Model):
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    private_conversation = models.ForeignKey(PrivateConversation, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('date_added',)
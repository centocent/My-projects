import json
from accounts.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import PrivateConversation, Room, ChatRoom, Message
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_type = self.scope['url_route']['kwargs']['room_type']
        self.room_group_name = f'chat_{self.room_type}_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room_type = data['room_type']
        if room_type == 'room':
            await self.save_room_message(username, self.room_name, message)
        elif room_type == 'chatroom':
            await self.save_chatroom_message(username, self.room_name, message)
        elif room_type == 'private_conversation':
            conversation_id = data['conversation_id']
            await self.save_private_conversation_message(username, conversation_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room_type': room_type,
                'conversation_id': conversation_id if room_type == 'private_conversation' else None,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_room_message(self, username, room_name, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room_name)
        Message.objects.create(user=user, room=room, content=message)

        print("message saved")

    @sync_to_async
    def save_chatroom_message(self, username, chatroom_name, message):
        user = User.objects.get(username=username)
        chatroom = ChatRoom.objects.get(slug=chatroom_name)
        Message.objects.create(user=user, chatroom=chatroom, content=message)

    @sync_to_async
    def save_private_conversation_message(self, username, conversation_id, message):
        user = User.objects.get(username=username)
        conversation = PrivateConversation.objects.get(id=conversation_id)

        if user in conversation.participants.all():
            Message.objects.create(
                user=user,
                private_conversation=conversation,
                content=message
            )
        else:
            raise ValueError("User is not a participant of this conversation.")

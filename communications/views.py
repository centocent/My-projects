from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Room, Message,ChatRoom
from accounts.models import User
from .models import PrivateConversation
from django.http import JsonResponse

# Create your views here.
@login_required (login_url= 'accounts:login')
def home(request):
    currentuser = request.user
    context = {
        'currentuser': currentuser
    }
    return render( request, 'chat/home.html', context)

@login_required
def rooms(request):
    rooms = Room.objects.all()
    chatrooms = ChatRoom.objects.all()
    users = User.objects.all()
    currentuser = request.user
    context = {
        'currentuser': currentuser,
        'rooms': rooms,
        'chatrooms': chatrooms,
        'users': users
    }

    return render(request, 'room/rooms.html', context)

@login_required
def comms_base(request):
    currentuser = request.user
    context = {
        'currentuser': currentuser,
        'rooms':rooms
    }

    return render(request, 'room/comms_base.html', context)

@login_required
def room(request, slug):
    rooms = Room.objects.all()
    currentuser = request.user
    room = Room.objects.get(slug = slug)
    messages = Message.objects.filter(room=room)[0:50]
    context = {
        'room':room,
        'messages': messages, 
        'currentuser': currentuser,
        'rooms': rooms
    }
    return render(request, 'room/room.html', context)

@login_required
def chatroom(request, slug):
    chatrooms = ChatRoom.objects.all()
    currentuser = request.user
    chatroom = ChatRoom.objects.get(slug = slug)
    messages = Message.objects.filter(chatroom=chatroom)[0:50]
    context = {
        'chatroom':chatroom,
        'messages': messages, 
        'currentuser': currentuser,
        'chatrooms': chatrooms
    }
    return render(request, 'room/chatroom.html', context)

def users_list(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'room/users.html', context)
def create_google_meet(request):
    # Generate the Google Meet link (replace this with your actual code to generate a link)
    google_meet_link = 'https://meet.google.com/?authuser=0'

    # Add logic here to add users to the meeting if needed

    return JsonResponse({'google_meet_link': google_meet_link})

@login_required
def private_conversation(request,otheruser, conversation_id):
    conversation = get_object_or_404(PrivateConversation, id=conversation_id)
    users = User.objects.all()
    otheruser = otheruser
    if request.user not in conversation.participants.all():
        return HttpResponseForbidden("You are not authorized to access this conversation.")

    messages = Message.objects.filter(private_conversation=conversation)[0:50]
    context = {
        'conversation': conversation,
        'messages': messages,
        'users': users,
        'otheruser': otheruser,
    }
    return render(request, 'room/private_conversation.html', context)

@login_required
def start_private_conversation(request, username):
    target_user = get_object_or_404(User, username=username)
    current_user = request.user

    # Check if a conversation already exists between the two users
    conversation = PrivateConversation.objects.filter(
        participants=current_user
    ).filter(
        participants=target_user
    ).first()

    if conversation:
        # If a conversation already exists, redirect to the conversation page
        return redirect('communications:private_conversation', otheruser = target_user, conversation_id=conversation.id)
    else:
        # Create a new private conversation
        conversation = PrivateConversation.objects.create()
        conversation.participants.add(current_user, target_user)
        return redirect('communications:private_conversation', otheruser = target_user, conversation_id=conversation.id)
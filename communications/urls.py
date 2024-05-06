from django.urls import path, include
from . import views
from .views import create_google_meet
app_name = 'communications'

urlpatterns  = [
    path('', views.rooms, name='rooms'),
    path('Home/', views.home, name= 'home'),
    path('comms/', views.comms_base, name = 'comms'),
    path('chatroom/<slug:slug>/', views.chatroom, name='chatroom'),
    path('room/<slug:slug>/', views.room, name='room'),
    path('start-private-conversation/<str:username>/', views.start_private_conversation, name='start_private_conversation'),
    path('private-conversation/<str:otheruser>/<int:conversation_id>/', views.private_conversation, name='private_conversation'),
    path('users/', views.users_list, name='users_list'),
     path('create_google_meet/', create_google_meet, name='create_google_meet'),
]
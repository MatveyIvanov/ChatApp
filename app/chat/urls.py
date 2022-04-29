from django.urls import path

from .views import home, chat, chat_room, global_search


urlpatterns = [
    path('', home, name='home'),
    path('chat', chat, name='chat'),
    path('chat/global_search', global_search, name='global_search'),
    path('chat/<str:room_name>/global_search', global_search, name='global_search'),
    path('chat/<str:room_name>', chat_room, name='room'),
]

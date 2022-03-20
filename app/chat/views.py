from http import HTTPStatus
from telnetlib import STATUS
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils import dateformat
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import ChatRoom, Message, ChatUser


@login_required
def home(request):
    return redirect('chat')

@login_required
def chat(request):
    if request.method == 'GET':
        user = request.user
        try:
            rooms = ChatRoom.objects.filter(Q(user1_id=user) | Q(user2_id=user))
            contacts = []
            for room in rooms:
                if room.user1_id == user:
                    contacts.append(room.user2_id)
                else:
                    contacts.append(room.user1_id)
        except ChatRoom.DoesNotExist as e:
            print(e)
        except IntegrityError as e:
            print(e)
        except Exception as e:
            print(e)

        if request.is_ajax():
            return render(request, 'chat/contacts_list.html', {'contacts': contacts})
        return render(request, "chat/chat.html", {'contacts': contacts})
    
    return render(request, "chat/chat.html")

@login_required
def chat_room(request, room_name):
    if request.is_ajax() and request.method == 'GET':
        user = request.user
        companion_id = room_name.split('-')
        if companion_id[0] == user.id:
            companion_id = companion_id[1]
        else:
            companion_id = companion_id[0]

        try:
            chat = ChatRoom.objects.get(Q(user1_id=user, user2_id=companion_id) | Q(user1_id=companion_id, user2_id=user))
            companion = ChatUser.objects.get(id=companion_id)
            messages = Message.objects.filter(chat_id=chat)
            for message in messages:
                message.send_time = dateformat.format(message.send_time, 'Y-m-d H:i')

            messages_num = messages.count()

            return render(request, 'chat/chat_box.html', {'messages': messages, 'companion': companion, 'messages_num': messages_num})
        except ChatRoom.DoesNotExist as e:
            return redirect('chat')
        except IntegrityError as e:
            return redirect('chat')
        except Exception as e:
            return redirect('chat')

    if request.method == 'GET':
        user = request.user
        companion_id = room_name.split('-')
        if companion_id[0] == user.id:
            companion_id = companion_id[1]
        else:
            companion_id = companion_id[0]

        try:
            chat = ChatRoom.objects.get(Q(user1_id=user, user2_id=companion_id) | Q(user1_id=companion_id, user2_id=user))
            print(f"CHAT: {chat}")
            messages = Message.objects.filter(chat_id=chat)
            for message in messages:
                message.send_time = dateformat.format(message.send_time, 'Y-m-d H:i')
            rooms = ChatRoom.objects.filter(Q(user1_id=user) | Q(user2_id=user))
            contacts = []
            for room in rooms:
                if room.user1_id == user:
                    contacts.append(room.user2_id)
                else:
                    contacts.append(room.user1_id)

            messages_num = messages.count()

            return render(request, 'chat/chat.html', {
                'room_name': room_name,
                'messages': messages,
                'contacts': contacts,
                'companion': companion_id,
                'messages_num': messages_num
            })
        except ChatRoom.DoesNotExist as e:
            return redirect('chat')
        except IntegrityError as e:
            return redirect('chat')
        except Exception as e:
            return redirect('chat')
    
    return render(request, 'chat/chat.html', {'room_name': room_name})


def global_search(request, room_name=None):
    if request.method == "GET" and request.is_ajax():
        substr = request.GET.get("search_substring").lower()
        try:
            users = ChatUser.objects.filter(Q(id__icontains=substr) & ~Q(id=request.user.id))
            return render(request, 'chat/contacts_list.html', {'contacts': users})
        except ChatUser.DoesNotExist as e:
            return redirect('chat')
        except IntegrityError as e:
            return redirect('chat')
        except Exception as e:
            return redirect('chat')

    return redirect('chat')


def handler404(request, exception, template_name='404.html'):
    return render(request, template_name, status=404)
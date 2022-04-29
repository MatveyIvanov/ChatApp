import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import IntegrityError
from django.db.models import Q
from django.utils import dateformat

from .models import Message, ChatRoom
from accounts.models import ChatUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.new_chat = False
        self.new_chat_has_messages = True

        splt = self.room_name.split('-')
        if len(splt) == 3:
            self.new_chat = True
            temp = sorted(splt[:-1])
        else:
            temp = sorted(splt)


        if temp[0] == str(self.user_id):
            self.companion_id = temp[1]
        else:
            self.companion_id = temp[0]
        self.companion_id = self.companion_id.replace('_', ' ')

        self.room_group_name = f'chat_{temp[0] + temp[1]}'

        self.user = await self.get_user()
        self.companion = await self.get_companion()
        if self.new_chat:
            self.chat = await self.create_chat()
            self.new_chat_has_messages = False
            self.new_chat = False
        else:
            self.chat = await self.get_chat()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def create_chat(self):
        try:
            companion_obj = ChatUser.objects.get(id=self.companion_id)
            chat = ChatRoom(user1_id=self.user, user2_id=companion_obj)
            chat.save()
            return chat
        except ValueError as e:
            print(e)
        except IntegrityError as e:
            print(e)
        except Exception as e:
            print(e)

    @database_sync_to_async
    def delete_chat(self):
        try:
            self.chat.delete()
        except IntegrityError as e:
            print(e)
        except Exception as e:
            print(e)

    @database_sync_to_async
    def get_chat(self):
        try:
            return ChatRoom.objects.get(Q(user1_id=self.user_id, user2_id=self.companion_id) | Q(user1_id=self.companion_id, user2_id=self.user_id))
        except ChatRoom.DoesNotExist as e:
            print(e)
        except IntegrityError as e:
            print(e)
        except Exception as e:
            print(e)

    @database_sync_to_async
    def get_user(self):
        try:
            return ChatUser.objects.get(id=self.user_id)
        except ChatUser.DoesNotExist as e:
            print(e)
        except IntegrityError as e:
            print(e)
        except Exception as e:
            print(e)

    @database_sync_to_async
    def get_companion(self):
        try:
            return ChatUser.objects.get(id=self.companion_id)
        except ChatUser.DoesNotExist as e:
            print(e)
        except IntegrityError as e:
            print(e)
        except Exception as e:
            print(e)

    async def disconnect(self, close_code):
        if not self.new_chat_has_messages:
            await self.delete_chat()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        self.new_chat_has_messages = True

        message_object = await self.save_message(message, sender)
        time = dateformat.format(message_object.send_time, 'm-d H:i')

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'time': time,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        time = event['time']

        await self.send(text_data=json.dumps({
            'message': message,
            'time': time,
            'sender': sender
        }))

    @database_sync_to_async
    def save_message(self, msg, sender):
        try:
            user = self.user if self.user.id == sender else self.companion
            message = Message(chat_id=self.chat, user_id=user, message=msg)
            message.save()
            self.chat.last_message = timezone.now()
            last_msg_sender = self.chat.user2_id.id if self.chat.last_message_sender else self.chat.user1_id.id
            if last_msg_sender == sender:
                self.chat.unread += 1
            else:
                self.chat.unread = 1
                self.chat.last_message_sender = True if self.chat.user2_id.id == sender else False
            self.chat.save()
            return message
        except Message.DoesNotExist as e:
            print(e)
        except IntegrityError as e:
            print(e)
        except Exception as e:
            print(e)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user']
        
        self.notification_group_name = f'notifications_{self.user_id}'

        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = text_data_json['sender']
        reciever = text_data_json['reciever']

        await self.channel_layer.group_send(
            f'notifications_{reciever}',
            {
                'type': 'new.message',
                'sender': sender,
                'reciever': reciever
            }
        )

    async def new_message(self, event):
        sender = event['sender']
        reciever = event['reciever']

        await self.send(text_data=json.dumps({
            'sender': sender,
            'reciever': reciever
        }))

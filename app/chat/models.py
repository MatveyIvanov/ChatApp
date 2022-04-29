from django.utils import timezone
from django.db import models

from accounts.models import ChatUser


class ChatRoom(models.Model):
    user1_id = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='%(class)s_user1')
    user2_id = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='%(class)s_user2')

    last_message = models.DateTimeField(default=timezone.now())
    unread = models.IntegerField(default=0)
    last_message_sender = models.BooleanField(null=True)

    def __str__(self) -> str:
        return f'{self.user1_id}, {self.user2_id}'

    class Meta:
        ordering = ['-last_message']


class Message(models.Model):
    chat_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user_id = models.ForeignKey(ChatUser, on_delete=models.CASCADE)

    message = models.TextField(null=False)
    send_time = models.DateTimeField(default=timezone.now)

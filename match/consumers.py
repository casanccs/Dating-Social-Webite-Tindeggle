from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *


class DMConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'dm_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.user = self.scope['user']
        self.profile = Profile.objects.get(user__exact=self.user)
        try:
            self.chatRoom = ChatRoom.objects.get(room_name=self.room_name)
        except:
            self.chatRoom = ChatRoom(room_name=self.room_name)
            self.chatRoom.save()
        self.accept()

    def receive(self, text_data=None):
        print(text_data)
        
        msg = Message(content=text_data, profile=self.profile, chat=self.chatRoom)
        msg.save()
        print(msg.time)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': f"[{msg.time}] ({self.profile.user.username}): {text_data} ",
            }
        )

    def send_message(self, event):
        message = event['message']
        self.send(text_data=message)

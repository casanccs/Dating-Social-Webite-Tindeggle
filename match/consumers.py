from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
import json


class DMConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print("In connect with: ", self.room_name)
        self.room_group_name = f'dm_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name )
        self.user = self.scope['user']
        self.profile = Profile.objects.get(user__exact=self.user)
        try:
            self.chatRoom = ChatRoom.objects.get(room_name=self.room_name)
        except:
            self.chatRoom = ChatRoom(room_name=self.room_name)
            self.chatRoom.save()
        self.accept()

    def receive(self, text_data):
        receiveDict = json.loads(text_data)
        action = receiveDict['action']
        
        if action == 'new-message':
            msg = Message(content=receiveDict['message']['text-content'], profile=self.profile, chatRoom=self.chatRoom)
            msg.save()
            message = f'[{msg.time}] ({msg.profile.user.username}): {msg.content}'
            receiveDict['message']['text-content'] = message
            print(msg.time)
            #receiver_channel_name = receiveDict['message']['receiver_channel_name']
            #receiveDict['message']['receiver_channel_name'] = self.channel_name
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send_message',
                    'receive_dict': receiveDict
                }
            )
            #This time, it sends the JSON BUT with ['message']['text-content']
            return
            
        if (action == 'new-offer') or (action == 'new-answer'):
            receiver_channel_name = receiveDict['message']['receiver_channel_name']
            receiveDict['message']['receiver_channel_name'] = self.channel_name

            async_to_sync(self.channel_layer.send)(
                receiver_channel_name,
                {
                    'type': 'send_message',
                    'receive_dict': receiveDict
                }
            )
            return
        receiveDict['message']['receiver_channel_name'] = self.channel_name
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_message',
                'receive_dict': receiveDict
            }
        )

    def send_message(self, event):
        receiveDict = event['receive_dict']
        self.send(text_data=json.dumps(receiveDict))
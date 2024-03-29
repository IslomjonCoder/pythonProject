# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        print('hello', self.room_group_name)
        # add try catch hereawait self.channel_layer.group_add(

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print('Hello2')

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connection established'
        }))

    async def disconnect(self, close_code):
        username = self.scope.get('user')
        if username:
            # Log the disconnection event
            print(f"User {username} disconnected.")
        else:
            # Log the disconnection event for anonymous users
            print("Anonymous user disconnected.")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

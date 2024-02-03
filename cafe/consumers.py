import logging
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import asyncio

logger = logging.getLogger(__name__)
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('hello')
        logger.info('WebSocket connected')
        self.room_name = 'test'  # self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = "chat_test"

        # Add the user to the room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )

        self.accept()
        self.send(text_data=json.dumps(
            {
                "type": 'connection established',
                "message": "You are now connected!"
            }
        ))

    def receive(self, text_data=None, bytes_data=None):
        print('receive')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(
            {
                "type": 'chat',
                "message": event['message'],
            }
        ))

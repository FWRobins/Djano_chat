# chat/consumers.py
import json
from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # join room group (sync)
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        #
        # self.accept()

        # join room group (async)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # leave room group (sync)
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name,
        #     self.channel_name
        # )

        # leave room group (async)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # send message to room group (sync)
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type':'chat_message',
        #         'message': message
        #     }
        # )


        # send message to room group (async)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message
            }
        )



        # setup test code
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

    # receive message from room group
    async def chat_message(self, event):
        message =event['message']

        # send message to WebSocket (sync)
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

        # send message to WebSocket (async)
        await self.send(text_data=json.dumps({
            'message': message
        }))

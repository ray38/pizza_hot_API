# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import socket
import time
import asyncio
from asgiref.sync import sync_to_async

class StoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.group_name = 'store'
        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    def communicateWithSocket(self, message):
        print("async start")
        HOST, PORT = "localhost", 9999
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(bytes(message + "\n", "utf-8"))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")
        print("Sent:     {}".format(message))
        print("Received: {}".format(received))
        return received

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json
        print(message);

        self.communicateWithSocket(text_data)

        if message["type"] == "open":


            # Send message to room group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'news_message',
                    'message': "new store open"
                }
            )

    # Receive message from room group
    async def news_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
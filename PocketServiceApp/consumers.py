import json
from channels.generic.websocket import AsyncWebsocketConsumer



class ClientStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'client',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'client',
            self.channel_name
        )

    async def update_task_status(self, event):
        data = event['data']
        print(f'BOT EVENT {event}')
        await self.send(text_data=json.dumps(data))
import json
from channels.generic.websocket import AsyncWebsocketConsumer



class ClientStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'client',
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'connected'}))
        await self.close()
    async def receive(self, event):
        data = event['data']
        print(f'BOT EVENT {event}')
        await self.send(text_data=json.dumps(data))
        await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'client',
            self.channel_name
        )
        await self.close()

    # async def update_task_status(self, event):
    #     data = event['data']
    #     print(f'BOT EVENT {event}')
    #     await self.send(text_data=json.dumps(data))
    #     await self.close()
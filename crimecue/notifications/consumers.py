import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CrimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("crimes", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("crimes", self.channel_name)
    
    async def send_crime(self, event):
        await self.send(text_data=json.dumps(event["crime"]))
from alicebot import Plugin
import requests
import os

KPORT = int(os.environ.get('K_PORT')) or 8000

class BanTracker(Plugin):
    async def handle(self):
        text = requests.get(f'http://host.docker.internal:{KPORT}/wdr').json()['wdr']
        await self.event.reply(text)
    
    async def rule(self) -> bool:
        return (
            self.event.adapter.name == "cqhttp"
            and self.event.type == "message"
            and str(self.event.message).lower() == "wds"
        )
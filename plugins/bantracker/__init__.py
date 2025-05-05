from alicebot import Plugin
import requests

class BanTracker(Plugin):
    async def handle(self):
        text = requests.get('http://127.0.0.1:8000/wdr').json()['wdr']
        await self.event.reply(text)
    
    async def rule(self) -> bool:
        return (
            self.event.adapter.name == "cqhttp"
            and self.event.type == "message"
            and str(self.event.message).lower() == "wds"
        )
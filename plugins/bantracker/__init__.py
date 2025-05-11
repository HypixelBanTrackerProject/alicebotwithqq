from alicebot import Plugin
from alicebot.adapter.cqhttp.event import MessageEvent, GroupMessageEvent, PrivateMessageEvent
import requests
import os
import time

KPORT = int(os.environ.get('K_PORT')) or 8000

class BanTracker(Plugin):
    def __init_state__(self):
        return {
            #uin / timelatest
        }

    async def handle(self):
        groupid = None
        verify = False
        senderid = self.event.sender.user_id
        if isinstance(self.event, GroupMessageEvent):
            groupid = self.event.group_id

        if senderid in self.bot.global_state['admin_list']:
            verify = True
        if (groupid is not None) and (not verify):
            if (time.time() - self.state.get(groupid,0)) > 60:
                self.state[groupid] = time.time()
            else:
                return

        text = requests.get(f'http://host.docker.internal:{KPORT}/wdr').json()['wdr']
        await self.event.reply(text)
    
    async def rule(self) -> bool:
        return (
            self.event.adapter.name == "cqhttp"
            and self.event.type == "message"
            and str(self.event.message).lower() == "wds"
        )
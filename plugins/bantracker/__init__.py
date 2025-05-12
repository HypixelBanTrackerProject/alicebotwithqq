from alicebot import Plugin
from alicebot.adapter.cqhttp.event import MessageEvent, GroupMessageEvent, PrivateMessageEvent
import requests
import os
import time

KPORT = int(os.environ.get('K_PORT')) or 8000

TIME_RATE = 60

class BanTracker(Plugin):
    def __init_state__(self):
        return {
            #uin / timelatest
        }
        # return {
        #     "group":{},
        #     "uin":{},
        # }

    async def handle(self):
        groupid = None
        verify = False
        senderid = self.event.sender.user_id

        extensionMessage = ''

        if isinstance(self.event, GroupMessageEvent):
            groupid = self.event.group_id

        if senderid in self.bot.global_state['admin_list']:
            verify = True
        if (groupid is not None) and (groupid in self.bot.global_state['white_group_list']):
            verify = True
        if (groupid is not None) and (not verify):
            if (time.time() - self.state.get(groupid,0)) > TIME_RATE:
                self.state[groupid] = time.time()
                extensionMessage += f'\nPay attention! This group has been enabled rate limit /{TIME_RATE}s'
            else:
                return

        text = requests.get(f'http://host.docker.internal:{KPORT}/wdr').json()['wdr'] + extensionMessage
        await self.event.reply(text)
    
    async def rule(self) -> bool:
        return (
            self.event.adapter.name == "cqhttp"
            and self.event.type == "message"
            and str(self.event.message).lower() == "wds"
        )
from alicebot import Bot
import shutil
import os
import json

if not os.path.exists('/app/c/config/config.json'):
    shutil.copy('/app/c/config.json','/app/c/config/config.json')

ConfigJson = {}
AdminList = []
with open('/app/c/config/config.json', 'r', encoding='utf-8') as f:
    ConfigJson = json.loads(f.read())
AdminList = ConfigJson['admin'] or []

WhiteGroupList = ConfigJson['groups'] or []

bot = Bot()
bot.global_state['admin_list'] = AdminList
bot.global_state['white_group_list'] = WhiteGroupList

if __name__ == '__main__':
    bot.run()
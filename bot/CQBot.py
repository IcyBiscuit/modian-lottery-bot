from aiocqhttp import CQHttp

from configs.BotConfig import config

bot = CQHttp(api_root=config['url'],
             access_token=config['access_token'])


async def send_msg(msg: str, group: str = config['qqGroup']):
    if config['enable']:
        await bot.send_group_msg(group_id=group, message=msg)

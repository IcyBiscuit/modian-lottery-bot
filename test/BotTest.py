from setup import setup
setup()
from bot.CQBot import send_msg
import asyncio

loop= asyncio.get_event_loop()

loop.run_until_complete(send_msg("test\n[CQ:image,file=c:\\Users\\Administrator\\Desktop\\cardpoolR\\R4.png]"))

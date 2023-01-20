# Telegram file copying using pyrogram
# pip3 install pyrogram
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio


FROM = -10012345678
TO = -10012345678
PYRO_SESSION = ""
API_ID = 1234
API_HASH = "abcd1234edfghijkl"

user = Client(
    "Test",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=PYRO_SESSION,
)

@user.on_message(filters.command('copy') & filters.me)
async def copy_files(c, m):
    async for msg in c.iter_history(FROM):
        try:
            if msg.document:  # specify the message type (document|video|photo|...)
                await msg.copy(TO)
        except FloodWait as t:
            await asyncio.sleep(t.x)
  
user.run()

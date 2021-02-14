"""
A commandline tool for copying telegram files using pyrogram
pip3 install pyrogram
after logging in use /copy in any chat to initialise the process
"""
import sys
import asyncio
import argparse
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

parser = argparse.ArgumentParser(description='CLI tool for copying files bw two channels')
parser.add_argument(
    "-i", "--api-id", help="API id from my.telegram.org",
    required=True, type=int
)
parser.add_argument(
    "-a", "--api-hash", help="API hash from my.telegram.org",
    required=True
)
parser.add_argument(
    "-s", "--session", help="Pyrogram session string (optional)",
    default="anything"
)
parser.add_argument(
    "-f", "--fromc", help="from chat id",
    required=True, type=int
)
parser.add_argument(
    "-t", "--toc", help="target chat id",
    required=True, type=int
)
parser.add_argument(
    "-l", "--filter", help="type of file which you want to copy",
    default="document"
)
args = parser.parse_args()

user = Client(
    args.session,
    api_id=args.api_id,
    api_hash=args.api_hash
)


@user.on_message(filters.command('copy') & filters.me)
async def copy_files(client, message):
    await message.edit(f"Trying to copy files from __{args.fromc}__ to __{args.toc}__")
    await asyncio.sleep(2)
    count=0
    async for msg in client.search_messages(args.fromc, filter=args.filter):
        try:
            await msg.copy(args.toc)
        except FloodWait as wait:
            await asyncio.sleep(wait.x)
        except Exception as e:
            sys.exit(e)
        if count % 10 == 0:
            await message.edit(f"copied {count} files")
        count += 1
    await message.edit(f"Done, {count} file(s) copied")

if __name__ == "__main":
    user.run()

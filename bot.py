import asyncio
import aioconsole
import discord
import math
from subprocess import call

TOKEN = "REDACTED_TOKEN"
channel_id = REDACTED_ID
client = discord.Client()

user1_id = '<@REDACTED_ID>'
user2_id = '<@REDACTED_ID>'


async def shutdown(op_code):
    call("sudo shutdown -h now", shell=True)


async def message_decode(op_code):
    message = mention_map[int(op_code[0]) % 3] + ", " + message_map[math.ceil(int(op_code[0]) / 3)]
    if len(op_code) > 1:
        message += " binnen " + op_code[1:] + " minuten"
    await client.get_channel(channel_id).send(message)

op_code_map = {"0": shutdown}
mention_map = ["%s" % user2_id, "@everyone", "%s" % user1_id]
message_map = ["", "het eten is klaar", "we vertrekken", "kom eens naar beneden"]


async def send_message():
    await client.wait_until_ready()
    while not client.is_closed():
        op_code = await aioconsole.ainput()
        op_code = op_code.replace('+', '').replace('-', '').replace('*', '').replace('/', '')
        await op_code_map.get(op_code, message_decode)(op_code)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('----')
    # await client.get_channel(channel_id).send("Test", tts=True)

loop = asyncio.get_event_loop()
tasks = [client.start(TOKEN), send_message()]
loop.run_until_complete(asyncio.gather(*tasks))
loop.close()

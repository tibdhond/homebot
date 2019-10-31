import asyncio
import aioconsole
import discord
import math
from subprocess import call
import sys
from datetime import datetime as d

TOKEN = "REDACTED_TOKEN"
channel_id = REDACTED_ID
client = discord.Client()

user1_id = '<@REDACTED_ID>'
user2_id = '<@REDACTED_ID>'


async def shutdown(_):
    call("sudo shutdown -h now", shell=True)


async def reboot(_):
    call("sudo reboot", shell=True)


async def message_decode(op_code):
    op_code = op_code.replace('+', '').replace('-', '').replace('*', '').replace('/', '')
    message = mention_map[int(op_code[0]) % 3] + ", " + message_map[math.ceil(int(op_code[0]) / 3)]
    if len(op_code) > 1:
        message += " binnen " + op_code[1:] + " minuten"
    await client.get_channel(channel_id).send(message)

op_code_map = {"0": shutdown, "0+": reboot}
mention_map = ["%s" % user2_id, "@everyone", "%s" % user1_id]
message_map = ["", "het eten is klaar", "we vertrekken", "kom eens naar beneden"]


async def send_message():
    op_code = ''
    await client.wait_until_ready()
    call("numlockx on", shell=True)
    while not client.is_closed():
        try:
            op_code = await aioconsole.ainput()
            await op_code_map.get(op_code, message_decode)(op_code)
        except:
            f = open("error.log", 'a+')
            f.write("%s\n" % d.now())
            f.write("%s\n" % sys.exc_info()[0])
            f.write("%s\n\n" % ("Op_code: %s" % op_code if op_code != "" else "Op_code is empty"))
            f.close()
        finally:
            await reboot("")


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

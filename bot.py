import asyncio
import aioconsole
import discord
import math
from subprocess import call
import sys
from datetime import datetime as d
from time import sleep

TOKEN = "REDACTED_TOKEN"
# channel_id = REDACTED_ID   # General
channel_id = REDACTED_ID     # Testing
client = discord.Client()

user1_id = '<@REDACTED_ID>'
user2_id = '<@REDACTED_ID>'
numlock = 0


def blink_once():
    call("numlockx on", shell=True)
    sleep(0.1)
    call("numlockx off", shell=True)


async def shutdown(_):
    call("sudo shutdown -h now", shell=True)


async def reboot(_):
    call("sudo reboot", shell=True)


async def reset_blink(_):
    global numlock
    numlock = 0
    call("numlockx on", shell=True)


async def message_decode(op_code):
    op_code = op_code.replace('+', '').replace('-', '').replace('*', '').replace('/', '')
    message = mention_map[int(op_code[0]) % 3] + ", " + message_map[math.ceil(int(op_code[0]) / 3)]
    if len(op_code) > 1:
        message += " binnen " + op_code[1:] + " minuten"
    await client.get_channel(channel_id).send(message)
    call("numlockx off", shell=True)

op_code_map = {"0": shutdown, "0+": reboot}
mention_map = ["@everyone", "%s" % user1_id, "%s" % user2_id]
message_map = ["", "het eten is klaar", "we vertrekken", "kom eens naar beneden"]


@client.event
async def on_message(d_message):
    global numlock
    if d_message.author.id == user1_id:
        numlock += 1
    elif d_message.author.id == user2_id:
        numlock += 2


async def send_message():
    op_code = ''
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            op_code = await aioconsole.ainput()
            op_code = op_code[max(0, op_code.rfind('.')+1):]
            print(op_code)
            await op_code_map.get(op_code, message_decode)(op_code)
        except:
            f = open("error.log", 'a+')
            f.write("%s\n" % d.now())
            f.write("%s\n" % sys.exc_info()[0])
            f.write("%s\n\n" % ("Op_code: %s" % op_code if op_code != "" else "Op_code is empty"))
            f.close()
            await reboot("")


async def numlock_feedback():
    await client.wait_until_ready()
    while not client.is_closed():
        i = 0
        while i < numlock:
            blink_once()
            i += 1
        await asyncio.sleep(0.1)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('----')
    call("numlockx on", shell=True)

loop = asyncio.get_event_loop()
tasks = [client.start(TOKEN), send_message(), numlock_feedback()]
loop.run_until_complete(asyncio.gather(*tasks))
loop.close()

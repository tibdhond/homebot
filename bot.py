import asyncio
import aioconsole
import discord
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
    print("Rebooting")
    # call("sudo reboot", shell=True)


async def message_construct(op_code):
    message = message_map[int(op_code[0])]
    if len(op_code) > 1:
        message += " binnen " + op_code[1:] + " minuten"
    await client.get_channel(channel_id).send(message)

op_code_map = {"0": shutdown, "0+": reboot}
message_map = ["", "@everyone, het eten is klaar", "@everyone, we vertrekken", "",
               "@everyone, komen jullie eens naar beneden?",
               "%s, kom eens naar beneden" % user1_id, "%s, kom eens naar beneden" % user2_id]


async def send_message():
    op_code = ''
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            op_code = await aioconsole.ainput()
            op_code = op_code.replace('+', '').replace('-', '').replace('*', '').replace('/', '')
            await op_code_map.get(op_code, message_construct)(op_code)
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

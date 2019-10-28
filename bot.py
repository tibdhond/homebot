import asyncio
import aioconsole
import discord
from subprocess import call

TOKEN = "REDACTED_TOKEN"
channel_id = REDACTED_ID
client = discord.Client()

user1_id = '<@REDACTED_ID>'
user2_id = '<@REDACTED_ID>'


async def shutdown(op_code):
    call("sudo shutdown -h now", shell=True)


async def message(op_code):
    message = message_map[int(op_code[0])]
    if len(op_code) > 1:
        message += " binnen " + op_code[1:] + " minuten"
    await client.get_channel(channel_id).send(message)

op_code_map = {"0": shutdown}
message_map = ["", "@everyone, het eten is klaar", "@everyone, we vertrekken", "",
               "@everyone, komen jullie eens naar beneden?",
               "%s, kom eens naar beneden" % user1_id, "%s, kom eens naar beneden" % user2_id]


async def send_message():
    await client.wait_until_ready()
    while not client.is_closed():
        op_code = await aioconsole.ainput()
        op_code = op_code.replace('+', '').replace('-', '').replace('*', '').replace('/', '')
        await op_code_map.get(op_code, message)(op_code)


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

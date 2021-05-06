import discord
import os
import requests
import json
import random
import xml.etree.ElementTree as ET
from keep_alive import keep_alive
from pathlib import Path
from dotenv import load_dotenv
import asyncio

env_path=Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person / bot!"
]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def idezet():
    r = requests.get(
        'https://api.citatum.hu/idezet.php?f=apitest&j=957811486d3132fe353d18e116cb17c6&kat=%C9let&rendez=veletlen')
    root = ET.fromstring(r.content)
    idezet = root[0][0].text + " - " + root[0][1].text
    return (idezet)

def idezetSP():

    r = requests.get(
        'https://api.citatum.hu/idezet.php?f=apitest&j=957811486d3132fe353d18e116cb17c6&szerzo=szabo+peter&rendez=veletlen')
    root = ET.fromstring(r.content)
    idezet = root[0][0].text + " - A Mester Maga"
    return (idezet)

def idezetteszt(kat):
    r = requests.get(
        'https://api.citatum.hu/idezet.php?f=apitest&j=957811486d3132fe353d18e116cb17c6&kat={}&rendez=veletlen'
            .format(kat))
    root = ET.fromstring(r.content)
    idezet = root[0][0].text + " - " + root[0][1].text
    return (idezet)

@client.event
async def on_ready():
    #guild = client.guilds[0]
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(int(os.environ['chid']))
    quoteHU = idezet()
    quoteEN = get_quote()
    #await random.choice(guild.text_channels).send(quoteHU)
    #await random.choice(guild.text_channels).send(quoteEN)
    while True:
      quoteHU = idezet()
      quoteEN=get_quote()
      await asyncio.sleep(86400)
      await channel.send(quoteHU)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$inspiráció'):
        quote = idezet()
        await message.channel.send(quote)

    if msg.startswith('$insp sp'):
        quote = idezetSP()
        await message.channel.send(quote)

    if msg.startswith('$insp bolcs'):
        quote = idezetteszt('B%F6lcsess%E9g')
        await message.channel.send(quote)

    if msg.startswith('$insp moti'):
        quote = idezetteszt('Motiv%E1ci%F3')
        await message.channel.send(quote)

    if msg.startswith('$insp en'):
        quote = get_quote()
        await message.channel.send(quote)

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))

# @tasks.loop(seconds=30)
# async def orankenti():
#     channel = client.get_channel(chid)
#     quote = idezet()
#     await channel.send(quote)



keep_alive()
client.run(os.environ['token'])
#orankenti.start()

# scheduler = BlockingScheduler()
# scheduler.add_job(hourlyinsp, 'interval', mins=1)
# scheduler.start()

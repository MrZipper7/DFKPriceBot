# main.py

import os, sys, logging
from dotenv import load_dotenv
import discord
from discord.ext import tasks
import asyncio, aiohttp

load_dotenv()

log_format = '%(asctime)s|%(name)s|%(levelname)s: %(message)s'
logger = logging.getLogger("DFKPriceBot")
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout)

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def fetch(client, params):
  url = f"https://api.dexscreener.io/latest/dex/pairs/{params['chainId']}/{params['pairAddress']}"
  async with client.get(url) as resp:
    return await resp.json()

async def getPrices(params):
  async with aiohttp.ClientSession() as client:
    r = await fetch(client, params)
    return r

async def getCRYSTAL():
    chainId = "avalanchedfk"
    pairAddress = "0x48658e69d741024b4686c8f7b236d3f1d291f386"
    params = {'chainId': chainId, 'pairAddress': pairAddress}
    r = await getPrices(params)
    return r

async def getJEWEL():
    chainId = "avalanchedfk"
    pairAddress = "0xCF329b34049033dE26e4449aeBCb41f1992724D3"
    params = {'chainId': chainId, 'pairAddress': pairAddress}
    r = await getPrices(params)
    return r

async def getJADE():
    chainId = "klaytn"
    pairAddress = "0x85DB3CC4BCDB8bffA073A3307D48Ed97C78Af0AE"
    params = {'chainId': chainId, 'pairAddress': pairAddress}
    r = await getPrices(params)
    return r


@client.event
async def on_ready():
    logger.info(f"{client.user} Online")
    priceInfo.start()

@tasks.loop(seconds=12)
async def priceInfo():
    # JEWEL Price
    try:
        JEWEL = await getJEWEL()
        jewelPrice = float(JEWEL['pair']['priceUsd'])
    except:
        jewelPrice = 0

    activity_string = f"JEWEL at ${round(jewelPrice, 3)}"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))

    await asyncio.sleep(4)

    # CRYSTAL Price
    try:
        CRYSTAL = await getCRYSTAL()
        crystalPrice = float(CRYSTAL['pair']['priceUsd'])
    except:
        crystalPrice = 0

    activity_string = f"CRYSTAL at ${round(crystalPrice, 3)}"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))

    await asyncio.sleep(4)

    # JADE Price
    try:
        JADE = await getJADE()
        jadePrice = float(JADE['pair']['priceUsd'])
    except:
        jadePrice = 0

    activity_string = f"JADE at ${round(jadePrice, 3)}"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))

client.run(os.getenv("TOKEN"))

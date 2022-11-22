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



@client.event
async def on_ready():
    logger.info(f"{client.user} Online")
    priceInfo.start()

@tasks.loop(seconds=20)
async def priceInfo():
    JEWEL = await getJEWEL()
    CRYSTAL = await getCRYSTAL()
    jewelPrice = float(JEWEL['pair']['priceNative'])
    crystalPrice = float(JEWEL['pair']['priceNative']) * float(CRYSTAL['pair']['priceNative'])

    # JEWEL Price
    activity_string = f"JEWEL at ${round(jewelPrice, 2)}"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))

    await asyncio.sleep(10)

    # CRYSTAL Price
    activity_string = f"CRYSTAL at ${round(crystalPrice, 2)}"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))

client.run(os.getenv("TOKEN"))

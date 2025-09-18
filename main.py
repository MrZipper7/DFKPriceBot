# main.py

import os
import sys
import logging
import asyncio
import aiohttp
from dotenv import load_dotenv
import discord
from discord.ext import tasks

load_dotenv()

log_format = '%(asctime)s|%(name)s|%(levelname)s: %(message)s'
logger = logging.getLogger("DFKPriceBot")
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout)

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def fetch_dexscreener(client, params):
    url = f"https://api.dexscreener.io/latest/dex/pairs/{params['chainId']}/{params['pairAddress']}"
    async with client.get(url) as resp:
        return await resp.json()


async def fetch_cmc(client, params):
    url = f"https://api.coinmarketcap.com/dexer/v3/dexer/pair-info?dexer-platform-name={params['chainId']}&address={params['pairAddress']}"
    async with client.get(url) as resp:
        return await resp.json()


async def fetch_gecko(client, params):
    url = f"https://app.geckoterminal.com/api/p1/{params['chainId']}/pools/{params['pairAddress']}"
    async with client.get(url) as resp:
        return await resp.json()


async def getPrices(params, fetch):
    async with aiohttp.ClientSession() as client:
        r = await fetch(client, params)
        return r


async def getCRYSTAL():
    chainId = "avalanchedfk"
    pairAddress = "0x48658e69d741024b4686c8f7b236d3f1d291f386"
    params = {'chainId': chainId, 'pairAddress': pairAddress}
    r = await getPrices(params, fetch_dexscreener)
    # r = await getPrices(params, fetch_cmc)
    return r


async def getJEWEL():
    chainId = "avalanchedfk"
    pairAddress = "0xCF329b34049033dE26e4449aeBCb41f1992724D3"
    params = {'chainId': chainId, 'pairAddress': pairAddress}
    r = await getPrices(params, fetch_dexscreener)
    # r = await getPrices(params, fetch_cmc)
    return r


async def getJADE():
    chainId = "kaia"
    pairAddress = "0x509d49AC90EF180363269E35b363E10b95c983AF"
    params = {'chainId': chainId, 'pairAddress': pairAddress}
    r = await getPrices(params, fetch_gecko)
    return r


@client.event
async def on_ready():
    logger.info(f"{client.user} Online")
    priceInfo.start()


@tasks.loop(seconds=9)
async def priceInfo():
    # JEWEL Price
    try:
        JEWEL = await getJEWEL()
        jewelPrice = float(JEWEL['pair']['priceUsd'])
        # jewelPrice = float(JEWEL['data']['priceUsd'])
    except Exception:
        jewelPrice = 0

    activity_string = f"JEWEL at ${round(jewelPrice, 3)}"
    # print(activity_string)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))

    await asyncio.sleep(3)

    # CRYSTAL Price
    try:
        CRYSTAL = await getCRYSTAL()
        crystalPrice = float(CRYSTAL['pair']['priceUsd'])
        # crystalPrice = float(CRYSTAL['data']['priceUsd'])
    except Exception:
        crystalPrice = 0

    activity_string = f"CRYSTAL at ${round(crystalPrice, 4)}"
    # print(activity_string)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))

    await asyncio.sleep(3)

    # JADE Price
    try:
        JADE = await getJADE()
        # jadePrice = float(JADE['pair']['priceUsd'])
        # jadePrice = float(JADE['data']['priceUsd'])
        # jadePrice = float(JADE['data']['priceQuote']) * jewelPrice
        jadePrice = float(JADE['data']['attributes']['price_in_usd'])  # GeckoTerminal
    except Exception:
        jadePrice = 0

    activity_string = f"JADE at ${round(jadePrice, 4)}"
    # print(activity_string)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_string))

client.run(os.getenv("TOKEN"))

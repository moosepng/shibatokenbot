import discord
import requests
import json
import asyncio
from decimal import Decimal

bot = discord.Client(intents=discord.Intents.default())
bot_token = '###' #token is not here for privacy reasons


class Values():
    def __init__(self):
        self.price
        self.change24
        self.arrow

async def status_task():
    while True:
        a = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=shiba-inu&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true").text
        jsonfile = json.loads(a)
        Values.price = round(Decimal(jsonfile["shiba-inu"]["usd"]), 7)
        Values.change24 = round((jsonfile["shiba-inu"]["usd_24h_change"]), 2)
        if Values.change24 < 0:
            Values.arrow = '⬊'
            sign = " "
        elif Values.change24 > 0:
            Values.arrow = '⬈'
            sign = "+"
        else:
            Values.arrow = " "
            sign = " "
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{sign}{Values.change24}%'))
        for guild in bot.guilds:
            await guild.me.edit(nick=f'SHIB {Values.arrow} ${Values.price}')
        print(Values.price, Values.arrow, sign, Values.change24)
        await asyncio.sleep(60)

@bot.event
async def on_guild_join(ctx):
    await ctx.me.edit(nick=f'SHIB {Values.price}$ {Values.arrow}')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    bot.loop.create_task(status_task())
bot.run(bot_token)

import discord
import requests
from discord.ext import commands
import json
import asyncio
import faker
from faker import Faker
import random
import string
from random import randint
fake = Faker()
import time
from time import sleep
import datetime
from datetime import datetime, timedelta
now = datetime.now()
###### config ######

import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')

section_name = 'SELFBOT'

if cfg.has_section(section_name):
    required_keys = ['token', 'prefix']
    
    for key in required_keys:
        if not cfg.has_option(section_name, key):
            print("please fill out config file correctly, closing in 3 seconds")
            sleep (3)
            exit()

    token = cfg.get(section_name, 'token')
    twitch_url = cfg.get(section_name, 'stream_url')
    prefix = cfg.get(section_name, 'prefix')
    wltc = cfg.get(section_name, 'ltc')
    wbtc = cfg.get(section_name, 'btc')
    weth = cfg.get(section_name, 'eth')
    wcashapp = cfg.get(section_name, 'cashapp')
    wpaypal = cfg.get(section_name, 'paypal')

else:
    print(f"Error: Section '{section_name}' is missing in the configuration file, closing in 3 seconds")
    sleep (3)
    exit() 





#####################

bot = commands.Bot(command_prefix=prefix, self_bot=True)

#####################

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def ping(ctx):
    ping = round(bot.latency * 1000)
    response = f'``Latancy is {ping}ms``'
    await ctx.message.delete()
    await ctx.send(response)
    print ("command ping used")



# crypto
@bot.command()
async def crypto(ctx, currency):
        clink = ("https://www.binance.com/api/v3/ticker/price?symbol=" + currency + "USDT")
        cdata = requests.get(clink)
        cdata = cdata.json() 
        prices = f"{cdata['price']}"
        cresponse = f"``price of {currency} is ${round(prices)}"
        await ctx.message.delete()
        await ctx.send(cresponse)
        print ("command crypto used")


# nuke
@bot.command()
async def nuke(ctx, message, user):
    print ("nuking")
    if ctx.author == bot.user:

        for channel in ctx.guild.channels:
            await channel.delete()
            await asyncio.sleep(0.1)  

        for i in range(50): 
            try:
                channelspam = await ctx.guild.create_text_channel("nuked by " + user)
                await channelspam.send("@everyone " + message)
            except discord.errors.Forbidden:  
                await ctx.send("I don't have the necessary permissions")
                break
            except discord.errors.HTTPException as e:
                if e.status == 429:  
                    await ctx.send("Rate limited. Stopping further actions.")
                    break
                else:
                    await ctx.send(f"An error occurred: {e}")
                    break
            await asyncio.sleep(0.1)  



@bot.command()
async def passwordgen(ctx):
    password = ''.join(random.choice(string.ascii_letters) for i in range(30))
    await ctx.message.delete()
    await ctx.channel.send(f"```Password is: {password}```")

@bot.command()
async def fakeid(ctx):
    fname = fake.first_name()
    lname = fake.last_name()
    address = fake.address()
    job = fake.job()
    phone = fake.phone_number()
    emails = ["gmail.com", "yahoo.com", "proton.me", "hotmail.com"]
    emailchoice = random.choice(emails)
    emailnum = randint(1,10000)
    email = f"{fname}.{lname}{emailnum}@{emailchoice}"
    birthday = fake.date_of_birth()
    genders = ["Male", "Female"]
    gender = random.choice(genders)
    await ctx.message.delete()
    await ctx.send (f"""```ini

Full Name: {fname} {lname}
Email: {email}
Phone Number: {phone}
Occupation: {job}
Birthdate: {birthday}
Gender: {gender}
Address: {address}```""")


@bot.command(name="chatbypass", description="Bypass chat language restrictions.", usage="chatbypass [text]", aliases=["bypasschat"])
async def chatbypass(ctx, *, text):
    text = text.lower()
    regional_indicators = {
    'a': '𝚊',
    'b': '𝚋',
    'c': '𝚌',
    'd': '𝚍',
    'e': '𝚎',
    'f': '𝚏',
    'g': '𝚐',
    'h': '𝚑',
    'i': '𝚒',
    'j': '𝚓',
    'k': '𝚔',
    'l': '𝚕',
    'm': '𝚖',
    'n': '𝚗',
    'o': '𝚘',
    'p': '𝚙',
    'q': '𝚚',
    'r': '𝚛',
    's': '𝚜',
    't': '𝚝',
    'u': '𝚞',
    'v': '𝚟',
    'w': '𝚠',
    'x': '𝚡',
    'y': '𝚢',
    'z': '𝚣'
    }

    output = ""
    text = list(text)
    for letter in text:
        if letter in regional_indicators:
            output = output + regional_indicators[letter] + ""
        else:
            output = output + letter
    await ctx.message.delete()
    await ctx.send(output)


@bot.command()
async def ccgen(ctx):
    string1 = randint(1000,9999)
    string2 = randint(1000,9999)
    string3 = randint(1000,9999)
    string4 = randint(1000,9999)
    cvv = randint(100,999)
    fname = fake.first_name()
    lname = fake.last_name()
    name = f"{fname} {lname}"
    address = fake.address()
    expiremonth = random.randint(1, 12)
    expireyear = now.year + random.randint(1, 4)
    exdate = f"{expiremonth}/{expireyear}"
    brands = ["Visa", "Mastercard"]
    brand = random.choice(brands)
    cc = (f"""```css
Card Number: {string1} {string2} {string3} {string4}
CVV: {cvv}
Expire Date: {exdate}
Brand: {brand}
Name: {name}
Adress: {address}```""")
    await ctx.message.delete()
    await ctx.send(cc)

#mock
mocking_enabled = False
@bot.command()
async def mock(ctx, user: discord.User):
    global user_to_mock_id, mocking_enabled
    
    if mocking_enabled:
        mocking_enabled = False
        await ctx.message.delete()
        await ctx.send("Mocking is now turned off.")

        
    else:
        user_to_mock_id = user.id
        mocking_enabled = True
        await ctx.message.delete()
        await ctx.send(f"Mocking is now turned on for {user.display_name}.")


@bot.event
async def on_message(message):
    if mocking_enabled and message.author.id == user_to_mock_id:
        mocked_message = ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(message.content)])
        await message.channel.send(mocked_message)
    
    await bot.process_commands(message)

@bot.command()
async def howbig(ctx, user: discord.User):
    size = randint(1,15)
    msg = f"{user}'s dick is {size} inches long"
    await ctx.message.delete()

    await ctx.send(msg)

@bot.command()
async def howgay(ctx, user: discord.User):
    percent = randint(1,100)
    msg = f"{user} is {percent}% gay"
    await ctx.message.delete()

    await ctx.send(msg)

@bot.command
async def gping(ctx, user):
    await ctx.message.delete()

@bot.command()
async def meme(ctx):
    response = requests.get("https://meme-api.com/gimme")
    data = response.json()
    await ctx.message.delete()
    await ctx.send(data["title"] + "\n" + data["url"])


@bot.command(name="geoip", description="Get information from an IP address.", usage="geoip [ip]", aliases=["iplookup", "lookupip", "ipinfo"])
async def geoip(ctx, ip):
    data = requests.get(f"http://ip-api.com/json/{ip}").json()
    data2 = requests.get(f"https://ipqualityscore.com/api/json/ip/oOswzMILsf8QA7JGtaQDdXARfDtbKW1K/{ip}").json()

    country = data["country"]
    city = data["city"]
    zipCode = data["zip"]
    lat = data["lat"]
    lon = data["lon"]
    isp = data["isp"]
    as1 = data["as"]
    region = data["regionName"]
    await ctx.send(f"""```ini
[ {ip} information ]

Country: {country}
City: {city}
Region: {region}
ZIP: {zipCode}
LAT: {lat}
LON: {lon}
AS: {as1}
ISP: {isp}
```""",)   

@bot.command()
async def countdown(ctx, number: int):
    for count in range(number, 0, -1):
        await ctx.send(count)


import longvar     
@bot.command()
async def purgehack(ctx,):

    await ctx.send(longvar.purge)


afkon = False
@bot.command()
async def afkmode(ctx):
    global afkon
    if afkon == True:
        afkon = False
        await ctx.send("AFK off")
    elif afkon == False:
        afkon = True
        await ctx.send("AFK on")

@bot.event
async def on_message(message):
    if afkon:
        if message.author == bot.user:
            return
        if isinstance(message.channel, discord.DMChannel) or bot.process_commands(message):
            await message.channel.send(f'{message.author.mention} I am currently AFK, please message me when im availible')
    await bot.process_commands(message)


@bot.command()
async def linvertise(ctx, link):
    data = requests.get(f'https://ancient-dew-2472.fly.dev/api?url={link}')
    url = data.json()
    await ctx.send(url["bypassedlink"])


@bot.command
async def unshorten(ctx, link):
    data = requests.get(f'https://unshorten.me/s/{link}')
    url = data.json()
    await ctx.send(url["resolved_url"])

#####################


@bot.command()
async def activity(ctx, type, activity):
    if type == 'game':
        await bot.change_presence(activity=discord.Game(name=f"{activity}"))
    elif type == 'stream':
        await bot.change_presence(activity=discord.Streaming(name=f"{activity}", url=twitch_url))
    elif type == 'listening':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{activity}"))
    elif type == 'watching':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{activity}"))



### ODNT USE THIS IN PUBLIC SERVERS ####
@bot.command()
async def sendtoken(ctx):
    await ctx.send(f'{token}')
##########################################

@bot.command()
async def btc(ctx):
    await ctx.send(f"My BTC Wallet: {wbtc}")

@bot.command()
async def ltc(ctx):
    await ctx.send(f"My LTC Wallet: {wltc}")

@bot.command()
async def eth(ctx):
    await ctx.send(f"My ETH Wallet: {weth}")

@bot.command()
async def paypal(ctx):
    await ctx.send(f"My Paypal Account: {wpaypal}")

@bot.command()
async def cashapp(ctx):
    await ctx.send(f"My Cashapp Account: {wcashapp}")

###### YOU CAN ADD YOUR OWN PAYMENT DETAILS JUST ADD INTO CONFIG, AND MAKE A VARIABLE HERE ####

@bot.command()
async def pm(ctx):
    await ctx.send(f"""```LTC Address: {wltc}
BTC Address: {wbtc}
ETH Adress: {weth}
Paypal Account: {wpaypal}
Cashapp Account: {wcashapp}
```""")

@bot.command()
async def randomfact(ctx):
    fact = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
    data = fact.json()
    await ctx.send(data["text"])

@bot.command()
async def randomjoke(ctx):
    joke = requests.get("https://v2.jokeapi.dev/joke/Any")
    data = joke.json()
    await ctx.send(data["setup"])
    sleep(2)
    await ctx.send(data["delivery"])


bot.run(token)



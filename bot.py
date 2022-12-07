# bot.py
import asyncio
import sys
import os
import random
import re
import time
from os import listdir
from os.path import isfile, join
#!pip install discord
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from dotenv import load_dotenv
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver import Keys

from vars import *

#sys.path.append("/mnt/d/stu/prog/python/modules/")
#import frac


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')

intents = discord.Intents(messages=True, guilds=True)
intents.members = True
bot = commands.Bot(command_prefix='!')
#bot2 = commands.Bot(command_prefix='!', intents=intents) #to update, same with other things relating with intents
client = discord.Client()

@bot.event
async def on_ready():
    print("Ready")

    # initializing scheduler
    scheduler = AsyncIOScheduler()


    scheduler.add_job(poke, CronTrigger(hour="21", minute="37")) #)

    print("starting scheduler")
    scheduler.start()

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    #print(
        #f'{client.user} is connected to the following guild:\n'
       #,000 f'{guild.name}(id: {guild.id})'
   # )



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "1":
        await message.channel.send('1')

    elif message.content == 'raise-exception':
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'I am assistant. You can contact with me either on server or here. Type !help for possible commands and their syntax.')

@bot.command(name='cat', help='get a cat')
async def cat(ctx):
    filenames = next(os.walk('D:/Nowy folder/cat'), (None, None, []))[2]  # [] if no file
    filenamerandom = str('D:/Nowy folder/cat'+'/'+random.choice(filenames))
    #filenames = next(os.walk('/mnt/d/Nowy folder/cat'), (None, None, []))[2]  # [] if no file
    #filenamerandom = str('/mnt/d/Nowy folder/cat'+'/'+random.choice(filenames))
    await ctx.send('purr...', file=discord.File(filenamerandom))

    #onlyfiles = [f for f in listdir('C:\Users\x\Desktop\Nowy folder\style') if isfile(join('C:\Users\x\Desktop\Nowy folder\style', f))]
    #print(onlyfiles)

    #print(filenames)
    #print(str(f)
    #arr = next(os.walk(r'C:\Users\x\Desktop\stu\prog\python\bot'))[2]
    #print(arr)
@bot.command(name='catgen', help='generate a cat')
async def catgen(ctx):
    import requests
    import io
    url = 'https://thiscatdoesnotexist.com/'
    #files = {'media': open('test.jpg', 'rb')}
    resp = requests.get(url)
    #eq = requests.get(url, files=files)
    arr = io.BytesIO()
    #resp.content.save(arr, "PNG")
    arr.write(resp.content)
   
    arr.seek(0)
    
    #arr = arr.getvalue()
    await ctx.send(file=discord.File(arr, "cat.png"))
	
	
@bot.command(name='genanything', help='I will generate anything, just write what you want to see. optional params: amount=, sampling_steps=, CFG= '
                                      'example cat in house amount=3 sampling_steps=40 CFG=15')
async def genanything(ctx, *args, amount=2):
    from selenium import webdriver

    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager


    #options = webdriver.ChromeOptions()
    #options.binary_location = "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    #chrome_driver_binary = "/mnt/c/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
    #driver=webdriver.Chrome(executable_path=r'/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe')
    #driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get("http://127.0.0.1:7860")
    raw_input = ""
    for i in args:
        raw_input = raw_input + i+" "
    driver.implicitly_wait(20)

    print("cos")
    inputbox = driver.execute_script("return document.querySelector(\"body > gradio-app\").shadowRoot.querySelector(\"#txt2img_prompt > label > textarea\")")


    # if ',' in raw_input:
    #     amount, prompt = raw_input.split(",")
    #     amount = int(amount)
    # else:
    #     amount = 1
    #     prompt = raw_input

    #getting params

    amount = re.search(r'amount=[0-9]+', raw_input)
    amount = amount.group()

    if amount is None:
        amount = 1
    else:
        raw_input = raw_input.replace(amount,"")
        amount = re.search(r'[0-9]+', amount)
        amount = int(amount.group())
        gen_amounth = driver.execute_script(
            "return document.querySelector(\"body > gradio-app\").shadowRoot.querySelector(\"#component-61 > div.w-full.flex.flex-col > div > input\")")
        gen_amounth.clear()
        gen_amounth.send_keys(amount)


    sampling_steps = re.search(r'sampling_steps=[0-9]+', raw_input)
    sampling_steps = sampling_steps.group()

    if sampling_steps is None:
        sampling_steps = 20
    else:
        raw_input = raw_input.replace(sampling_steps, "")
        sampling_steps = re.search(r'[0-9]+', sampling_steps)
        sampling_steps = int(sampling_steps.group())
        gen_sampling_steps = driver.execute_script(
            "return document.querySelector(\"body > gradio-app\").shadowRoot.querySelector(\"#component-44 > div.w-full.flex.flex-col > div > input\")")
        gen_sampling_steps.clear()
        gen_sampling_steps.send_keys(sampling_steps)


    CFG = re.search(r'CFG=[0-9]+', raw_input)
    CFG = CFG.group()

    if CFG is None:
        CFG = 7
    else:
        raw_input = raw_input.replace(CFG, "")
        CFG = re.search(r'[0-9]+', CFG)
        CFG = int(CFG.group())
        gen_CFG = driver.execute_script(
            "return document.querySelector(\"body > gradio-app\").shadowRoot.querySelector(\"#component-64 > div.w-full.flex.flex-col > div > input\")")
        gen_CFG.clear()
        gen_CFG.send_keys(CFG)





    prompt=raw_input
    print(prompt)
    print(raw_input)

    inputbox.send_keys(prompt)#text

    driver.implicitly_wait(2)
    genbutton = driver.execute_script("return document.querySelector(\"body > gradio-app\").shadowRoot.getElementById(\"txt2img_generate\")")
    genbutton.click()


    #waiting for output######################

    driver.execute_script(
#sprawdza przypadek jak dodaje sie node i zmienia sie stroktora trzeba i czy ten node ma source
        """
let mutationObserver = new MutationObserver((changed, _) => {
  changed.forEach((mutationObject) => {
    mutationObject.addedNodes.forEach((element) => {
      if (element.src != null) alert("renderFinish");
    });
  });
});

mutationObserver.observe(
  document
    .querySelector("body > gradio-app")
    .shadowRoot.querySelector("#txt2img_gallery"),
  { attributes: true, childList: true, subtree: true }
);
        """

    )
    #
    print("czekanie")

 #bot klika w dowolne miejscegdzoe nie ma przycisku na stronie co t
 #sprawdz czy jest exception, on sie pokaze tylko kiedy jest alert present
 #jesli tak to wyslij output



    point = driver.execute_script(
        "return document.querySelector(\"body > gradio-app\").shadowRoot.querySelector(\"#component-42\")")
    while(1):

        time.sleep(1)

        try:
            point.click()
            print('CZEKAM NADAL')
        except UnexpectedAlertPresentException as e:
            print('ZAKONCZONE POPRAWNIE MOGE WYSLAC')
            break
    # pobiera plik z model - output
    # #wchodzi na local host, wpisuje tam tekst, i daje generate
    # #classname = scroll-hide block gr-box gr-input w-full gr-text-input  #raise

    outputs = []
    #linux filenames = next(os.walk('/mnt/d/programy/SDlocal/outputs/txt2img-images'), (None, None, []))[2]  #set output
    filenames = next(os.walk('D:\\Programy\\SDlocal\\outputs\\txt2img-images'), (None, None, []))[2]  # set output

    #linux filenamerandom = str('/mnt/d/Programy/SDlocal/outputs/txt2img-images'+'/'+filenames[-1])
    for i in range(0, amount):
        filenamerandom = str('D:\\Programy\\SDlocal\\outputs\\txt2img-images' + '\\' + filenames[-1-i])
        outputs.append(filenamerandom)



    #await ctx.send(file=discord.File(for f in outputs))#filenamerandom
    for f in outputs:
        await ctx.send(file=discord.File(f))

    outmessage="amount: %i\nsampling_steps: %i\nCFG: %i" % (amount,sampling_steps,CFG)
    await ctx.message.author.dm_channel.send(f'{outmessage}')

@bot.command()
async def getRandomUser(ctx):
    users = ctx.guild.members
    return random.choice(users)
async def poke():
    print("poked")
    #user = random.choice(ctx.message.channel.guild.members)
    a = bot.get_channel(CHANNEL) #to put in different server

    #a=user.dm_channel
    # print("random user: ")
    # #print(getRandomUser(ctx))
    # print(bot2.guilds[0].members)
    # print(len(bot2.guilds[0].members))
    #await bot.send_message(user, random.choice(poke_messages))
    await a.send(random.choice(a.members).mention + ", " +random.choice(poke_messages))

#@bot.command(name='temp')
async def temp(ctx):
    pass

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='trivia', help ='get some trivias')
async def trivia(ctx):
        with open('burned.log', 'r+') as f:
            filebody = str(f.read())
            if (str(ctx.message.author.id) not in filebody):
                    await ctx.message.author.create_dm()
                    await ctx.message.author.dm_channel.send(
                        f'{random.choice(trivias)}')
                    f.write(f'{filebody}\n{ctx.message.author.id} {ctx.message.author}')    
            
@bot.command(name='status', help ='My status')
async def status1(ctx):
     await ctx.message.author.create_dm()
     await ctx.message.author.dm_channel.send(f'{status}')
                   

@bot.command(name='timed_message', help= 'dd/mm/hh:mm text - i will get pm from you then')
async def timemessage(ctx, date, text:str):
        with open('mail.log', 'a') as f:      
            f.write(f'{date} {ctx.message.author}: {text}\n')    
            


#client.run(TOKEN)
bot.run(TOKEN)

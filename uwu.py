# Iam obsessed with imports being in descending order.
# Written by EchoQuill, on a laggy mobile that too.
# Make sure to star the github page.
#------------------------------------------------
# REMINDER:- THIS IS MOSTLY MADE FOR MOBILE
# it might look ugly in desktop consoles etc.
# iam bad with decorating cli.
#------------------------------------------------
# It would also be great if you understand that iam a new python developer
# Iam not that skilled so there might be some repetitions etc
# Please do give me advice on how to improve.
from flask import Flask, request, render_template, jsonify, redirect, url_for
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord import SyncWebhook
from rich.console import Console
from threading import Thread
from rich.panel import Panel
import discord.errors
import threading
import requests
import random
import asyncio
import logging
import discord
import secrets
import string
import shutil
import time
import json
import sys
import os
import re
def clear():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Others
        os.system('clear')
clear()
# For console.log thingy
console = Console()
# Random module seed for better anti detection.
#seed = secrets.randbelow(4765839360747)
#random.seed(seed)
# Console width size
console_width = shutil.get_terminal_size().columns
# Owo text art for panel 
owoArt = """
 _          __      _         
/ \     _  (_  _ |_|_|_  __|_ 
\_/\/\/(_) __)(/_| | |_)(_)|_ 
"""
owoPanel = Panel(owoArt, style="purple on black", highlight=False)

# Load json file
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
with open(resource_path("config.json")) as file:
    config = json.load(file)
#----------OTHER VARIABLES----------#
version = "0.0.8"
ver_check_url = "https://raw.githubusercontent.com/EchoQuill/owo-dusk/main/version.txt"
ver_check = requests.get(ver_check_url).text.strip()
list_captcha = ["to check that you are a human!","https://owobot.com/captcha","please reply with the following", "captcha"]
mobileBatteryCheckEnabled = config["termuxAntiCaptchaSupport"]["batteryCheck"]["enabled"]
mobileBatteryStopLimit = config["termuxAntiCaptchaSupport"]["batteryCheck"]["minPercentage"]
termuxNotificationEnabled = config["termuxAntiCaptchaSupport"]["notifications"]
termuxTtsEnabled = config["termuxAntiCaptchaSupport"]["texttospeech"]["enabled"]
termuxTtsContent = config["termuxAntiCaptchaSupport"]["texttospeech"]["content"]
termuxVibrationEnabled = config["termuxAntiCaptchaSupport"]["vibrate"]["enabled"]
termuxVibrationTime = config["termuxAntiCaptchaSupport"]["vibrate"]["time"] * 1000
desktopNotificationEnabled = config["desktopNotificationEnabled"]
websiteEnabled = config["website"]
if desktopNotificationEnabled:
    try:
        from plyer import notification
    except:
        clear()
        console.print(f"-{System}[0] Plyer is not installed, attempting to install automatically.. if this doesn't work please run 'pip install plyer' In your console and run the script again...".center(console_width - 2 ), style = "red on black")
        os.system("pip install plyer")
if termuxTtsEnabled:
    clear()
    os.system("mkfifo ~/.tts")
    console.print(f"-System[0] setting up Text To Speech for faster usage... if this takes way too long then you should consider disabling Termux TTs...", style = "cyan on black")
    os.system("cat ~/.tts | termux-tts-speak")
    clear()
webhookEnabled = config["webhookEnabled"]
if webhookEnabled:
    webhook_url = config["webhook"]
    webhookUselessLog = config["webhookUselessLog"]
    dwebhook = SyncWebhook.from_url(webhook_url)
else:
    webhookUselessLog = False
webhook_url = config["webhook"]
setprefix = config["setprefix"]
#----------MAIN VARIABLES----------#
listUserIds = []
autoHunt = config["commands"][0]["hunt"]
autoBattle = config["commands"][0]["battle"]
autoPray = config["commands"][1]["pray"]
autoCurse = config["commands"][1]["curse"]
userToPrayOrCurse = config["commands"][1]["userToPrayOrCurse"]
autoDaily = config["autoDaily"]
autoOwo = config["sendOwo"]
autoCrate = config["autoUse"]["autoUseCrate"]
autoLootbox = config["autoUse"]["autoUseLootbox"]
autoHuntGem = config["autoUse"]["autoGem"]["huntGem"]
autoEmpoweredGem = config["autoUse"]["autoGem"]["empoweredGem"]
autoLuckyGem = config["autoUse"]["autoGem"]["luckyGem"]
autoSpecialGem = config["autoUse"]["autoGem"]["specialGem"]
sleepEnabled = config["commands"][8]["sleep"]
minSleepTime = config["commands"][8]["minTime"]
maxSleepTime = config["commands"][8]["maxTime"]
sleepRandomness = config["commands"][8]["randomness"]
if autoHuntGem or autoEmpoweredGem or autoLuckyGem or autoSpecialGem:
    autoGem = True
else:
    autoGem = False
autoSell = config["commands"][2]["sell"]
autoSac = config["commands"][2]["sacrifice"]
autoQuest = config["commands"][4]["quest"]
ignoreDisable_Quest = config["commands"][4]["doEvenIfDisabled"]
rarity = ""
for i in config["commands"][2]["rarity"]:
    rarity = rarity + i + " "
autoCf = config["commands"][3]["coinflip"]
autoSlots = config["commands"][3]["slots"]
#GAMBLE
doubleOnLose = config["commands"][3]["doubleOnLose"]
gambleAllottedAmount = config["commands"][3]["allottedAmount"]
gambleStartValue = config["commands"][3]["startValue"]
#%%%%%%%
customCommands = config["customCommands"]["enabled"]
lottery = config["commands"][5]["lottery"]
lotteryAmt = config["commands"][5]["amount"]
lvlGrind = config["commands"][6]["lvlGrind"]
cookie = config["commands"][7]["cookie"]
cookieUserId = config["commands"][7]["userid"]
customCommandCnt = -1
for i in config["customCommands"]["commands"]:
    customCommandCnt+=1
if customCommandCnt >= 1:
    sorted_zipped_lists = sorted(zip(config["customCommands"]["commands"], config["customCommands"]["cooldowns"]), key=lambda x: x[1]) 
    sorted_list1, sorted_list2 = zip(*sorted_zipped_lists)
elif customCommandCnt == 0:
    sorted_list1 = config["customCommands"]["commands"]
    sorted_list2 = config["customCommands"]["cooldowns"]
#lotter amt check:-
if lotteryAmt > 250000:
    lotteryAmt = 250000
# Gems.
huntGems = ["057","056","055","054","053","052","051"]
empGems = ["071","070","069","068","067","066","065"]
luckGems = ["078","077","076","075","074","073","072"]
specialGems = ["085","084","083","082","081","080","079"]
qtemp = []
# Cooldowns
huntOrBattleCooldown = config["commands"][0]["cooldown"]
prayOrCurseCooldown = config["commands"][1]["cooldown"]
sellOrSacCooldown = config["commands"][2]["cooldown"]
gambleCd = config["commands"][3]["cooldown"]
lvlGrindCooldown = config["commands"][6]["cooldown"]
# Box print
def printBox(text, color):
    test_panel = Panel(text, style=color)
    console.print(test_panel)
# For lvl grind
def generate_random_string():
    characters = string.ascii_lowercase + ' '
    length = random.randint(5, 20)
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string
# For battery check
def batteryCheckFunc():
    while True:
        time.sleep(120)
        battery_status = os.popen("termux-battery-status").read()
        battery_data = json.loads(battery_status)
        percentage = battery_data['percentage']
        console.print(f"-system[0] Current battery •> {percentage}".center(console_width - 2 ), style = "blue on black")
        if percentage < mobileBatteryStopLimit:
            break
    os._exit(0)
if mobileBatteryCheckEnabled:
    loop_thread = threading.Thread(target=batteryCheckFunc)
    loop_thread.start()
# Webhook Logging
def webhookSender(msg, desc=None):
    try:
        emb = discord.Embed(
        title=msg,
        description=desc,
        color=discord.Color.purple() # Double check
        )
    
        dwebhook.send(embed=emb, username='uwu bot warnings')
    except discord.Forbidden as e:
        print("Bot does not have permission to execute this command:", e)
    except discord.NotFound as e:
        print("The specified command was not found:", e)
    except Exception as e:
        print(e)
#-------------


#----------------------
#WEBSITE
#_____________


#APP
app = Flask(__name__)

# List to store captcha data
captchas = []
captchaAnswers = []
# API endpoint to add captchas
@app.route('/add_captcha', methods=['POST'])
def add_captcha():
    # Get data from API request
    data = request.get_json()
    captcha_type = data.get('type')
    url = data.get('url')
    username = data.get('username')

    # Add captcha to the list
    temp_index = len(captchas)
    captchaAnswers.append(None)
    captchas.append({'type': captcha_type, 'url': url, 'username': username})
    print(captchas)
    print(captchaAnswers)    
    # Return a response
    return jsonify({'status': temp_index})

# Render the main page
@app.route('/', methods=['GET'])
def index():
    try:
        if not captchas:
            # Render the green text if there are no captchas
            return render_template('index.html', no_captchas=True)
        else:
            # Render the page with captcha boxes
            return render_template('index.html', captchas=captchas)
    except Exception as e:
        print(f"error in index(): <index.html> :-> {e}")

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get the text from the input bar
    captcha_ans = request.form.get('text')
    captcha_index = request.form.get('captcha_index', type=int) 
    captchaAnswers[captcha_index] = captcha_ans
    print(captcha_ans)
    print(captchaAnswers[captcha_index])
    # Redirect back to the index page
    return redirect(url_for('index'))

def web_start():
    flaskLog = logging.getLogger('werkzeug')
    flaskLog.disabled = True
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    app.run(debug=False, use_reloader=False)
if websiteEnabled:
    web_thread = threading.Thread(target=web_start)
    web_thread.start()

#-------------
class MyClient(discord.Client):
    def __init__(self, token, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = int(channel_id)
        self.list_channel = [self.channel_id]
#----------SENDING COMMANDS----------#
    #Solve Captchas
    @tasks.loop()
    async def captchaSolver(self):
        if self.webInt != None and self.webSend == True and self.tempJsonData != None:
            print(captchaAnswers)
            print(captchaAnswers[self.webInt])
            print(self.user)
            self.tempListCount = 0
            #self.captchaAnswerGot = False
            print("attemting to solve")
            for i in captchas:
                if i == self.tempJsonData:
                    if captchaAnswers[self.tempListCount] != None:
                        print("got ans")
                        await self.dm.send(captchaAnswers[self.tempListCount])
                        await asyncio.sleep(random.uniform(5.5,9.7))
                        print(captchaAnswers[self.tempListCount])
                        captchaAnswers[self.tempListCount] = None
                self.tempListCount+=1    
            await asyncio.sleep(random.uniform(1.5,2.7))
    #Sleep
    @tasks.loop()
    async def random_account_sleeper(self):
        try:
            self.randSleepInt = random.randint(1,100)
            print(self.randSleepInt)
            if self.randSleepInt > (100 - sleepRandomness):
                self.f = True
                self.sleepTime = random.uniform(minSleepTime, maxSleepTime)
                console.print(f"-{self.user}[~] sleeping for {self.sleepTime} seconds".center(console_width - 2 ), style = "plum4 on black")
                await asyncio.sleep(self.sleepTime)
                console.print(f"-{self.user}[~] Finished sleeping {self.sleepTime} seconds".center(console_width - 2 ), style = "plum4 on black")
                self.f = False
            else:
                console.print(f"-{self.user}[~] skipped sleep".center(console_width - 2 ), style = "plum4 on black")
                await asyncio.sleep(random.uniform(60,120))
        except Exception as e:
            print(e)
    #daily
    @tasks.loop()
    async def send_daily(self):
        if self.f != True:
            if self.justStarted:
                await asyncio.sleep(random.uniform(21,67))
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}daily")
                self.last_cmd_time = time.time()
                self.lastcmd = "daily"
                console.print(f"-{self.user}[+] ran daily (next daily :> {self.formatted_time})".center(console_width - 2 ), style = "Cyan on black")
            self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
            self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst
        
            self.formatted_time = "{:02}h {:02}m {:02}s".format(
                int(self.time_until_12am_pst.total_seconds() // 3600),
                int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
                int(self.time_until_12am_pst.total_seconds() % 60)
)
            self.total_seconds = self.time_until_12am_pst.total_seconds()
        #print(f"Time till mext daily for {self.user.name} = {self.formatted_time}")
            await asyncio.sleep(self.total_seconds+random.uniform(30,90))
            self.current_time = time.time()
            self.time_since_last_cmd = self.urrent_time - self.last_cmd_time
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
            await self.cm.send(f"{setprefix}daily")
            console.print(f"-{self.user}[+] ran daily (next daily :> {self.formatted_time})".center(console_width - 2 ), style = "Cyan on black")
            if webhookUselessLog:
                webhookSender(f"-{self.user}[+] ran daily", f"next daily in {self.formatted_time}")
            self.lastcmd = "daily"
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    #hunt/battle
    @tasks.loop()
    async def send_hunt_or_battle(self):
        if not self.huntOrBattleSelected:
            if self.hb == 1:
                self.huntOrBattle = "battle"
            elif self.hb == 0:
                self.huntOrBattle = "hunt"
        if self.lastHb == 0:
            await asyncio.sleep(random.uniform(2.5,3.5))
        self.lastHb = self.hb
        if self.f != True:
            self.current_time = time.time()
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
            else:
                pass
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if not self.tempHuntDisable:
                await self.cm.send(f'{setprefix}{self.huntOrBattle}')
                console.print(f"-{self.user}[+] ran {self.huntOrBattle}.".center(console_width - 2 ), style = "purple on black")
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[+] ran {self.huntOrBattle}.")
                if self.hb == 1 and self.huntOrBattleSelected == False:
                    await asyncio.sleep(huntOrBattleCooldown + random.uniform(0.99, 1.10))
                elif self.huntOrBattleSelected == False:
                    await asyncio.sleep(random.uniform(0.3,0.6))
                else:
                    await asyncio.sleep(huntOrBattleCooldown + random.uniform(0.99, 1.10))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    #pray/curse
    @tasks.loop()
    async def send_curse_and_prayer(self):
        if self.justStarted:
            await asyncio.sleep(random.uniform(0.93535353, 1.726364646))
        if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
            await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))        
        if self.f != True:
            if userToPrayOrCurse and self.user.id != userToPrayOrCurse:
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                await self.cm.send(f'{setprefix}{self.prayOrCurse} <@{userToPrayOrCurse}>')
                self.lastcmd = self.prayOrCurse
                self.last_cmd_time = time.time()
            else:
                await self.cm.send(f'{setprefix}{self.prayOrCurse}')
                self.lastcmd = self.prayOrCurse
                self.last_cmd_time = time.time()
            console.print(f"-{self.user}[+] ran {self.prayOrCurse}.".center(console_width - 2 ), style = "magenta on black")
            if webhookUselessLog:
                webhookSender(f"-{self.user}[+] ran {self.prayOrCurse}.")
            await asyncio.sleep(prayOrCurseCooldown + random.uniform(0.99, 1.10))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
     # Coinflip
    @tasks.loop()
    async def send_cf(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.slotsLastAmt >= 250000:
                console.print(f"-{self.user}[-] Stopping coinflip 《250k exceeded》".center(console_width - 2 ), style = "red on black")
                if webhookEnabled:
                    webhookSender(f"-{self.user}[-] Stopping coinflip 《250k exceeded》.")
                self.send_cf.stop()
                return
            elif 0 >= self.gambleTotal:
                if webhookEnabled:
                    webhookSender(f"-{self.user}[-] Stopping All Gambling. 《allotted value exceeded》.")
                console.print(f"-{self.user}[-] Stopping coinflip 《allotted value exceeded》".center(console_width - 2 ), style = "red on black")
                self.send_slots.stop()
                self.send_cf.stop()
                return
                #add bj here...
            await self.cm.send(f'{setprefix}cf {self.cfLastAmt}')
            if webhookUselessLog:
                webhookSender(f"-{self.user}[-] ran Coinflip")
            console.print(f"-{self.user}[+] ran Coinflip.".center(console_width - 2 ), style = "cyan on black")
            await asyncio.sleep(gambleCd + random.uniform(0.28288282, 0.928292929))
   # Slots
    @tasks.loop()
    async def send_slots(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.slotsLastAmt >= 250000:
                if webhookEnabled:
                    webhookSender(f"-{self.user}[-] Stopping Slots 《250k exceeded》.")
                console.print(f"-{self.user}[-] Stopping slots 《250k exceeded》".center(console_width - 2 ), style = "red on black")
                self.send_slots.stop()
                return
            elif 0 >= self.gambleTotal:
                if webhookEnabled:
                    webhookSender(f"-{self.user}[-] Stopping All Gambling. 《allotted value exceeded》.")
                console.print(f"-{self.user}[-] Stopping slots 《allotted value exceeded》".center(console_width - 2 ), style = "red on black")
                self.send_slots.stop()
                self.send_cf.stop()
                return
                #add bj here...
            await self.cm.send(f'{setprefix}slots {self.slotsLastAmt}')
            if webhookUselessLog:
                webhookSender(f"-{self.user}[-] ran Slots")
            console.print(f"-{self.user}[+] ran Slots.".center(console_width - 2 ), style = "cyan on black")
            await asyncio.sleep(gambleCd + random.uniform(0.28288282, 0.928292929))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
     # Owo top
    @tasks.loop()
    async def send_owo(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            await self.cm.send('owo')
            console.print(f"-{self.user}[+] ran owo".center(console_width - 2 ), style = "Cyan on black")
            if webhookUselessLog:
                webhookSender(f"-{self.user}[-] ran OwO")
            if autoOwo == False and self.owoQuest == True:
                self.owoTempInt+=1 
                if self.owoTempInt == self.owoTempIntTwo:
                    self.send_owo.stop()
            await asyncio.sleep(random.uniform(19.28288282, 21.928292929))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    # auto sell / auto sac.
    @tasks.loop()
    async def send_sell_or_sac(self):
        #print(self.hb)
        if not self.sellOrSacSelected:
            if self.ss == 1:
                self.sellOrSac = "sac"
                self.ss = 0
            elif self.ss == 0:
                self.sellOrSac = "sell"
                self.ss = 1
        if self.f != True:
            self.current_time = time.time()
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                await self.cm.send(f'{setprefix}{self.sellOrSac} {rarity}')
                self.last_cmd_time = time.time()
                if webhookEnabled:
                    webhookSender(f"-{self.user}[+] ran {self.sellOrSac}")
                console.print(f"-{self.user}[+] ran {self.sellOrSac}".center(console_width - 2 ), style = "Cyan on black")
                await asyncio.sleep(sellOrSacCooldown + random.uniform(0.377373, 1.7373828))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
     # Custom commands
    @tasks.loop()
    async def send_custom(self):
        if self.f != True:
            for i in range(customCommandCnt):
                if i != 0 and i+1 <= customCommandCnt:    
                    await asyncio.sleep(random.uniform((sorted_list2[i] - sorted_list2[i-1]) + 0.3, (sorted_list2[i] - sorted_list2[i-1]) + 0.5))
                elif i == 0:
                    await asyncio.sleep(random.uniform(sorted_list2[i] + 0.3, sorted_list2[i] + 0.5))
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
                await self.cm.send(sorted_list1[i])
                self.last_cmd_time = time.time()
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    # Quests
    @tasks.loop()
    async def check_quests(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            await self.cm.send(f'{setprefix}quest')
            self.qtemp2 = False
            console.print(f"-{self.user}[+] checking quest status...".center(console_width - 2 ), style = "magenta on black")
            self.last_cmd_time = time.time()
            await asyncio.sleep(random.uniform(500.28288282, 701.928292929))
            if self.qtemp:
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
                self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst       
                self.formatted_time = "{:02}h {:02}m {:02}s".format(
                    int(self.time_until_12am_pst.total_seconds() // 3600),
                    int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
                    int(self.time_until_12am_pst.total_seconds() % 60)
            )
                self.total_seconds = self.time_until_12am_pst.total_seconds()
                await asyncio.sleep(self.total_seconds + random.uniform(34.377337,93.7473737))
        else:        
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    # Lottery
    @tasks.loop()
    async def send_lottery(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            await self.cm.send(f'{setprefix}lottery {lotteryAmt}')
            self.last_cmd_time = time.time()
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
            self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst       
            self.formatted_time = "{:02}h {:02}m {:02}s".format(
                int(self.time_until_12am_pst.total_seconds() // 3600),
                int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
                int(self.time_until_12am_pst.total_seconds() % 60)
        )
            self.total_seconds = self.time_until_12am_pst.total_seconds()
            console.print(f"-{self.user}[+] ran lottery. {self.total_seconds}".center(console_width - 2 ), style = "cyan on black")
            if webhookEnabled:
                webhookSender(f"-{self.user}[+] ran lottery.", f"Running Lottery again in {self.total_seconds}")
            await asyncio.sleep(self.total_seconds + random.uniform(34.377337,93.7473737))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
     # Lvl grind
    @tasks.loop()
    async def lvlGrind(self):
        if self.f != True:
            await self.cm.send(generate_random_string()) # Better than sending quotes(In my opinion).
            console.print(f"-{self.user}[+] Send random strings(lvl grind)".center(console_width - 2 ), style = "purple3 on black")
            if webhookEnabled:
                webhookSender(f"-{self.user}[+] send random strings.", "This is for level grind")
            await asyncio.sleep(random.uniform(lvlGrindCooldown + 0.1, lvlGrindCooldown + 0.4))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))
    # cookie
    @tasks.loop()
    async def send_cookie(self):
        if self.f != True:
            if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1, 0.3))
            await self.cm.send(f'{setprefix}cookie {cookieUserId}')
            
            self.last_cmd_time = time.time()
            self.current_time = time.time()
            self.time_since_last_cmd = self.current_time - self.last_cmd_time
            self.current_time_pst = datetime.utcnow() - timedelta(hours=8)
            self.time_until_12am_pst = datetime(self.current_time_pst.year, self.current_time_pst.month, self.current_time_pst.day, 0, 0, 0) + timedelta(days=1) - self.current_time_pst       
            self.formatted_time = "{:02}h {:02}m {:02}s".format(
                int(self.time_until_12am_pst.total_seconds() // 3600),
                int((self.time_until_12am_pst.total_seconds() % 3600) // 60),
                int(self.time_until_12am_pst.total_seconds() % 60)
        )
            self.total_seconds = self.time_until_12am_pst.total_seconds()
            if webhookEnabled:
                webhookSender(f"-{self.user}[+] send cookie.", f"Trying cookie again in {self.total_seconds}")
            console.print(f"-{self.user}[+] send cookie. {self.total_seconds}".center(console_width - 2 ), style = "cyan on black")
            await asyncio.sleep(self.total_seconds + random.uniform(34.377337,93.7473737))
        else:
            await asyncio.sleep(random.uniform(1.12667373732, 1.9439393929))

#---------ON READY----------#
    async def on_ready(self):
        self.on_ready_dn = False
        self.cmds = 1
        self.cmds_cooldown = 0
        printBox(f'-Loaded {self.user.name}[*].'.center(console_width - 2 ),'bold purple on black' )
        listUserIds.append(self.user.id)
        await asyncio.sleep(0.12)
        try:
            self.cm = self.get_channel(self.channel_id)           
            qtemp.append(self.cm.guild.id)
        except Exception as e:
            print(e)
        try:
            self.dm = await self.fetch_user(408785106942164992)
        except Exception as e:
            print(e)
            print(f"try send a message to owo bot using {self.user.name} acc")
        self.list_channel.append(self.dm.dm_channel.id)
        self.qtemp = False
        self.qtemp2 = True
        self.owoQuest = False
        self.friendCurseQuest = False
        self.friendPrayQuest = False
        self.cookieQuest = False
        self.actionQuest = False
        self.owoTempInt = 0
        self.owoTempIntTwo = 0
        self.battleWithFriendQuest = False
        self.hunt = None
        self.webInt = None
        self.webSend = False
        self.tempHuntDisable = False
        self.battle = None
        self.justStarted = True
        self.list_channel = [self.channel_id, self.dm.dm_channel.id]
        try:
            self.owoSupportChannel = self.get_channel(465978474163601436)
            self.list_channel.append(self.owoSupportChannel.channel.id)
        except:
            self.owoSupportChannel = None
        self.spams = 0
        self.last_cmd_time = 0
        self.randSleepInt = 0
        self.lastcmd = None
        self.busy = False
        self.hb = 0
        self.lastHb = None
        self.ss = 0
        self.hCount = 0
        self.time_since_last_cmd = 0
        self.tempForCheck = False
        self.f = False
        self.questDone = False
        self.gemHuntCnt = None
        self.gemEmpCnt = None
        self.gemLuckCnt = None
        self.gemSpecialCnt = None
        self.gems = autoGem
        self.invCheck = False
        self.gambleTotal = gambleAllottedAmount
        self.task_methods = []
        # Starting hunt/battle loop
        self.on_ready_dn = True
        if autoHunt or autoBattle:
            if autoHunt and autoBattle:
                self.huntOrBattle = None
                self.huntOrBattleSelected = False
            elif autoHunt:
                self.huntOrBattle = "hunt"
                self.huntOrBattleSelected = True
            else:
                self.huntOrBattle = "battle"
                self.huntOrBattleSelected = True
            #self.send_hunt_or_battle.start()
            self.task_methods.append(self.send_hunt_or_battle.start)
         # Starting curse/pray loop
        if autoCurse or autoPray:
            if autoCurse:
                self.prayOrCurse = "curse"
            else:
                self.prayOrCurse = "pray"
            self.task_methods.append(self.send_curse_and_prayer.start)
        # Starting Daily loop
        if autoDaily:
            self.task_methods.append(self.send_daily.start)
        # Starting Auto Owo
        if autoOwo:
            self.task_methods.append(self.send_owo.start)
            #self.send_owo.start()
        await asyncio.sleep(random.uniform(0.4,0.8))
        # Send Cookie
        if cookie:
            self.task_methods.append(self.send_cookie.start)
        # Starting Coinflip
        if autoCf:
            if doubleOnLose:
                self.cfMulti = 2
            else:
                self.cfMulti = 1
            self.cfLastAmt = gambleStartValue
            print("ctest")
            self.task_methods.append(self.send_cf.start)
            print("ctest2")
        # Starting slots CHEXK
        if autoSlots:
            if doubleOnLose:
                self.slotsMulti = 2
            else:
                self.slotsMulti = 1
            self.slotsLastAmt = gambleStartValue
            print("test")
            self.task_methods.append(self.send_slots.start)
            print("test2")
        # Start Sell or Sac
        if autoSell or autoSac:
            if autoSell and autoSac:
                self.sellOrSac = None
                self.sellOrSacSelected = False
            elif autoSell:
                self.sellOrSac = "sell"
                self.sellOrSacSelected = True
            else:
                self.sellOrSac = "sac"
                self.sellOrSacSelected = True
            #self.send_sell_or_sac.start()
            self.task_methods.append(self.send_sell_or_sac.start)
        # Send Custom Commands
        if customCommands:
            #self.send_custom.start()
            self.task_methods.append(self.send_custom.start)
        # Do auto quest
        if autoQuest:
            #self.check_quests.start()
            self.task_methods.append(self.check_quests.start)
        # Random Breaks
        if sleepEnabled:
                self.random_account_sleeper.start()
        # Auto Lottery
        if lottery:
            #self.send_lottery.start()
            self.task_methods.append(self.send_lottery.start)
        # Send Random strings
        if lvlGrind:
            self.task_methods.append(self.lvlGrind.start)
            
        # Shuffle and start all loops
        random.shuffle(self.task_methods)
        for task_method in self.task_methods:
            task_method()
            await asyncio.sleep(random.uniform(0.4,0.8))
                
        embed1 = discord.Embed(
            title='logging in',
            description=f'logged in as {self.user.name}',
            color=discord.Color.dark_green()
        )

        if webhookEnabled:
            dwebhook.send(embed=embed1, username='uwu bot') 
        await asyncio.sleep(random.uniform(2.69,3.69))
        if desktopNotificationEnabled:
            pass
        self.justStarted = False
#----------ON MESSAGE----------#
    async def on_message(self, message):
        if not self.on_ready_dn:
            return
        if message.author.id != 408785106942164992:
            return
        if "I have verified that you are human! Thank you! :3" in message.content and message.channel.id in self.list_channel:
            console.print(f"-{self.user}[+] Captcha solved. restarting...".center(console_width - 2 ), style = "dark_magenta on black")
            await asyncio.sleep(random.uniform(0.69,1.69))
            self.f = False
            if webhookEnabled:
                webhookSender(f"-{self.user}[+] Captcha solved. restarting...")
            print(f'int {self.webInt} bool(webSend) {self.webSend} -- {self.user}')
            if websiteEnabled and self.webInt != None:
                print("attempting to pop captcha indirectly")
                while True:
                    self.tempListCount = 0
                    self.popped = False
                    for i in captchas:
                        if i == self.tempJsonData:
                            captchas.pop(self.tempListCount)
                            captchaAnswers.pop(self.tempListCount)
                            print("popped captcha indirectly")
                            self.popped = True
                            break
                        self.tempListCount+=1
                    if self.popped:
                        break
                    print("loopinh while")
                print(captchas , captchaAnswers)
                self.webInt = None
                    
                self.captchaSolver.stop()
                self.webSend = False
                print(f'int {self.webInt} bool(webSend) {self.webSend} -- {self.user} after solving')
                print(f"{self.user} stopped captcha solver")
            return
        if any(b in message.content.lower() for b in list_captcha) and message.channel.id in self.list_channel:
            print("test")
            if "I have verified that you are human! Thank you! :3" in message.content and message.channel.id in self.list_channel:
                console.print(f"-{self.user}[+] Captcha solved. restarting...".center(console_width - 2 ), style = "dark_magenta on black")
                self.f = False
                self.webSend = False
                console.print(f"-{self.user}[+] Captcha solved. restarted!!...".center(console_width - 2 ), style = "dark_magenta on black")
                if webhookEnabled:
                    webhookSender(f"-{self.user}[+] Captcha solved. restarting...")
                print(f'int {self.webInt} bool(webSend) {self.webSend} -- {self.user}')
                if websiteEnabled and self.webInt != None:
                    if captchas[self.webInt] == self.tempJsonData:
                        print("attempting to pop captcha directly")
                        try:
                            captchas.pop(self.webInt)
                            captchaAnswers.pop(self.webInt)
                        except Exception as e:
                            print(e)
                        print("popped captcha directly")
                    else:
                        print("attempting to pop captcha indirectly")
                        for i in range(captchas):
                            if captchas[i] == self.tempJsonData:
                                captchas.pop(i)
                                captchaAnswers.pop(i)
                                print("popped captcha indirectly")
                    print(captchas , captchaAnswers)
                    self.webInt = None
                    self.tempJsonData = None
                    self.captchaSolver.stop()
                    self.webSend = False
                    print(f'int {self.webInt} bool(webSend) {self.webSend} -- {self.user} after solving')
                    print(f"{self.user} stopped captcha solver")
                return
            else:
                try:
                    self.f = True
                    if termuxNotificationEnabled:
                        os.system(f"termux-notification -c 'captcha detected! {self.user.name}'")
                        os.system(f"termux-toast -c red -b black 'Captcha Detected:- {self.user.name}'")
                    console.print(f"-{self.user}[!] CAPTCHA DETECTED. waiting...".center(console_width - 2 ), style = "deep_pink2 on black")
                    embed2 = discord.Embed(
                        title=f'CAPTCHA :- {self.user} ;<',
                        description=f"user got captcha :- {self.user} ;<",
                        color=discord.Color.red()
                    )
                    if webhookEnabled:
                        dwebhook.send(embed=embed2, username='uwu bot warnings')
                    if termuxVibrationEnabled:
                       os.system(f"termux-vibrate -d {termuxVibrationTime}")
                       print("vibration")
                    #if termuxTtsEnabled:
                    #    os.system(f"termux-tts-speak {termuxTtsContent}")
                    #    print("tts")
                    if desktopNotificationEnabled:
                        notification.notify(
                            title = f'{self.user}  DETECTED CAPTCHA',
                            message = "Pls solve it within 10min to prevent ban",
                            app_icon = None,
                            timeout = 15,
                        )
                    if self.webSend == False and websiteEnabled:
                        try:
                            if list_captcha[1] in message.content:
                           #self.curl_command = f'''curl -X POST http://localhost:5000/add_captcha \
  #-H "Content-Type: application/json" \
 # -d '{"type": "link", "url": "https://owobot.com/captcha", "username": "{self.user.name}}" ' '''
                                self.dataToSend = {
                                   "type": "link",
                                   "url": "https://owobot.com/captcha",
                                   "username": self.user.name
                                    }
                                
                                
                            elif message.attachments:
                                if message.attachments[0].url != None:
                                #self.curl_command = f'''curl -v -X POST http://localhost:5000/add_captcha \ -H "Content-Type: application/json" \ -d '{"type": "image", "url": "{str(message.attachments[0].url)}", "username": "{self.user.name}}" ' '''
                                    self.dataToSend = {
                                       "type": "image",
                                       "url": str(message.attachments[0].url),
                                       "username": self.user.name
                                        }
                                    self.captchaSolver.start()
                                    self.webSend = True
                        except Exception as e:
                            print(f"error when attempting to send captcha to web {e}")
                            print(f"error for {self.user}")
                        try:
                            if self.webInt == None:
                                self.data_json = json.dumps(self.dataToSend)
                                self.curl_command = f'curl -X POST http://localhost:5000/add_captcha -H "Content-Type: application/json" -d \'{self.data_json}\' ' 
                                self.response_json = os.popen(self.curl_command).read() 
                                self.response_dict = json.loads(self.response_json)
                                self.webInt = int(self.response_dict.get('status'))
                                self.tempJsonData = captchas[self.webInt]
                                print(self.webInt , "from curl post section")                            
                                print("captcha solver started")
                                
                        except Exception as e:
                            print(f'Error when trying to get status :-> {e} Error for {self.user}')
                    console.print(f"-{self.user}[!] Delay test successfully completed!.".center(console_width - 2 ), style = "deep_pink2 on black")
                    return
                except Exception as e:
                    print(e)
        if "☠" in message.content and "You have been banned for" in message.content and message.channel.id in self.list_channel:
            self.f = True
            if termuxNotificationEnabled:
                os.system(f"termux-notification -c 'BAN DETECTED! {self.user.name}'")
                os.system(f"termux-toast -c red -b black 'BAN DETECTED:- {self.user.name}'")
            console.print(f"-{self.user}[!] BAN DETECTED.".center(console_width - 2 ), style = "deep_pink2 on black")
            embed2 = discord.Embed(
                    title=f'BANNED IN OWO :- {self.user} ;<',
                    description=f"user got banned :- {self.user} ;<",
                    color=discord.Color.red()
                                )
            if webhookEnabled:
                dwebhook.send(embed=embed2, username='uwu bot warnings')
            if termuxVibrationEnabled:
                os.system(f"termux-vibrate -d {termuxVibrationTime}")
            #if termuxTtsEnabled:
            #    os.system(f"termux-tts-speak user got banned!")
            # temp disabled tts
            if desktopNotificationEnabled:
                notification.notify(
                    title = f'{self.user}[!] User BANNED in OwO!!',
                    message = "Sad...",
                    app_icon = None,
                    timeout = 15,
                    )
            console.print(f"-{self.user}[!] Delay test successfully completed!.".center(console_width - 2 ), style = "deep_pink2 on black")
            return
        if message.channel.id == self.channel_id and "please slow down~ you're a little **too fast** for me :c" in message.content.lower():
            pass
        if message.channel.id == self.channel_id and "slow down and try the command again" in message.content.lower():
            await asyncio.sleep(random.uniform(3.9,5.2))
            if self.f:
                return
            if self.lastcmd == "hunt":
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}hunt")
                console.print(f"-{self.user}[+] ran hunt.".center(console_width - 2 ), style = "purple on black")
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[+] ran hunt")
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
            if self.lastcmd == "battle":
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}battle")
                console.print(f"-{self.user}[+] ran battle.".center(console_width - 2 ), style = "purple on black")
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[+] ran battle")
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
        if message.channel.id == self.channel_id and ('you found' in message.content.lower() or "caught" in message.content.lower()):
            self.hb = 1
            self.last_cmd_time = time.time()
            self.lastcmd = "hunt"
            if "caught" in message.content.lower() and self.gems:
                if self.f:
                    return
                self.current_time = time.time()
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}inventory")
                console.print(f"-{self.user}[~] checking Inventory....".center(console_width - 2 ), style = "Cyan on black")
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[~] checking Inventory.", "For autoGem..")
                self.invCheck = True
        if message.channel.id == self.channel_id and ("you found a **lootbox**!" in message.content.lower() or "you found a **weapon crate**!" in message.content.lower()):
            if self.f:
                return
            if "**lootbox**" in message.content.lower() and autoLootbox:
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}lb all")
                console.print(f"-{self.user}[+] used lootbox".center(console_width - 2 ), style = "magenta on black")
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[+] used lootbox")
                await asyncio.sleep(random.uniform(0.3,0.5))
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
            elif "**weapon crate**" in message.content.lower() and autoCrate:
                self.current_time = time.time()
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                await self.cm.send(f"{setprefix}crate all")
                if webhookUselessLog:
                    webhookSender(f"-{self.user}[+] used crates")
                console.print(f"-{self.user}[+] used all crates".center(console_width - 2 ), style = "magenta on black")
                await asyncio.sleep(random.uniform(0.3,0.5))
                self.time_since_last_cmd = self.current_time - self.last_cmd_time
        if message.channel.id == self.channel_id and "Inventory" in message.content and "=" in message.content.lower():
            if self.invCheck:
                self.invNumbers = re.findall(r'`(\d+)`', message.content)
                self.tempHuntDisable = True
                self.tempForCheck = False
                self.sendingGemsIds = ""
                if autoHuntGem:
                    for i in huntGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds = self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break                            
                self.tempForCheck = False
                if autoEmpoweredGem:
                    for i in empGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds = self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break
                self.tempForCheck = False
                if autoLuckyGem:
                    for i in luckGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds = self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break
                self.tempForCheck = False
                if autoSpecialGem:
                    for i in specialGems:
                        for o in self.invNumbers:
                            if i == o:
                                self.sendingGemsIds = self.sendingGemsIds + str(i) + " "
                                self.tempForCheck = True
                                break
                        if self.tempForCheck == True:
                            break
                if self.time_since_last_cmd < 0.5:  # Ensure at least 0.3 seconds wait
                    await asyncio.sleep(0.5 - self.time_since_last_cmd + random.uniform(0.1,0.3))
                self.tempForCheck = False
               # print(self.sendingGemsIds)
                if self.sendingGemsIds != "":
                    await self.cm.send(f'{setprefix}use {self.sendingGemsIds}')
                    console.print(f"-{self.user}[+] used gems({self.sendingGemsIds})".center(console_width - 2 ), style = "Cyan on black")
                    if webhookUselessLog:
                        webhookSender(f"-{self.user}[+] used Gems({self.sendingGemsIds})")
                    self.last_cmd_time = time.time()
                else:
                    self.gems = False
                    console.print(f"-{self.user}[!] No gems to use... disabling...".center(console_width - 2 ), style = "deep_pink2 on black")
                self.invCheck = False
                self.tempHuntDisable = False
                self.sendingGemsIds = ""
        if message.embeds and message.channel.id == self.channel_id:
            for embed in message.embeds:
                if embed.author.name is not None and "goes into battle!" in embed.author.name.lower():
                    self.hb = 0 #check
                    self.last_cmd_time = time.time()
                    self.lastcmd = "battle"
                if embed.author.name is not None and "quest log" in embed.author.name.lower():
                    if not autoQuest:
                        return
                    if "you finished all of your quests!" in embed.description.lower():
                        self.qtemp = True
                        self.qtemp2 = False
                        #set qtemp2 to True if quest. Otherwise False
                        return
                    if "Manually hunt'" not in message.content:
                        self.owoQuest = False
                    else:
                        self.owoTempIntTwo = re.findall(r"\'owo\'\s*(\d+)\s*times", message.content)
                        if autoOwo == False:
                            self.owoQuest = True
                            self.send_owo.start()
                    if "Have a friend pray to you" not in message.content:
                        self.friendPrayQuest = False
                    else:
                        #self.prayTempIntTwo = re.findall(r"\'owo\'\s*(\d+)\s*times", message.content)
                        if self.owoSupportChannel != None and self.qtemp2 == False:
                            await self.owoSupportChannel.send("owo quest")
                            self.qtemp2 = True
                        self.friendPrayQuest = True
                    if "Have a friend curse you" not in message.content:
                        self.friendCurseQuest = False
                    else:
                        #self.curseTempIntTwo = re.findall(r"\'owo\'\s*(\d+)\s*times", message.content)
                        if self.owoSupportChannel != None and self.qtemp2 == False:
                            await self.owoSupportChannel.send("owo quest")
                            self.qtemp2 = True
                        self.friendCurseQuest = True
                    if "Receive a cookie from 1 friends" not in message.content:
                        self.cookieQuest = False
                    else:
                        #self.cookieTempIntTwo = re.findall(r"\'owo\'\s*(\d+)\s*times", message.content)
                        if self.owoSupportChannel != None and self.qtemp2 == False:
                            await self.owoSupportChannel.send("owo quest")
                            self.qtemp2 = True
                        self.cookieQuest = True
                    if "xp from hunting and battling" not in message.content:
                        pass
                    else:
                        pass
                    if "Use an action command on someone" not in message.content:
                        self.actionQuest = False
                    else:
                        if self.owoSupportChannel != None and self.qtemp2 == False:
                            await self.owoSupportChannel.send("owo quest")
                            self.qtemp2 = True
                        self.actionQuest = True
                    if "Battle with a friend" not in message.content:
                        pass
                    else:
                        if self.owoSupportChannel != None and self.qtemp2 == False:
                            await self.owoSupportChannel.send("owo quest")
                            self.qtemp2 = True
#----------ON MESSAGE EDIT----------#
    async def on_message_edit(self, before, after):
        if before.author.id != 408785106942164992:
            return
        if before.channel.id != self.channel_id:
            return
        # slots
        if "slots" in after.content.lower():
            if "and won nothing... :c" in after.content:
              #  print(after.content)
                console.print(f"-{self.user}[+] ran Slots and lost {self.slotsLastAmt} cowoncy!.".center(console_width - 2 ), style = "magenta on black")
                if doubleOnLose:
                    self.slotsLastAmt = self.slotsLastAmt * 2
                self.gambleTotal-=self.slotsLastAmt
            else:
                #print(after.content)
                if "<:eggplant:417475705719226369>" in after.content.lower() and "and won" in after.content.lower():
                    console.print(f"-{self.user}[+] ran Slots and didn't win nor lose anything..".center(console_width - 2 ), style = "magenta on black")
                elif "and won" in after.content.lower():
                    self.gambleTotal+=self.slotsLastAmt
                    console.print(f"-{self.user}[+] ran Slots and won {self.slotsLastAmt}..".center(console_width - 2 ), style = "magenta on black")
                    if doubleOnLose:
                        self.slotsLastAmt = gambleStartValue
        #coinflip
        if "chose" in after.content.lower():
            if "and you lost it all... :c" in after.content.lower():
                console.print(f"-{self.user}[+] ran Coinflip and lost {self.cfLastAmt} cowoncy!.".center(console_width - 2 ), style = "magenta on black")
                self.gambleTotal-=self.cfLastAmt
                if doubleOnLose:
                    self.cfLastAmt = self.cfLastAmt*2
            else:
                console.print(f"-{self.user}[+] ran Coinflip and won {self.cfLastAmt} cowoncy!.".center(console_width - 2 ), style = "magenta on black")
                self.gambleTotal+=self.cfLastAmt
                if doubleOnLose:
                    self.cfLastAmt = gambleStartValue
#----------STARTING BOT----------#                 
def run_bots(tokens_and_channels):
    threads = []
    for token, channel_id in tokens_and_channels:
        thread = Thread(target=run_bot, args=(token, channel_id))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
def run_bot(token, channel_id):
    client = MyClient(token, channel_id)
    client.run(token, log_handler=None)
if __name__ == "__main__":
    console.print(owoPanel)
    print('-'*console_width)
    printBox(f'-Made by EchoQuill'.center(console_width - 2 ),'bold green on black' )
    printBox(f'-Current Version:- {version}'.center(console_width - 2 ),'bold cyan on black' )
    printBox(f'-This is a test version, anything can go wrong at any time. use at your own risk...'.center(console_width - 2 ),'bold plum4 on black' )
    if ver_check != version:
        console.print("""version does not seem to match the one at github
please update from:> https://github.com/EchoQuill/owo-dusk :>""", style = "yellow on black")
    if autoPray == True and autoCurse == True:
        console.print("Both autoPray and autoCurse enabled", style = "red on black")
    if termuxNotificationEnabled and desktopNotificationEnabled:
        console.print("Only enable either termux notifs of desktop notifs.", style = "red on black")
    tokens_and_channels = [line.strip().split() for line in open("tokens.txt", "r")]
    token_len = len(tokens_and_channels)
    printBox(f'-Loaded {token_len} accounts.'.center(console_width - 2 ),'bold magenta on black' )
    
    if desktopNotificationEnabled:
        notification.notify(
            title = f'{token_len} Tokens loaded!',
            message = "Thankyou for putting your trust on OwO-Dusk",
            app_icon = None,
            timeout = 15,
            )
    #print(token_len)
    run_bots(tokens_and_channels)
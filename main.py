import discord  #import all the necessary modules

import serial
import random
import json
import os
import random
import time
import threading
import cooldowns


from discord.ext import commands
from datetime import datetime, timedelta
from discord import Embed
from threading import Timer

import json

# ---------------------------------
# Change Directory to current folder
os.chdir(os.getcwd())
print(os.getcwd());


# Set Serial to Current Com
global serport
serport = serial.Serial("CHANGE TO YOUR COM PORT", baudrate=9600, timeout=1)


# Bot command prefix is what they type before command 'p.'play, where 'p.' is prefix
bot = commands.Bot(command_prefix='p.') #define command decorator

ledstate = False



nl = "\n"


# Cooldowns in seconds for each command
feedcooldown = 18000

petcooldown =  300

playcooldown =  9000


# Used to turn on notification leds on the bot and check if webhook command can be activated
global onfeedcd
onfeedcd = False

global onpetcd
onpetcd = False

global onplaycd
onplaycd = False
# ----------------------------------



# User Defined Functions ------------------------------------------------------



def createUser(user):
    users = getPlayerData()
    # check if account checkuserExist
    if str(user.id) in users:
        return False
    else:
        #make account
        users[str(user.id)] = {"PetName": "Buddy (Default: change with p.name (name))","health":100, "happiness":100, "death": False}
        with open("players.json","w") as file:
            json.dump(users,file)
        # with open("userid.txt", "a") as a_file:
        #     a_file.write(str(user.id))
        with open("userids.txt", "a") as a_file:
          a_file.write(str(user.id) + '\n')
    return True

def updateJSON(userdata):
    users = userdata
    with open('players.json',"w") as f:
        json.dump(users,f)


def getPlayerData():
    with open("players.json","r") as file:
        users = json.load(file)
    return users

    # Converts Seconds to Time format
def cooldownCheck(seconds):
    sec = timedelta(seconds=int(seconds))
    d = datetime(1,1,1) + sec
    desc = "%dd %dh %dm %ds" % (d.day-1, d.hour, d.minute, d.second)
    return desc

def checkUser(user):
    users = getPlayerData()
    # check if account checkuserExist
    if str(user.id) in users:
        return True
    else:
        return False

def subtractHp():

    filesize = os.path.getsize("userids.txt")
    # Checks if there are no users
    if filesize == 0:
        return


    mylist = []
    with open("userids.txt") as file:
        mylist = file.read().splitlines()
    userNum = len(mylist)
    users = getPlayerData()
    for x in range(userNum):
        # takeaway hp is random float between 5.65 and 6.5
        users[str(mylist[x])]["health"] -= round(random.uniform(.75,1.3),2)
        if users[str(mylist[x])]["health"] < 0:
            users[str(mylist[x])]["health"] = 0
            users[str(mylist[x])]["death"] = True;

        print("New Health: " + str(users[str(mylist[x])]["health"]))
    updateJSON(users)


def subtractHappiness():
    filesize = os.path.getsize("userids.txt")
    # Checks if there are no users
    if filesize == 0:
        return

    mylist = []
    with open("userids.txt") as file:
        mylist = file.read().splitlines()

    userNum = len(mylist)
    users = getPlayerData()
    for x in range(userNum):
        # takeaway hp is random float between 5.65 and 6.5
        check = random.randint(1,100)
        if check > 50:
            users[str(mylist[x])]["happiness"] -= random.randint(7,15)
            print("New Happiness: " + str(users[str(mylist[x])]["happiness"]))
        else:
            break
    updateJSON(users)

#





# notification Lights

    # pet light On

    # Pet CD / Light
def light1On():
    serport.write(b'light1On')
    print('Light 1 on')

    # Turn off cooldown
    global onpetcd
    onpetcd = False


    # Play CD / Light
def light2On():
    serport.write(b'light2On')
    print('Light 2 on')

    # Turn off cooldown
    onplaycd = False


    # Feed CD / Light
def light3On():
    serport.write(b'light3On')
    print('Light 3 on')

    # Turn off cooldown
    onfeedcd = False


    #  Pet light Off
def light1Off():
    serport.write(b'light1Off')
    print('Light 1 off')

def light2Off():
    serport.write(b'light2Off')
    print('Light 2 off')

def light3Off():
    serport.write(b'light3Off')
    print('Light 3 off')





# -----------------------------------------------------------------------------

# Run function every 1 hour decrease hp by random amount of health (.75-1.3)
# Run subtractHappiness every 2 hours decrease by random amount of happiness (7-15)


def runthread():
  threading.Timer(3600, runthread).start()
  subtractHp()
  subtractHappiness()

runthread()


# -----------------------------------------------------------------------------




# BOT COMMANDS
@bot.event #print that the bot is ready to make sure that it actually logged on
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# Set pet name
@bot.command()
async def name(ctx, args):
    check = checkUser(ctx.message.author)
    if check == False:
        em = discord.Embed(title="⛔ No Account Detected",description="Please register an account with `p.register`", color=0xe00034)
        await ctx.send(embed=em)
        play.reset_cooldown(ctx)
    else:

        # Grab user INFO
            # grab unique id
        user = ctx.author
            # get information for users array from JSON file
        users = getPlayerData()





        # Check for pet death
        if users[str(user.id)]["death"] == True:
            desc = "Your dog has passed away!" + " RIP:" + users[str(user.id)]["PetName"] + nl + "Please use p.adopt (newpetname) to adopt a new dog"
            em = discord.Embed(title=":skull_crossbones: You made an oopsie woopsie!" ,description = desc , color=0x949494)
            await ctx.send(embed=em)
            return


        users[str(user.id)]["PetName"] = args
        em = discord.Embed(title=":dog: PET NAME CHANGED!",description="Your pet's name has been changed to " + "`" +  users[str(user.id)]["PetName"] + "`" , color=0x00db1d)

        # Update JSON file after using command to update text file
        updateJSON(users)

        # adds your profile pic to embed
        em.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)



@bot.command()
async def adopt(ctx, args):
    check = checkUser(ctx.message.author)
    if check == False:
        em = discord.Embed(title="⛔ No Account Detected",description="Please register an account with `p.register`", color=0xe00034)
        await ctx.send(embed=em)
        play.reset_cooldown(ctx)
    else:

        # Grab user INFO
            # grab unique id
        user = ctx.author
            # get information for users array from JSON file
        users = getPlayerData()


        if users[str(user.id)]["death"] == True:
            users[str(user.id)]["PetName"] = args
            em = discord.Embed(title=":dog: YOU ADOPTED A DOG!",description= users[str(user.id)]["PetName"] + " is happy to be with you! " , color=0x00db1d)


            users[str(user.id)]["death"] = False
            users[str(user.id)]["happiness"] = 100
            users[str(user.id)]["health"] = 100

            # Update JSON file after using command to update text file
            updateJSON(users)

            # adds your profile pic to embed
            em.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=em)

        else:
            em = discord.Embed(title=":dog: Cannot Adopt",description= users[str(user.id)]["PetName"] + " is perfectly fine!" , color=0xe00034)



            # Update JSON file after using command to update text file
            updateJSON(users)

            # adds your profile pic to embed
            em.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=em)



@bot.command()
@commands.cooldown(1, 9000, commands.BucketType.user)
async def register(ctx):
    check = checkUser(ctx.message.author)
    if check == True:
        em = discord.Embed(title="⛔ Account is already made!",description="For help use `p.help`", color=0xe00034)
        await ctx.send(embed=em)
    else:
        createUser(ctx.author)
        em = discord.Embed(title=":white_check_mark: Account Registered!",description="To learn the list of commands please use \n `p.help`", color=0x00db1d)
        await ctx.send(embed=em)




# play command
@bot.command()
@commands.cooldown(1, playcooldown, commands.BucketType.default)
async def play(ctx):
        # CHECK IF USER EXIST ALREADY
        check = checkUser(ctx.message.author)
        if check == False:
            em = discord.Embed(title="⛔ No Account Detected",description="Please register an account with `p.register`", color=0xe00034)
            await ctx.send(embed=em)
            play.reset_cooldown(ctx)
        else:

            # Grab user INFO
                # grab unique id
            user = ctx.message.author
                # get information for users array from JSON file
            users = getPlayerData()

            # Check for pet death
            if users[str(user.id)]["death"] == True:
                desc = "Your dog has passed away!" + " RIP:" + users[str(user.id)]["PetName"] + nl + "Please use p.adopt (newpetname) to adopt a new dog"
                em = discord.Embed(title=":skull_crossbones: You made an oopsie woopsie!" ,description = desc , color=0x949494)
                await ctx.send(embed=em)
                return

            # Start timer for light to turn on
            threading.Timer(playcooldown, light2On).start()
            #  Set OnCooldown to true
            onplaycd = True

            #SEND ARDUINO SERIAL MESSAGE
            serport.write(b'play')



            petName = users[str(user.id)]["PetName"]

            happyincrease = random.randint(13,18)
            users[str(user.id)]["happiness"] += happyincrease

            # If happiness reaches over 100, put back down to 100
            if users[str(user.id)]["happiness"] > 100:
                users[str(user.id)]["happiness"] = 100

            em = discord.Embed(title="<a:pet:830178751094063164> You played with " + petName + "!"  ,description="", color=0xe91fff)
            footertext = petName + " really likes those tennis balls and frisbee play time! "+ " (" + "Happiness " + "+" + str(happyincrease)+ ")"
            em.set_footer(text=footertext)

            updateJSON(users)
            await ctx.send(embed=em)

# feed command
@bot.command()
@commands.cooldown(1, feedcooldown, commands.BucketType.default)
async def feed(ctx):
        # CHECK IF USER EXIST ALREADY
        check = checkUser(ctx.author)
        if check == False:
            em = discord.Embed(title="⛔ No Account Detected",description="Please register an account with `p.register`", color=0xe00034)
            await ctx.send(embed=em)
            feed.reset_cooldown(ctx)
        else:

            # Grab user INFO
                # grab unique id
            user = ctx.message.author
                # get information for users array from JSON file
            users = getPlayerData()


            # Check for pet death
            if users[str(user.id)]["death"] == True:
                desc = "Your dog has passed away!" + " RIP:" + users[str(user.id)]["PetName"] + nl +  "Please use p.adopt (newpetname) to adopt a new dog"
                em = discord.Embed(title=":skull_crossbones: You made an oopsie woopsie!" ,description = desc , color=0x949494)
                await ctx.send(embed=em)
                return

            # Start timer for light to turn on
            threading.Timer(feedcooldown, light3On).start()
            #  Set OnCooldown to true
            onfeedcd = True



            #SEND ARDUINO SERIAL MESSAGE FOR IMAGE PLAY
            serport.write(b'feed')

            petName = users[str(user.id)]["PetName"]
            petHealth = round(users[str(user.id)]["health"],2)
            petHappiness = users[str(user.id)]["happiness"]


            # Set up embded Message
            em = discord.Embed(title="<:food:830168205154451456> You fed " + petName + "!"  ,description="", color=0x00de00)

            if petHappiness > 50:

                users[str(user.id)]["health"] += random.randint(10,15)

                happyincrease = random.randint(5,10)
                users[str(user.id)]["happiness"] += happyincrease

                if users[str(user.id)]["happiness"] > 100:
                    users[str(user.id)]["happiness"] = 100

                print("Health after " + str(users[str(user.id)]["health"]))
                round(users[str(user.id)]["health"],2)
                # If health is past 100, set it to 100

                if (users[str(user.id)]["health"] > 100):
                    users[str(user.id)]["health"] = 100
                # If happiness reaches over 100, put back down to 100
                    footertext = petName + "'s health is at 100!" + " (" + "Happiness " + "+" + str(happyincrease)+ ")"

                else:
                    petHealth = round(users[str(user.id)]["health"],2)
                    footertext = petName + "'s health is at " + str(petHealth) + " (" + "Happiness " + "+" + str(happyincrease)+ ")"


            else:
                chanceNoEat = random.randint(1,100)
                print(chanceNoEat)
                if chanceNoEat > 50:

                    users[str(user.id)]["health"] += random.randint(10,15)

                    happyincrease = random.randint(5,10)
                    users[str(user.id)]["happiness"] += happyincrease


                    print("Health after " + str(users[str(user.id)]["health"]))
                    round(users[str(user.id)]["health"],2)
                    # If health is past 100, set it to 100

                    # If happiness reaches over 100, put back down to 100
                    # if users[str(user.id)]["happiness"] > 100:
                    #     users[str(user.id)]["happiness"] = 100


                    if (users[str(user.id)]["health"] > 100):
                        users[str(user.id)]["health"] = 100
                        footertext = petName + "'s health is at " + str(petHealth) + " (" + "Happiness " + "+" + str(happyincrease)+ ")"
                    else:
                        petHealth = round(users[str(user.id)]["health"],2)
                        footertext = petName + "'s health is at " + str(petHealth) + " (" + "Happiness " + "+" + str(happyincrease)+ ")"
                else:
                        em = discord.Embed(title="<:food:830168205154451456> You did not feed " + petName + "!"  ,description="", color=0x00de00)
                        footertext = petName + " chose not to eat because they're unhappy"

            em.set_footer(text=footertext)

            updateJSON(users)

            await ctx.send(embed=em)
            # await ctx.send("You fed" +  users[str(user.id)]["petName"]  +  "!")

# pet command
@bot.command()
@commands.cooldown(1, petcooldown, commands.BucketType.default)
# @cooldowns.cooldown(petcooldown)
async def pet(ctx):
    global onpetcd
    print ("onpetcd " + str(bool(onpetcd)))

    if onpetcd == False:
        # CHECK IF USER EXIST ALREADY
        check = checkUser(ctx.author)

        if check == False:
            em = discord.Embed(title="⛔ No Account Detected",description="Please register an account with `p.register`", color=0xe00034)
            await ctx.send(embed=em)
            pet.reset_cooldown(ctx)
        else:


            user = ctx.message.author
                # get information for users array from JSON file
            users = getPlayerData()

            # Check for pet death
            if users[str(user.id)]["death"] == True:
                desc = "Your dog has passed away!" + " RIP:" + users[str(user.id)]["PetName"] + nl + "Please use p.adopt (newpetname) to adopt a new dog"
                em = discord.Embed(title=":skull_crossbones: You made an oopsie woopsie!" ,description = desc , color=0x949494)
                await ctx.send(embed=em)
                return


            # Start thread to turn on led later
            threading.Timer(petcooldown, light1On).start()
            #  Set OnCooldown to true
            onpetcd = True

            #SEND ARDUINO SERIAL MESSAGE
            serport.write(b'pet')
            print("Serport")


            petName = users[str(user.id)]["PetName"]

            happyincrease = random.randint(5,10)
            users[str(user.id)]["happiness"] += happyincrease

            if users[str(user.id)]["happiness"] > 100:
                users[str(user.id)]["happiness"] = 100

            em = discord.Embed(title="<a:pet:830178751094063164> You pet " + petName + "!"  ,description="", color=0xfff582)
            footertext = petName + " likes the good pats. "+ " (" + "Happiness " + "+" + str(happyincrease)+ ")"
            em.set_footer(text=footertext)
            print("check")
            updateJSON(users)
            await ctx.send(embed=em)
    else:
        desc = "It takes 5mins"
        em = discord.Embed(title="<a:pet:830178751094063164> Petting is on cooldown!",description=desc, color=0xe00034)
        await ctx.send(embed=em)

@bot.command()
async def cds(ctx):
        global onpetcd
        global onfeedcd
        global onplaycd
        # command = bot.get_command('feed')

        # check if cd is up

        # FIRST CHECK IF USER IS REGISTERED
        check = checkUser(ctx.author)
        if check == False:
            em = discord.Embed(title="⛔ No Account Detected",description="Please register an account with `p.register`", color=0xe00034)
            await ctx.send(embed=em)
            pet.reset_cooldown(ctx)
        else:

            # Grab user INFO
                # grab unique id
            user = ctx.message.author
                # get information for users array from JSON file
            users = getPlayerData()

            # Check for pet death
            if users[str(user.id)]["death"] == True:
                desc = "Your dog has passed away!" + " RIP:" + users[str(user.id)]["PetName"] + nl + "Please use p.adopt (newpetname) to adopt a new dog"
                em = discord.Embed(title=":skull_crossbones: You made an oopsie woopsie!" ,description = desc , color=0x949494)
                await ctx.send(embed=em)
                return



            petHealth = round(users[str(user.id)]["health"],2)
            petHappiness = users[str(user.id)]["happiness"]
            petName = users[str(user.id)]["PetName"]


            if (feed.get_cooldown_retry_after(ctx) == 0):
                feedcd = "`You got more food! Feed " + "" + petName + "!`"
            else:
                feedcd = "You have to wait ~5hr "+ "(" + cooldownCheck(feed.get_cooldown_retry_after(ctx)) + ")"

            if (onpetcd == False):
                petcd = "`You can pet " + petName + " now!`"
            else:
                petcd = "You have to wait ~5m "+ "(" + cooldownCheck(pet.get_cooldown_retry_after(ctx)) + ")"

            if (play.get_cooldown_retry_after(ctx) == 0):
                playcd = "`" + petName + " wants to play with you!`"
            else:
                playcd = "You have to wait ~2.5hr "+ "(" + cooldownCheck(play.get_cooldown_retry_after(ctx)) + ")"


            # Emoji detection for dog
            if petHappiness > 80:
                emoji = ":smile:"
            elif petHappiness < 80 and petHappiness > 50:
                emoji = ":neutral_face:"
            else:
                emoji = ":confounded:"

            # combine ALL cd message
            hpandhap = ":heart: ***HP:  ***" + "   `" + str(petHealth) + "`" + " / " + emoji + "  ***Happiness:  ***" + "   `" + str(petHappiness) + "`"
            # combine ALL descriptions in one variable message
            d =  ":dog: " + "***" + petName + "***" + nl + nl + hpandhap + nl + nl + "<a:pet:830178751094063164> ***Petting:  ***" + petcd + nl + nl +"<a:play:830190266584924181> ***Play:  ***" + playcd + nl + nl + "<:food:830168205154451456> ***Feeding:  *** " + feedcd
            em = discord.Embed(title="**COOLDOWNS**",description = d, color=0xff6a00)

            # add profile logo to Embed
            em.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed=em)


# COOLDOWN MESSAGES

@feed.error
async def feed_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = cooldownCheck(error.retry_after)
        em = discord.Embed(title="<:food:830168205154451456> Feeding is on cooldown!",description=desc, color=0xe00034)
        await ctx.send(embed=em)

@pet.error
async def pet_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = cooldownCheck(error.retry_after)
        em = discord.Embed(title="<a:pet:830178751094063164> Petting is on cooldown!",description=desc, color=0xe00034)
        await ctx.send(embed=em)

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = cooldownCheck(error.retry_after)
        em = discord.Embed(title="<a:play:830190266584924181> Playing is on cooldown!",description=desc, color=0xe00034)
        await ctx.send(embed=em)

@register.error
async def register_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = cooldownCheck(error.retry_after)
        print (desc);
        em = discord.Embed(title="⛔ Register is on cooldown!",description=desc, color=0xe00034)
        await ctx.send(embed=em)



# @bot.event #print that the bot is ready to make sure that it actually logged on
# async def on_message(message):
#     if (message.webhook_id):
#         print("WEBHOOK BOIS")
#         return
#     else:
#         print("normal")
#         return
#
#     await bot.process_commands(message)

@bot.event
async def on_message(message):
    # do some extra stuff here
    if message.content.startswith('-debug'):
        await message.channel.send('THIS THING IS A BOT')
    if message.webhook_id:
        # await message.channel.send('OOFERS')
        if "botpet" in message.content:
            # desc = "ree"
            # em = discord.Embed(title="<a:pet:830178751094063164> Petting is on cooldown!",description=desc, color=0xe00034)
            # await message.channel.send(embed=em)
            global onpetcd
            # print("botRUN")
            # print ("onpetcd " + str(bool(onpetcd)))
            if onpetcd == False:
                filesize = os.path.getsize("userids.txt")
                # Checks if there are no users
                if filesize == 0:
                    check = False
                else:
                    check = True


                    # Grab top of user ids
                with open("userids.txt") as file:
                    mylist = file.read().splitlines()

                userid = mylist[0]


                if check == False:
                    em = discord.Embed(title="⛔ No Account Detected",description="Please register an account with `p.register`", color=0xe00034)
                    await ctx.send(embed=em)
                    pet.reset_cooldown(ctx)
                else:

                        # get information for users array from JSON file
                    users = getPlayerData()

                    # Check for pet death
                    if users[str(userid)]["death"] == True:
                        desc = "Your dog has passed away!" + " RIP:" + users[str(userid)]["PetName"] + nl + "Please use p.adopt (newpetname) to adopt a new dog"
                        em = discord.Embed(title=":skull_crossbones: You made an oopsie woopsie!" ,description = desc , color=0x949494)
                        await message.channel.send(embed=em)
                        return


                    # Start thread to turn on led later
                    threading.Timer(petcooldown, light1On).start()
                    #  Set OnCooldown to true
                    onpetcd = True
                    #
                    # #SEND ARDUINO SERIAL MESSAGE
                    # serport.write(b'pet')
                    # print("check4")


                    petName = users[str(userid)]["PetName"]

                    happyincrease = random.randint(5,10)
                    users[str(userid)]["happiness"] += happyincrease

                    if users[str(userid)]["happiness"] > 100:
                        users[str(userid)]["happiness"] = 100

                    em = discord.Embed(title="<a:pet:830178751094063164> You pet " + petName + "!"  ,description="", color=0xfff582)
                    footertext = petName + " likes the good pats. "+ " (" + "Happiness " + "+" + str(happyincrease)+ ")"
                    em.set_footer(text=footertext)
                    updateJSON(users)
                    await message.channel.send(embed=em)
            else:
                 # ON CD
                desc = ""
                em = discord.Embed(title="<a:pet:830178751094063164> Petting is on cooldown!",description=desc, color=0xe00034)
                await message.channel.send(embed=em)
        elif "botplay" in message.content:
            global onplaycd
            if onplaycd == False:

                filesize = os.path.getsize("userids.txt")
                # Checks if there are no users
                if filesize == 0:
                    check = False
                else:
                    check = True



                if check == False:

                    em = discord.Embed(title="⛔ No Account Detected",description="Please register an account with `p.register`", color=0xe00034)
                    await message.channel.send(embed=em)
                    play.reset_cooldown(ctx)
                else:

                    # Grab user INFO
                        # grab unique id
                        # Grab top of user ids
                    with open("userids.txt") as file:
                        mylist = file.read().splitlines()

                    userid = mylist[0]
                        # get information for users array from JSON file
                    users = getPlayerData()

                    # Check for pet death
                    if users[str(userid)]["death"] == True:
                        desc = "Your dog has passed away!" + " RIP:" + users[str(user.id)]["PetName"] + nl + "Please use p.adopt (newpetname) to adopt a new dog"
                        em = discord.Embed(title=":skull_crossbones: You made an oopsie woopsie!" ,description = desc , color=0x949494)
                        await message.channel.send(embed=em)
                        return

                    # Start timer for light to turn on
                    threading.Timer(playcooldown, light2On).start()
                    #  Set OnCooldown to true
                    onplaycd = True

                    #SEND ARDUINO SERIAL MESSAGE
                    serport.write(b'play')



                    petName = users[str(userid)]["PetName"]

                    happyincrease = random.randint(13,18)
                    users[str(userid)]["happiness"] += happyincrease

                    # If happiness reaches over 100, put back down to 100
                    if users[str(userid)]["happiness"] > 100:
                        users[str(userid)]["happiness"] = 100

                    em = discord.Embed(title="<a:pet:830178751094063164> You played with " + petName + "!"  ,description="", color=0xe91fff)
                    footertext = petName + " really likes those tennis balls and frisbee play time! "+ " (" + "Happiness " + "+" + str(happyincrease)+ ")"
                    em.set_footer(text=footertext)

                    updateJSON(users)
                    await message.channel.send(embed=em)
            else:
                desc = "Please wait ~2.5hrs"
                em = discord.Embed(title="<a:play:830190266584924181> Playing is on cooldown!",description=desc, color=0xe00034)
                await message.channel.send(embed=em)
        elif "botfeed" in message.content:
            global onfeedcd

            if onfeedcd == False:

                filesize = os.path.getsize("userids.txt")

                # Checks if there are no users
                if filesize == 0:
                    check = False
                else:
                    check = True


                if check == False:
                    em = discord.Embed(title="⛔ No Account Detected",description="Please register an account with `p.register`", color=0xe00034)
                    await message.channel.send(embed=em)
                    feed.reset_cooldown(ctx)
                else:

                    # Grab user INFO
                        # grab unique id
                    with open("userids.txt") as file:
                        mylist = file.read().splitlines()

                    userid = mylist[0]
                        # get information for users array from JSON file
                    users = getPlayerData()


                    # Check for pet death
                    if users[str(userid)]["death"] == True:
                        desc = "Your dog has passed away!" + " RIP:" + users[str(user.id)]["PetName"] + nl +  "Please use p.adopt (newpetname) to adopt a new dog"
                        em = discord.Embed(title=":skull_crossbones: You made an oopsie woopsie!" ,description = desc , color=0x949494)
                        await message.channel.send(embed=em)
                        return

                    # Start timer for light to turn on
                    threading.Timer(feedcooldown, light3On).start()
                    #  Set OnCooldown to true
                    onfeedcd = True



                    #SEND ARDUINO SERIAL MESSAGE FOR IMAGE PLAY
                    serport.write(b'feed')

                    petName = users[str(userid)]["PetName"]
                    petHealth = round(users[str(userid)]["health"],2)
                    petHappiness = users[str(userid)]["happiness"]


                    # Set up embded Message
                    em = discord.Embed(title="<:food:830168205154451456> You fed " + petName + "!"  ,description="", color=0x00de00)

                    if petHappiness > 50:

                        users[str(userid)]["health"] += random.randint(10,15)

                        happyincrease = random.randint(5,10)
                        users[str(userid)]["happiness"] += happyincrease

                        if users[str(userid)]["happiness"] > 100:
                            users[str(userid)]["happiness"] = 100

                        print("Health after " + str(users[str(userid)]["health"]))
                        round(users[str(userid)]["health"],2)
                        # If health is past 100, set it to 100

                        if (users[str(userid)]["health"] > 100):
                            users[str(userid)]["health"] = 100
                        # If happiness reaches over 100, put back down to 100
                            footertext = petName + "'s health is at 100!" + " (" + "Happiness " + "+" + str(happyincrease)+ ")"

                        else:
                            petHealth = round(users[str(userid)]["health"],2)
                            footertext = petName + "'s health is at " + str(petHealth) + " (" + "Happiness " + "+" + str(happyincrease)+ ")"


                    else:
                        chanceNoEat = random.randint(1,100)
                        print(chanceNoEat)
                        if chanceNoEat > 50:

                            users[str(userid)]["health"] += random.randint(10,15)

                            happyincrease = random.randint(5,10)
                            users[str(userid)]["happiness"] += happyincrease


                            print("Health after " + str(users[str(user.id)]["health"]))
                            round(users[str(userid)]["health"],2)
                            # If health is past 100, set it to 100

                            # If happiness reaches over 100, put back down to 100
                            # if users[str(user.id)]["happiness"] > 100:
                            #     users[str(user.id)]["happiness"] = 100


                            if (users[str(userid)]["health"] > 100):
                                users[str(userid)]["health"] = 100
                                footertext = petName + "'s health is at " + str(petHealth) + " (" + "Happiness " + "+" + str(happyincrease)+ ")"
                            else:
                                petHealth = round(users[str(userid)]["health"],2)
                                footertext = petName + "'s health is at " + str(petHealth) + " (" + "Happiness " + "+" + str(happyincrease)+ ")"
                        else:
                                em = discord.Embed(title="<:food:830168205154451456> You did not feed " + petName + "!"  ,description="", color=0x00de00)
                                footertext = petName + " chose not to eat because they're unhappy"

                    em.set_footer(text=footertext)

                    updateJSON(users)

                    await message.channel.send(embed=em)

            else:
                desc = "Please wait approx 5 hours"
                em = discord.Embed(title="<:food:830168205154451456> Feeding is on cooldown!",description=desc, color=0xe00034)
                await ctx.send(embed=em)



    await bot.process_commands(message)
    # await bot.process_commands(message)



# --------------------------------------------------------




bot.run('PUT YOUR BOT TOKEN HERE') #run the client using using bot's token

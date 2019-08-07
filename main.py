import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from random import randint
import requests
import json
import os
from ftplib import FTP
import json
#import sqlite3
import psycopg2
import random
import secrets
import inspect
import io
from datetime import datetime, date, time, timedelta
import pyspeedtest
from urllib.parse import urlparse
import pyping

url = "postgres://url" 

adminRoles = [566249728732561410, 605456866775924746] # Engineer , Staff
result = urlparse(url)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
db = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname
)
c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Users(
                      UserID BIGSERIAL,
                      Xp INTEGER,
                      Tokens INTEGER)""")

c.execute("""CREATE TABLE IF NOT EXISTS Ecopp(
                      UserID BIGSERIAL,
                      Boost BOOLEAN)""")

c.execute("""CREATE TABLE IF NOT EXISTS Activity(
                      UserID BIGSERIAL,
                      GlobalMessages INTEGER,
                      GlobalRank INTEGER,
                      WeeklyMessages INTEGER,
                      WeeklyRank INTEGER)""")

c.execute("""CREATE TABLE IF NOT EXISTS Tickets(
                      Number INTEGER)""")

# c.execute("""CREATE TABLE IF NOT EXISTS Tickets(
#                       Open INTEGER,
#                       Number INTEGER,
#                       )""")


spams = {}
re = []
bot = commands.Bot(command_prefix = "s!") #Initialise bot
bot.launch_time = datetime.utcnow()

ongoingraffle = False
embcolor=0x363942
email = ""
channelnumb = 0
bot_on = True
end = False
username = ""
ongoingpurge = False

bot.remove_command('help') #I have better things to do then make a help cmd


async def loop():
    while True:
        await bot.change_presence(game=discord.Game(name="s!help"), status='idle')
        await asyncio.sleep(15)
        await bot.change_presence(game=discord.Game(name="with the fate of the world"), status='idle')
        await asyncio.sleep(15)
        await bot.change_presence(game=discord.Game(name="with hosting"), status='idle')
        await asyncio.sleep(15)
        await bot.change_presence(game=discord.Game(name="Minecraft"), status='idle')
        await asyncio.sleep(15)
        await bot.change_presence(game=discord.Game(name=f"with {len(list(bot.get_all_members()))} users"), status='idle')
        await asyncio.sleep(15)

@bot.event
async def on_ready():
    print("Bot is online and connected to Discord")
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + bot.user.id)
    await loop()




@bot.command(pass_context=True)
async def specs(ctx):
    embed = discord.Embed(title = "Our Specifications", description="The specifications regarding our minecraft hosting servers", color=embcolor)
    embed.add_field(name = "Locations", value = "Free: Finland and Belgium\n Premium: UK, US and Germany", inline = False)
    embed.add_field(name = "CPUs", value = "Free: Core i7s (Extreme Edition)\n Premium:  Xeon E5 v4s", inline = False)
    embed.add_field(name = "RAM", value= "Free:  Unlimited. We have a flexible licensing agreement with our host so RAM is automatically upgraded if there's not enough.", inline = False)
    embed.add_field(name = "Storage", value= "All Tiers:  NVMe M.2 SSDs", inline = False)
    await bot.say("Currently Being Updated")



@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title = "What Information Do You Require?", description = "React with 💬 for a list of user commands, 💰 for a list of economy commands and 🛑 for a list of moderation commands", color=0x363942)
    startmsg = await bot.send_message(ctx.message.channel, embed=embed)
    #🏠
    await bot.add_reaction(startmsg, '💬')
    await bot.add_reaction(startmsg, '💰')
    await bot.add_reaction(startmsg, '🛑')
    while True:
        choice = await bot.wait_for_reaction(['💬', '💰', '🛑', '🏠', '❌'], message=startmsg)
        if choice.user == bot.user:
            pass
        else:
            if choice.reaction.emoji == '🏠':
                await bot.remove_reaction(startmsg, '🏠', ctx.message.author)
                await bot.remove_reaction(startmsg, '🏠', bot.user)
                embed = discord.Embed(title = "What Information Do You Require?", description = "React with 💬 for a list of user commands, 💰 for a list of economy commands and 🛑 for a list of moderation commands", color=0x363942)
                await bot.edit_message(startmsg, embed=embed)
                await bot.add_reaction(startmsg, '❌')
            if choice.reaction.emoji == '💬':
                await bot.remove_reaction(startmsg, '💬', choice.user)
                await bot.add_reaction(startmsg, '🏠')
                await bot.add_reaction(startmsg, '❌')
                with open("textfiles/usercmds.txt", "r") as txtfile:
                    content = txtfile.read()
                    embed = discord.Embed(title="Help - React with 🏠 to return to the main menu", description="`[] = Not Required Argument`, `<> = Required Argument`",color=0x363942)
                    embed.add_field(name="\u200b", value=f"{content}")
                    embed.set_footer(text=f"Requested by: {choice.user.display_name}", icon_url=choice.user.avatar_url)
                    await bot.edit_message(startmsg, embed=embed)
                    await bot.add_reaction(startmsg, '❌')
                    txtfile.close()
            if choice.reaction.emoji == '💰':
                await bot.remove_reaction(startmsg, '💰', choice.user)
                await bot.add_reaction(startmsg, '🏠')
                with open("textfiles/economy.txt", "r") as txtfile:
                    content = txtfile.read()
                    embed = discord.Embed(title="Help - React with 🏠 to return to the main menu", description="`[] = Not Required Argument`, `<> = Required Argument`",color=0x363942)
                    embed.add_field(name="\u200b", value=f"{content}")
                    embed.set_footer(text=f"Requested by: {choice.user.display_name}", icon_url=choice.user.avatar_url)
                    await bot.edit_message(startmsg, embed=embed)
                    await bot.add_reaction(startmsg, '❌')
                    txtfile.close()
            if choice.reaction.emoji == '🛑':
                await bot.remove_reaction(startmsg, '🛑', choice.user)
                await bot.add_reaction(startmsg, '🏠')
                with open("textfiles/moderation.txt", "r") as txtfile:
                    content = txtfile.read()
                    embed = discord.Embed(title="Help - React with 🏠 to return to the main menu", description="`[] = Not Required Argument`, `<> = Required Argument`",color=0x363942)
                    embed.add_field(name="\u200b", value=f"{content}")
                    embed.set_footer(text=f"Requested by: {choice.user.display_name}", icon_url=choice.user.avatar_url)
                    await bot.edit_message(startmsg, embed=embed)
                    await bot.add_reaction(startmsg, '❌')
                    txtfile.close()
            if choice.reaction.emoji == '❌':
                await bot.remove_reaction(startmsg, '❌', choice.user)
                await bot.delete_message(ctx.message)
                await bot.delete_message(startmsg)


@bot.command(pass_context=True)
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    create_economypp(member.id)
    checklevelup(member.id)
    xp = get_xp(member.id)
    tk = get_tk(member.id)
    lvl = get_lvl(member.id)
    booster = getbooster(member.id)
    #if tk <= 0:
        #set_xp(ctx.message.author.id, 0)
        #print("SET VALUE TO 0")
    if tk <= 0:
        set_tk(ctx.message.author.id, 0)
        print("SET VALUE TO 0")
    embed = discord.Embed(color=0x363942)
    embed.add_field(name="XP", value=f"{xp}", inline=False)
    embed.add_field(name="Sytes", value=f"${tk}", inline=False)
    embed.add_field(name="Level", value=f"{lvl}", inline=False)
    embed.add_field(name="Booster", value=f"{booster}", inline=False)
    embed.add_field(name="Joined server at", value=member.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
    embed.set_author(name=f"{member.display_name}'s profile.")
    embed.set_thumbnail(url=member.avatar_url)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def cat(ctx):
        print("Here!")
        cat = requests.get('https://some-random-api.ml/img/cat')
        print("Here!")
        info = cat.json()
        embed = discord.Embed(color=0x363942)
        embed.set_image(url=f"{info['link']}")
        print("Here!")
        react = await bot.say(embed=embed)
        await bot.add_reaction(react, '🐱')
        while True:
            repeat = await bot.wait_for_reaction(emoji='🐱', message=react)
            if repeat.user == bot.user:
                pass
            else:
                await bot.remove_reaction(react, '🐱', repeat.user)
                cat = requests.get('https://some-random-api.ml/img/cat')
                info = cat.json()
                embed = discord.Embed(color=0x363942)
                embed.set_image(url=f"{info['link']}")
                await bot.edit_message(react, embed=embed)

@bot.command(pass_context=True)
async def dog(ctx):
    response = requests.get('https://some-random-api.ml/img/dog')
    data = response.json()
    embed = discord.Embed(color=0x363942)
    embed.set_image(url=f"{data['link']}")
    react = await bot.say(embed=embed)
    await bot.add_reaction(react, '🐶')
    while True:
        repeat = await bot.wait_for_reaction(emoji='🐶', message=react)
        if repeat.user == bot.user:
            pass
        else:
            await bot.remove_reaction(react, '🐶', repeat.user)
            response = requests.get('https://some-random-api.ml/img/dog')
            data = response.json()
            embed = discord.Embed(color=0x363942)
            embed.set_image(url=f"{data['link']}")
            await bot.edit_message(react, embed=embed)

@bot.command(pass_context=True)
async def pay(ctx, member: discord.Member = None, amount: int = None):
    if member == None:
        await bot.say(":x: Please specify a member to pay")
    if amount == None or amount == 0:
        await bot.say(":x: Please specify an amount to pay")
    else:
        rxp = get_tk(ctx.message.author.id)
        #dxp = get_xp(member.id)
        if rxp < amount:
            await bot.say(":x: You don't have enough funds to send to this player, please try a smaller amount.")
        else:
            add_tk(member.id, amount)
            remove_tk(ctx.message.author.id, amount)
            await bot.say(f"You have just payed {member.display_name}, {amount}$")

@bot.command(pass_context=True)
async def sql(ctx, cmd: str = None):
    if ctx.message.author.id == '279714095480176642':
        c.execute(f"{cmd}")
        db.commit()
        await bot.say(f"Executed the SQL command:\n ```{cmd}```.")
    else:
        await bot.say(":x: No, Just no")

@bot.command(pass_context=True)
async def serverinfo(ctx):
    server = ctx.message.server
    owner = server.owner
    ownername = owner.display_name
    embed = discord.Embed(title = f"Information On {server.name}", description = "", color=0x363942)
    embed.add_field(name="Server ID:", value=f"{server.id}", inline=False)
    embed.add_field(name="Server Members:", value=f"{server.member_count}")
    embed.add_field(name="Owner:", value=f"{ownername}", inline=False)
    embed.add_field(name="Region:", value=f"{server.region}", inline=False)
    embed.add_field(name="Verification Level:", value=f"{server.verification_level}", inline=False)
    embed.add_field(name="Server Created At:", value=f"{server.created_at}", inline=False)
    #embed.add_field(name="", value="", inline=False)
    embed.set_thumbnail(url=server.icon_url)
    await bot.say(embed=embed)




@bot.command(pass_context=True)
async def rulessetup(ctx):
    if ctx.message.author.id == '232888536574066688':
        #embedme.add_field(na="", value="")
        lowsev = discord.Embed(color =0x00FF00, title = "Low Severity [Warn]")
        lowsev.add_field(name="Use english in all channels unless stated otherwise.", value="Makes it easier for staff to moderate chat.", inline=False)
        lowsev.add_field(name="Don't be annoying.", value="Includes minimoding and treating other users/staff unniceley.", inline=False)
        lowsev.add_field(name="Don't undo what a staff member has done.", value="Name changes, etc.", inline=False)
        lowsev.add_field(name="False/ Spam pings.", value="Like ghost pinging, pinging staff for your message, etc.", inline=False)
        lowsev.add_field(name="Spamming of any sort.", value="Includes Character Spam, Flooding Chat, Emoji Spam, Reaction Spam and ASCII text.", inline=False)
        lowsev.add_field(name="Attempting to name hoist.", value="Adding `!` or another character to make your name at the top of the list.", inline=False)
        medsev = discord.Embed(color =0xffa500, title = "Medium Severity [Kick and or Ban]")
        medsev.add_field(name="Advertising of any sort.", value="Servers (Inc DM), Products, etc.", inline=False)
        medsev.add_field(name="Selfbotting.", value="Its against the TOS don't do it.", inline=False)
        medsev.add_field(name="Sharing of illegal or false information.", value="Untrue Rumors, etc.", inline=False)
        medsev.add_field(name="Being offensive to staff.", value="Saltyness, Offensive memes, etc.", inline=False)
        maxserv = discord.Embed(color =0xff0000, title = "High serverity [Permanent Ban]")
        maxserv.add_field(name="Sending NSFW.", value="Porn, Hentai, etc.", inline=False)
        maxserv.add_field(name="Alts.", value="We don't know what you do with them.", inline=False)
        maxserv.add_field(name="DDos/Dox/Death Threats.", value="Its uneeded and wrong.", inline=False)
        maxserv.add_field(name="Sending files or programs that can damage another user's device.", value="Viruses, Trojans, Adware, etc.", inline=False)
        maxserv.add_field(name="Raiding.", value="Ban and report to discord's trust and saftey team.", inline=False)
        maxserv.add_field(name="Racism, Homofobia.", value="We **must** respect everyone independent of race, sexuality or country of residance.", inline=False)
        await bot.say(embed=lowsev)
        await bot.say(embed=medsev)
        await bot.say(embed=maxserv)
    else:
        await bot.say("no. just no")


@bot.command(pass_context=True)
async def weekly_reset(ctx):
    if [role.id for role in ctx.message.author.roles] in adminRoles:
        for x in ctx.message.server.members:
            uid = x.id
            reset_weeklymessages(uid)
            print(f"[Activity] Reset weekly for {uid}")
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    embed = discord.Embed(color=embcolor)
    embed.add_field(name="Our bot's uptime :calendar_spiral:", value=f"Weeks: **{weeks}**\nDays: **{days}**\nHours: **{hours}**\nMinutes: **{minutes}**\nSeconds: **{seconds}**")
    await bot.say(embed=embed)



@bot.command(pass_context=True)
async def pfp(ctx, member: discord.Member):
    if member == None:
        member = ctx.message.author
    embed=discord.Embed(title="The user's profile picture.", color=0x363942)
    embed.set_image(url=member.avatar_url)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def purge(ctx, number):
    if [role.id for role in ctx.message.author.roles] in adminRoles:
        ongoingpurge = True
        msgs = []
        number = int(number)
        async for x in bot.logs_from(ctx.message.channel, limit = number):
            msgs.append(x)
        await bot.delete_messages(msgs)
        embed = discord.Embed(title=f"A message purge has occurred!", description="Everything is nice and clean now!", color=0x363942)
        embed.add_field(name=":recycle: Number of messages purged:", value=f"{number}", inline=False)
        embed.add_field(name=":closed_lock_with_key: Moderator:", value=ctx.message.author.display_name, inline=False)
        embed.set_thumbnail(url="https://www.allaboutlean.com/wp-content/uploads/2015/03/Broom-Icon.png")
        await bot.send_message(bot.get_channel('565201713951145994'), embed=embed)#log
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))


        # @bot.command(pass_context=True)
        # async def eme(ctx):
        #     if [role.id for role in ctx.message.author.roles] in adminRoles:
        #         for channel in ctx.message.server.channels:
        #                 staff = discord.utils.get(ctx.message.author.server.roles, name="🔨 Staff")
        #                 verified = discord.utils.get(ctx.message.author.server.roles, name="👥 Verified")
        #                 everyone = ctx.message.author.server.default_role
        #                 #everyone = discord.utils.get(user.server.roles, name="everyone")
        #                 disallow = discord.PermissionOverwrite()
        #                 disallow.read_messages = False
        #                 disallow.send_messages = False
        #                 allow = discord.PermissionOverwrite()
        #                 allow.read_messages = True
        #                 allow.send_messages = True
        #                 await bot.edit_channel_permissions(channel, verified, disallow)
        #                 await bot.edit_channel_permissions(channel, everyone, dissallow)
        #                 #await bot.edit_channel_permissions(channel, everyone, disallow)
        #                 await bot.edit_channel_permissions(channel, staff, allow)
        #     else:
        #         pass

        # @bot.command(pass_context=True)
        # async def unlock(ctx):
        #     if [role.id for role in ctx.message.author.roles] in adminRoles:
        #         staff = discord.utils.get(ctx.message.author.server.roles, name="🔨 Staff")
        #         verified = discord.utils.get(ctx.message.author.server.roles, name="👥 Verified")
        #         everyone = ctx.message.author.server.default_role
        #         #everyone = discord.utils.get(user.server.roles, name="everyone")
        #         disallow = discord.PermissionOverwrite()
        #         disallow.read_messages = False
        #         disallow.send_messages = False
        #         allow = discord.PermissionOverwrite()
        #         allow.read_messages = True
        #         allow.send_messages = True
        #         await bot.edit_channel_permissions(channel, verified, disallow)
        #         await bot.edit_channel_permissions(channel, everyone, dissallow)
        #         #await bot.edit_channel_permissions(channel, everyone, disallow)
        #         await bot.edit_channel_permissions(channel, staff, allow)
        #     else:
        #         pass


@bot.command(pass_context=True)
async def checkuser(ctx, user: discord.Member=None):
    if [role.id for role in ctx.message.author.roles] in adminRoles:
        if user is None:
            user = ctx.message.author
        accage = datetime.utcnow() - user.created_at
        postaccage = int(accage.days)
        embed = discord.Embed(color=0x363942)
        embed.set_author(name=user.display_name)
        embed.add_field(name=":desktop: ID:", value=user.id, inline=False)
        embed.add_field(name=":satellite: Status:", value=user.status, inline=False)
        embed.add_field(name=":star2: Joined server::", value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        embed.add_field(name=":date: Created account:", value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        embed.add_field(name=":bust_in_silhouette: Nickname:", value=user.display_name, inline=False)
        embed.add_field(name=":robot: Is Bot:", value=user.bot, inline=False)
        embed.add_field(name=':ballot_box_with_check: Top role:', value=user.top_role.name, inline=False)
        embed.add_field(name=':video_game: Playing:', value=user.game, inline=False)
        embed.add_field(name=':video_game: Account Age:', value=f"{postaccage} Days", inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        await bot.say(embed=embed)
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))


@bot.command(pass_context=True)
async def genpw(ctx):
    pw = secrets.token_urlsafe(5)
    await bot.send_typing(ctx.message.author)
    await bot.send_message(ctx.message.author, f"Your generated password is `{pw}`, this password is secure and hasn't been shared with anybody else")

@bot.command(pass_context=True)
async def setpfp(ctx):
    if ctx.message.author.id == '279714095480176642':
        await bot.delete_message(ctx.message)
        png = open('sytespace.jpg', 'rb')
        avatar = png.read()
        await bot.edit_profile(avatar = avatar)
    else:
        pass

@bot.command(pass_context=True)
async def shop(ctx):
    embed = discord.Embed(title = "Currently avalible shop items:", description = "You can buy any item by doing `s!buy <itemnumber>`. **All Prices are in Sytes**", color=0x363942)
    tk = get_tk(ctx.message.author.id)
    embed.add_field(name="**`1.` One Week Of SyteSpace premium** - 200$", value="This is the best way to try out our services full abilities.", inline=False)
    embed.add_field(name="**`2.` Custom Role for one week** - 150$", value="Show your freinds how cool you are with your very own elevated custom role.", inline=False)
    embed.add_field(name="**`3.` Long Live Summer Role** - 100$", value="Summer event role, limited time only", inline=False)
    embed.add_field(name="**`4.` Syte Booster (Permanent)** - 400$", value="This makes your chances of gaining sytes 50/50 (per message) and you also gain up to 5 sytes per message.", inline=False)
    embed.set_footer(text=f"You currently have {tk} Sytes", icon_url="https://assets.syte.space/assets/sytespace_bg.jpg")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def buy(ctx, itemnumber: int = None):
    if itemnumber == None:
        await bot.say(":x: Please specify a valid item number")
    else:
        if itemnumber == 1:
            tk = int(get_tk(ctx.message.author.id))
            itemprice = 200
            itemname = "One Week Of SyteSpace premium"
            seccode = secrets.token_urlsafe(16)
            if tk < itemprice:
                await bot.say(f":x: You don't have sufficent funds to buy that item (You are missing `{itemprice - tk}` Sytes)")
            else:
                await bot.delete_message(ctx.message)
                newtk = remove_tk(ctx.message.author.id, itemprice)
                embed = discord.Embed(title = "Purchase Confirmed", description=f"Your purchase of {itemname} has been confirmed, you now have {newtk} Sytes, a staff member will contact you shortly regarding your purchase")
                stafflog = discord.Embed(title = "A new store purchase has been made.")
                stafflog.add_field(name="Discord Name", value=f"{ctx.message.author.display_name}")
                stafflog.add_field(name="Discord ID", value=f"{ctx.message.author.id}")
                stafflog.add_field(name="Item Name", value=f"{itemname}")
                stafflog.add_field(name="Item Number", value=f"{itemnumber}")
                stafflog.add_field(name="Security Code", value=f"{seccode}")
                await bot.send_message(ctx.message.author, embed=embed)
                await bot.send_message(bot.get_channel('564113712580132866'), embed=stafflog)
        elif itemnumber == 2:
            await bot.say(":x: Item is not avalible yet.")
        elif itemnumber == 3:
            tk = int(get_tk(ctx.message.author.id))
            itemprice = 100
            itemname = "Long Live Summer Role"
            if tk < itemprice:
                await bot.say(f":x: You don't have sufficent funds to buy that item (You are missing `{itemprice - tk}` Sytes)")
            else:
                await bot.delete_message(ctx.message)
                newtk = remove_tk(ctx.message.author.id, itemprice)
                ecowarrior = discord.utils.get(ctx.message.server.roles, name="🍉 Long Live Summer")
                await bot.add_roles(ctx.message.author, ecowarrior)
                embed = discord.Embed(title = "Purchase Confirmed", description=f"Your purchase of {itemname} has been confirmed, you now have {newtk} Sytes, the role has now been added to you")
                stafflog = discord.Embed(title = "A new store purchase has been made.")
                stafflog.add_field(name="Discord Name", value=f"{ctx.message.author.display_name}")
                stafflog.add_field(name="Discord ID", value=f"{ctx.message.author.id}")
                stafflog.add_field(name="Item Name", value=f"{itemname}")
                stafflog.add_field(name="Item Number", value=f"{itemnumber}")
                await bot.send_message(ctx.message.author, embed=embed)
                await bot.send_message(bot.get_channel('564113712580132866'), embed=stafflog)
        elif itemnumber == 4:
            tk = int(get_tk(ctx.message.author.id))
            itemprice = 200
            itemname = "Syte Booster"
            seccode = secrets.token_urlsafe(16)
            if tk < itemprice:
                await bot.say(f":x: You don't have sufficent funds to buy that item (You are missing `{itemprice - tk}` Sytes)")
            else:
                await bot.delete_message(ctx.message)
                newtk = remove_tk(ctx.message.author.id, itemprice)
                setbooster(ctx.message.author.id, True)
                embed = discord.Embed(title = "Purchase Confirmed", description=f"Your purchase of {itemname} has been confirmed, you now have {newtk} Sytes, the booster has now been applied!")
                embed.set_footer(text=f"Security token: {seccode}")
                stafflog = discord.Embed(title = "A new store purchase has been made.")
                stafflog.add_field(name="Discord Name", value=f"{ctx.message.author.display_name}")
                stafflog.add_field(name="Discord ID", value=f"{ctx.message.author.id}")
                stafflog.add_field(name="Item Name", value=f"{itemname}")
                stafflog.add_field(name="Item Number", value=f"{itemnumber}")
                stafflog.add_field(name="Security Code", value=f"{seccode}")
                await bot.send_message(ctx.message.author, embed=embed)
                await bot.send_message(bot.get_channel('564113712580132866'), embed=stafflog)
        else:
            await bot.say(":x: That item isn't in our database please input a valid item code")

@bot.command(pass_context=True)
async def punish(ctx, member: discord.Member = None, *, reason: str = None):
    if [role.id for role in ctx.message.author.roles] in adminRoles:
        if reason == None:
            await bot.say(":x: Please Specify A Reason")
        elif member == None:
            await bot.say(":x: Please Specify A Member")
        else:
            embed = discord.Embed(title=f"What action do you wish to take against {member.display_name}?", description="React with 🔨 to **ban** the user, with 👢 to **kick** and 🛑 to **warn**", color = embcolor)
            msg = await bot.send_message(ctx.message.author, embed=embed)
            await bot.add_reaction(msg, '🔨')
            await bot.add_reaction(msg, '👢')
            await bot.add_reaction(msg, '🛑')
            while True:
                res = await bot.wait_for_reaction(['🔨', '👢', '🛑'], message=msg)
                if res.user == bot.user:
                    pass
                else:
                    if res.reaction.emoji == '🔨':
                        try:
                            await bot.delete_message(ctx.message)
                            await bot.delete_message(msg)
                            embed = discord.Embed(title = "You have been banned from `SyteSpace`!", description = "Details about the ban:", color =0x363942)
                            embed.add_field(name = ":closed_lock_with_key: Moderator:", value = ctx.message.author.display_name)
                            embed.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
                            embed.set_thumbnail(url=member.avatar_url)
                            await bot.send_message(member, embed=embed)
                            emb = discord.Embed(title = "Ban Issued!", description = "Details about the ban:", color =0x363942)
                            emb.add_field(name = "Moderator:", value = f"{ctx.message.author.display_name}")
                            emb.add_field(name = ":spy: member Banned:", value = f"{member.name}")
                            emb.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
                            emb.set_thumbnail(url=member.avatar_url)
                            await bot.send_message(bot.get_channel('565201713951145994'), embed=emb)
                            await bot.ban(member)
                        except discord.errors.Forbidden:
                            emb = discord.Embed(title = "Ban Issued!", description = "Details about the ban:", color =0x363942)
                            emb.add_field(name = "Moderator:", value = f"{ctx.message.author.display_name}")
                            emb.add_field(name = ":spy: member Banned:", value = f"{member.name}")
                            emb.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
                            emb.set_thumbnail(url=member.avatar_url)
                            await bot.send_message(bot.get_channel('565201713951145994'), embed=emb)
                            await bot.ban(member)
                    if res.reaction.emoji == '👢':
                        await bot.delete_message(ctx.message)
                        await bot.delete_message(msg)
                        embed = discord.Embed(color =0x363942, title="You have been kicked from `SyteSpace`!")
                        embed.set_thumbnail(url=member.avatar_url)
                        embed.add_field(name=":notepad_spiral: Reason:", value=f"{reason}")
                        embed.add_field(name="Moderator:", value=ctx.message.author.display_name)
                        emb = discord.Embed(color =0x363942, title="A kick has been issued")
                        emb.add_field(name=":notepad_spiral: Reason:", value=f"{reason}")
                        emb.add_field(name="Moderator:", value=ctx.message.author.display_name)
                        emb.add_field(name=":spy: User Kicked:", value=f"{member.name}")
                        emb.set_thumbnail(url=member.avatar_url)
                        await bot.send_message(member, embed=embed)
                        await bot.send_message(bot.get_channel('565201713951145994'), embed=emb)
                        await bot.kick(member)
                    if res.reaction.emoji == '🛑':
                        await bot.delete_message(ctx.message)
                        await bot.delete_message(msg)
                        embed = discord.Embed(title = "You have been warned in `SyteSpace`!", description = "Details about the warn:", color =0x363942)
                        embed.add_field(name = ":closed_lock_with_key: Moderator:", value = ctx.message.author.display_name)
                        embed.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
                        embed.set_thumbnail(url=member.avatar_url)
                        await bot.send_message(member, embed=embed)# DM it!
                        emb = discord.Embed(title = "Warn Issued!", description = "Details about the warn:", color =0x363942)
                        emb.add_field(name = "Moderator:", value = f"{ctx.message.author.display_name}")
                        emb.add_field(name = ":spy: member Warned:", value = f"{member.name}")
                        emb.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
                        emb.set_thumbnail(url=member.avatar_url)
                        await bot.send_message(bot.get_channel('565201713951145994'), embed=emb)#log it!
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))


@bot.command(pass_context=True)
async def ping(ctx):
    st = pyspeedtest.SpeedTest()
    google_req = pyping.ping('8.8.8.8')
    cloudflare_req = pyping.ping('1.1.1.1')  
    discord_req = pyping.ping('gateway.discord.gg')
    google = str(google_req.avg_rtt)
    cloudflare = str(cloudflare_req.avg_rtt)
    discord_ping = str(discord_req.avg_rtt)
    ping = str(int(round(st.ping(), 0)))
    down = round((st.download()/1000000), 2)
    up = round((st.upload()/1000000), 2)
    host = str(st.host)
    now = datetime.utcnow()
    old_message = now - ctx.message.timestamp
    old_delta = old_message.microseconds
    milsec_old = int(old_delta // 1000)
    embed = discord.Embed(title="Connection Statistics", description="Current Connection Statistics", color=0x363942)
    embed.add_field(name="Ping (st)", value="`%sms`" % ping, inline=False)
    embed.add_field(name="Ping (disc)", value="`%sms`" % discord_ping, inline=False)
    embed.add_field(name="Server Used", value="`%s`" % host, inline=False)
    embed.add_field(name="Download", value="`%s mbps`" % down, inline=False)
    embed.add_field(name="Upload", value="`%s mbps`" % up, inline=False)
    embed.set_footer(text=f"Requested by: {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
    emb = discord.Embed(title="Connection Statistics [2]", description="Statistics to pings for other services", color=0x363942)
    emb.add_field(name="Google", value="`%sms`" % google, inline=False)
    emb.add_field(name="Cloudflare", value="`%sms`" % cloudflare, inline=False)
    emb.add_field(name="Discord (time module)", value="`%sms`" % milsec_old, inline=False)
    emb.set_footer(text=f"Requested by: {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)
    await bot.say(embed=emb)

@bot.command(pass_context=True)
async def new(ctx, subject=""):
    ticknumb = 0
    numb = ticknumb + 1
    ticknumb = numb
    createchannel = await bot.create_channel(ctx.message.author.server, f"ticket-{numb}")
    embed = discord.Embed(title = f"New ticket created, Regarding {subject}", description = f"Hello {ctx.message.author.display_name}, thanks for reaching out to our support team, a member of staff will be with you as soon as possible.", color=0x363942)
    embed.set_footer(text=f"Ticket number: {createchannel.id}", icon_url=ctx.message.author.avatar_url)
    staff = discord.utils.get(ctx.message.author.server.roles, name="🔨 Staff")
    guest = discord.utils.get(ctx.message.author.server.roles, name="👤 Guest")
    client = discord.utils.get(ctx.message.author.server.roles, name="❤ Client")
    everyone = ctx.message.author.server.default_role
    #everyone = discord.utils.get(user.server.roles, name="everyone")
    disallow = discord.PermissionOverwrite()
    disallow.read_messages = False
    disallow.send_messages = False
    allow = discord.PermissionOverwrite()
    allow.read_messages = True
    allow.send_messages = True
    await bot.edit_channel_permissions(createchannel, guest, disallow)
    await bot.edit_channel_permissions(createchannel, everyone, disallow)
    await bot.edit_channel_permissions(createchannel, client, disallow)
    #await bot.edit_channel_permissions(createchannel, everyone, disallow)
    await bot.edit_channel_permissions(createchannel, ctx.message.author, allow)
    await bot.edit_channel_permissions(createchannel, staff, allow)
    await bot.send_message(createchannel, embed=embed)


@bot.command(pass_context=True)
async def skin(ctx, username = ""):
        uid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        data = uid.json()
        uid = f"{data['id']} "
        embed = discord.Embed(color=0x363942)
        embed.set_image(url=f"https://crafatar.com/renders/body/{uid}.png")
        await bot.say(embed=embed)


@bot.command(pass_context=True)
async def setup(ctx):
    if [role.id for role in ctx.message.author.roles] in adminRoles:
        print("Here!")
        #print("Set up!")
        msgs = []
        number = 100
        async for x in bot.logs_from(ctx.message.channel, limit = number):
            msgs.append(x)
        await bot.delete_messages(msgs)
        embed = discord.Embed(title = "**Let's get started!**", description="React to this message with :punch: to start the process of ordering your free unlimited Minecraft hosting.", color=0x363942)
        message = await bot.send_message(bot.get_channel('551800531358580736'), embed=embed)
        await bot.add_reaction(message, '👊')
        #embed = discord.Embed(title="Service Currently Down", description="Due to the discovery of a zeroday exploit in our server inferstructure we are currently **not accepting** server requests and all existing servers are down until further notice\n\n Apologies for the inconvinence\n The syte.space team.", color=0xff0000)
        #down = await bot.say(embed=embed)
        #await bot.add_reaction(down, '❌')
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def reboot(ctx):
    if not ctx.message.author.id == '279714095480176642':
        return await bot.say(":x: You **must** be the bot owner")
    await bot.logout()

@bot.command(pass_context=True)
async def weekly(ctx):
    first = f"<@{get_user_rank(1)}>"
    second = f"<@{get_user_rank(2)}>"
    third = f"<@{get_user_rank(3)}>"
    fourth = f"<@{get_user_rank(4)}>"
    fifth = f"<@{get_user_rank(5)}>"
    embed = discord.Embed(title="Weekly Leaderboard", description=f"#1 - {first}\n#2 - {second}\n#3 - {third}\n#4 - {fourth}\n#5 - {fifth}", color=0x363942)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def addguest(ctx):
    if [role.id for role in ctx.message.author.roles] in adminRoles:
        ecowarrior = discord.utils.get(ctx.message.server.roles, name="👋 Guest")
        for member in ctx.message.server.members:
            await bot.add_roles(member, ecowarrior)
    else:
        pass


@bot.command(pass_context=True)
async def statmod(ctx, member: discord.Member = None, amount: int = None):
    if [role.id for role in ctx.message.author.roles] in adminRoles:
        embed = discord.Embed(title=f"What aspect of {member.display_name}'s stats do you wish to change?'", description="React with 📕 to change XP and 📙 to change Sytes and 📗 to toggle booster", color=embcolor)
        wchange = await bot.send_message(ctx.message.channel, embed=embed)
        await bot.add_reaction(wchange, '📕')
        await bot.add_reaction(wchange, '📙')
        await bot.add_reaction(wchange, '📗')
        while True:
            wchanger = await bot.wait_for_reaction(['📕', '📙', '📗'], message=wchange)
            if wchanger.user == bot.user:
                print("Here")
                pass
            else:
                if wchanger.reaction.emoji == '📕':
                    await bot.remove_reaction(wchange, '📕', wchanger.user)
                    embed = discord.Embed(title=f"What sort of change do you wish to make to {member.display_name}'s stats?", description=f"React with to ➖ subtract {amount} XP or with ➕ to add {amount} XP to {member.display_name}'s stats.", color=embcolor)
                    pmmsg = await bot.send_message(ctx.message.channel, embed=embed)
                    await bot.add_reaction(pmmsg, '➕')
                    await bot.add_reaction(pmmsg, '➖')
                    while True:
                        plusminus = await bot.wait_for_reaction(['➕','➖'], message=pmmsg)
                        if plusminus.user == bot.user:
                            pass
                        if plusminus.user != ctx.message.author:
                            pass
                        else:
                            if plusminus.reaction.emoji == '➕':
                                add_xp(member.id, amount)
                                await bot.say(f"Added {amount} to {member.display_name}'s stats")
                            if plusminus.reaction.emoji == '➖':
                                remove_xp(member.id, amount)
                                await bot.say(f"Removed {amount} to {member.display_name}'s stats")
                if wchanger.reaction.emoji == '📙':
                    await bot.remove_reaction(wchange, '📙', wchanger.user)
                    embed = discord.Embed(title=f"What sort of change do you wish to make to {member.display_name}'s stats?", description=f"React with to ➖ subtract {amount} Sytes with ➕ to add {amount} Sytes to {member.display_name}'s stats.", color=embcolor)
                    pmmsg = await bot.send_message(ctx.message.channel, embed=embed)
                    await bot.add_reaction(pmmsg, '➕')
                    await bot.add_reaction(pmmsg, '➖')
                    while True:
                        plusminus = await bot.wait_for_reaction(['➕','➖'], message=pmmsg)
                        if plusminus.user == bot.user:
                            pass
                        if plusminus.user != ctx.message.author:
                            pass
                        else:
                            if plusminus.reaction.emoji == '➕':
                                add_tk(member.id, amount)
                                await bot.say(f"Added {amount} Sytes to {member.display_name}'s stats")
                            if plusminus.reaction.emoji == '➖':
                                remove_tk(member.id, amount)
                                await bot.say(f"Removed {amount} Sytes to {member.display_name}'s stats")
                if wchanger.reaction.emoji == '📗':
                    await bot.remove_reaction(wchange, '📗', wchanger.user)
                    boost = getbooster(member.id)
                    if boost == False:
                        setbooster(member.id, True)
                        await bot.say(f"Set {member.display_name}'s booster status to True")
                    if boost == True:
                        setbooster(member.id, True)
                        await bot.say(f"Set {member.display_name}'s booster status to False")
    else:
        await bot.say(":x: Staff only command")

@bot.command(pass_context=True)
async def close(ctx):
    embed = discord.Embed(title = "Are you sure you want to delete this ticket?", description = "React with :x: to confirm", color=0x363942)
    confirmmsg = await bot.say(embed=embed)
    await bot.add_reaction(confirmmsg, '❌')
    confirm = await bot.wait_for_reaction('❌', message=confirmmsg)
    if confirm.user == bot.user:
        pass
    #await bot.remove_reaction(confirmmsg, '❌', ctx.message.author)
    else:
        await bot.delete_channel(ctx.message.channel)

#@bot.command(pass_context=True)
#async def hello(ctx):
    #<#551800531358580736>
    #embed = discord.Embed(title = "Why, hello there! Thanks for joining us. This is the SyteSpace Discord server.", description = "Please be mindful and respect other members of the server, this means no spamming, rudeness, all that. Hopefully we don't need a set of rules because everyone in here is mature, but that can still change. Just don't be annoying.\n\n Oh, there's one more guideline which I'm hoping you can abide to, only 1 server is allowed per person so please don't go around in alt accounts and getting more than one server. If found to be doing this, both accounts will immediately be banned from the service. It's not worth it.\n\n Anyway, assuming you've set off on the right track, I'll bet you $10 that you're here to get a free Minecraft server. Oh, you are? You might want to give me my money then. Nah, only joking. We provide everyone with a completely free Minecraft server with unlimited RAM/memory, storage, bandwidth and processing power. How good is that? You can get it in around 30 seconds by following the instructions in <#551800531358580736>.\n\n You can purchase an upgrade in order to get dedicated resources to your server, that's available over at <#550958398410194974>. It only costs a few bucks a month, so we'd certainly recommend it.\n\n I think that's about all from me, if you require any assistance please speak to a member of staff or visit one of our offices. Alternatively, you could open a ticket in <#551800531358580736> and react with the :speech_balloon: emoji - a member of staff will get to you right away.\n\n Welp, I guess that's goodbye. See you around, and enjoy yourself!", color=0x363942)
    #embed.set_thumbnail(url="https://assets.syte.space/assets/sytespace_bg.jpg")
    #await bot.say(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(ctx, discord.ext.commands.errors.CommandNotFound):
        await bot.add_reaction(error.message, '❌')
    else:
        await bot.add_reaction(error.message, '🔎')
        raise ctx


#db.commit()
def checklevelup(uid: str):
    currentlvl = get_lvl(uid)
    currentxp = get_xp(uid)
    if currentxp >= 10000:
        if currentlvl != 10:
            set_lvl(uid, 10)
        else:
            pass
    if currentxp >= 20000:
        if currentlvl !=20:
            set_lvl(uid, 10)
        else:
            pass

def create_user_if_not_exists(user_id: str):
    c.execute("SELECT COUNT(*) FROM Users WHERE UserID=%s", (str(user_id),))
    user_count = c.fetchone()[0]
    if user_count < 1:
        print("[Users Table]Creating user with id " + str(user_id))
        c.execute("INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)", (str(user_id), 0, 0, 0, 0, 0))
        db.commit()

def create_economypp(user_id: str):
    c.execute("SELECT COUNT(*) FROM Ecopp WHERE UserID=%s", (str(user_id),))
    verif = c.fetchone()[0]
    if verif < 1:
        print("[Economy++] Creating user with id " + str(user_id))
        c.execute("INSERT INTO Ecopp VALUES (%s, %s)", (str(user_id), False))
        db.commit()

def create_activity(user_id: str):
    c.execute("SELECT COUNT(*) FROM Activity WHERE UserID=%s", (str(user_id),))
    verif = c.fetchone()[0]
    if verif < 1:
        print("[Activity] Creating user with id " + str(user_id))
        c.execute("INSERT INTO Activity VALUES (%s, %s, %s, %s, %s)", (str(user_id), 0, 0, 0, 0))
        db.commit()

def set_lvl(user_id, amount: int):
    lvl = amount
    c.execute("UPDATE Users SET Level=%s WHERE UserID=%s", (lvl, str(user_id)))
    db.commit()
    return lvl

def get_lvl(user_id: str):
    create_user_if_not_exists(user_id)
    create_economypp(user_id)
    c.execute("SELECT Level FROM Users WHERE UserID=%s", (str(user_id),))
    user_lvl = int(c.fetchone()[0])
    db.commit()
    return user_lvl

def setbooster(user_id: str, setto = bool):
    c.execute("UPDATE Ecopp SET Boost=%s WHERE UserID=%s", (bool(setto), str(user_id)))
    db.commit()

def getbooster(user_id: str):
    c.execute("SELECT Boost FROM Ecopp WHERE UserID=%s", (str(user_id),))
    booster = bool(c.fetchone()[0])
    db.commit()
    return booster

def get_xp(user_id: str):
    create_user_if_not_exists(user_id)
    create_economypp(user_id)
    c.execute("SELECT Xp FROM Users WHERE UserID=%s", (str(user_id),))
    user_xp = int(c.fetchone()[0])
    db.commit()
    return user_xp


def add_xp(user_id, amount: int):
    xp = int(get_xp(user_id) + amount)
    c.execute("UPDATE Users SET Xp=%s WHERE UserID=%s", (xp, str(user_id)))
    db.commit()
    return xp

def remove_xp(user_id, amount: int):
    xp = int(get_xp(user_id) - amount)
    c.execute("UPDATE Users SET Xp=%s WHERE UserID=%s", (xp, str(user_id)))
    db.commit()
    return xp

def get_tk(user_id: str):
    create_user_if_not_exists(user_id)
    create_economypp(user_id)
    c.execute("SELECT Tokens FROM Users WHERE UserID=%s", (str(user_id),))
    user_tk = int(c.fetchone()[0])
    db.commit()
    return user_tk


def add_tk(user_id, amount: int):
    tk = int(get_tk(user_id) + amount)
    create_economypp(user_id)
    c.execute("UPDATE Users SET Tokens=%s WHERE UserID=%s", (tk, str(user_id)))
    db.commit()
    return tk

def remove_tk(user_id, amount: int):
    tk = int(get_tk(user_id) - amount)
    c.execute("UPDATE Users SET Tokens=%s WHERE UserID=%s", (tk, str(user_id)))
    db.commit()
    return tk

def set_tk(user_id, amount: int):
    tk = amount
    c.execute("UPDATE Users SET Tokens=%s WHERE UserID=%s", (tk, str(user_id)))
    db.commit()
    return tk

def get_globalmessages(user_id: str):
    create_activity(user_id)
    c.execute("SELECT GlobalMessages FROM Activity WHERE UserID=%s", (str(user_id),))
    user_globalmessages = int(c.fetchone()[0])
    db.commit()
    return user_globalmessages

def get_weeklymessages(user_id: str):
    create_activity(user_id)
    c.execute("SELECT WeeklyMessages FROM Activity WHERE UserID=%s", (str(user_id),))
    user_weeklymessages = int(c.fetchone()[0])
    db.commit()
    return user_weeklymessages

def reset_weeklymessages(user_id: str):
    create_activity(user_id)
    c.execute("UPDATE Activity SET WeeklyMessages=%s WHERE UserID=%s", (0, str(user_id)))
    db.commit()
    return True

def set_weekly_rank(user_id, rank: int):
    c.execute("UPDATE Activity SET WeeklyRank=%s WHERE UserID=%s", (rank, str(user_id)))
    db.commit()
    return rank

def get_user_rank(input_rank: int):
    c.execute("SELECT UserID FROM Activity WHERE WeeklyRank=%s", (int(input_rank),))
    rank = int(c.fetchone()[0])
    db.commit()
    return rank

def add_messages(user_id: str):
    create_activity(user_id)
    globalmsg = int(get_globalmessages(user_id) + 1)
    weeklymsg = int(get_weeklymessages(user_id) + 1)
    c.execute("UPDATE Activity SET GlobalMessages=%s WHERE UserID=%s", (int(globalmsg), str(user_id)))
    c.execute("UPDATE Activity SET WeeklyMessages=%s WHERE UserID=%s", (int(weeklymsg), str(user_id)))
    db.commit()
    return globalmsg + weeklymsg

def isrisk(creation_date):
    inputacc = datetime.utcnow() - creation_date
    accagedays = int(inputacc.days)
    if accagedays <= 7:
        return True
    else:
        return False


async def muteuser(user, mutedby, reason, msg):
    try:
        server = bot.get_server('550944638383554561')
        userobj = server.get_member(user)
        if userobj == mutedby:
            pass
        else:
            muted = discord.utils.get(server.roles, name="🤬 Muted")
            await bot.add_roles(userobj, muted)
            embed = discord.Embed(title = "You have been muted in `SyteSpace`", description = "Details about your mute:", color =embcolor)
            embed.add_field(name = ":closed_lock_with_key: Moderator:", value = mutedby.display_name)
            embed.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
            embed.set_footer(text="This action was preformed by the overwatch auto-moderation system, if you belive this is a mistake please contact a member of staff", icon_url="https://images-ext-2.discordapp.net/external/uRBzAE1kdh2IHBCpPtO876DgohZkZDafXCfeH0mKu_s/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/534445908394377226/0dcc56c5fb681d249c94bbd929afbcbc.webp")
            embed.set_thumbnail(url=userobj.avatar_url)
            emb = discord.Embed(title = "A member has been muted!", description = "Details about the mute:", color =embcolor)
            emb.add_field(name = ":closed_lock_with_key: Moderator:", value = mutedby.display_name)
            emb.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
            emb.add_field(name = ":spy: User Muted:", value = f"{userobj.name}")
            emb.set_thumbnail(url=userobj.avatar_url)
            await bot.send_message(userobj, embed=embed)
            await bot.send_message(bot.get_channel('565201713951145994'), embed=emb)
    except discord.errors.HTTPException:
        server = bot.get_server('550944638383554561')
        userobj = server.get_member(user)
        muted = discord.utils.get(server.roles, name="🤬 Muted")
        await bot.add_roles(userobj, muted)
        emb = discord.Embed(title = "A member has been muted!", description = "Details about the mute:", color =embcolor)
        emb.add_field(name = ":closed_lock_with_key: Moderator:", value = mutedby.display_name)
        emb.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
        emb.add_field(name = ":spy: User Muted:", value = f"{userobj.name}")
        emb.set_thumbnail(url=userobj.avatar_url)
        await bot.send_message(bot.get_channel('565201713951145994'), embed=emb)


async def createraffle():
    re = []
    amount = random.randint(50, 100)
    embed = discord.Embed(title="A raffle has started!", description=f"A raffle for {amount} sytes has started, type in `s!enter` for a chance to win! (Raffle ends in 5 minutes!)", color=embcolor)
    await bot.send_message(bot.get_channel('551068777995960361'), embed=embed)
    await asyncio.sleep(300)
    winner = random.choice(re)
    print(f"Winner for raffle is {winner} @ {datetime.utcnow()}")
    await bot.send_message(bot.get_channel('551068777995960361'), f"<@{winner}> Has won the raffle! Congratulations!")
    add_tk(winner, amount)
    re = []


async def update_leaderboards():
    while 1:
        ids = []
        weeklead = {}
        globallead = {}
        weekfinal = []
        globalfinal = []
        c.execute("SELECT UserID FROM Activity")
        records = c.fetchall()
        for x in records:
            ids.append(str(x[0]))
        for x in ids:
            weekly = get_weeklymessages(x)
            global_msg = get_globalmessages(x)
            weeklead[weekly] = x
            globallead[weekly] = x
        week_sort = sorted(weeklead.items(),reverse=True)
        maximum= len(ids)
        until = range(1, maximum + 1)
        for x, y in zip(week_sort, until):
            check = set_weekly_rank(x[1], y)
        print("Updated Leaderboards")
        await asyncio.sleep(120)


async def spamcheck():
    while 1:
        spam = dict(spams)
        for user in spam:
            msgs = 0
            pings = 0
            for msg in spam[user]['msgs']:
                if datetime.utcnow() - msg[1] < timedelta(seconds=2):
                    msgs += 1
            for ping in spam[user]['pings']:
                if datetime.utcnow() - ping[1] < timedelta(seconds=2):
                    pings += 1
            if msgs >= 4:
                await muteuser(user, bot.user, "Spamming", spam[user]['msgs'][-1][0])
                await asyncio.sleep(2)
            if pings >= 2:
                await muteuser(user, bot.user, "Ping Spamming", spam[user]['pings'][-1][0])
                await asyncio.sleep(2)
        await asyncio.sleep(1)



@bot.event
async def on_member_join(member: discord.Member):
    #Security
    risky = isrisk(member.created_at)
    if risky == True:
        #Ashtetic
        create_user_if_not_exists(member.id)
        ecowarrior = discord.utils.get(member.server.roles, name="👥 Guest")
        await bot.add_roles(member, ecowarrior)
        embed = discord.Embed(title = f"Welcome to the syte.space discord server, {member.display_name}!", description = "If you wish to aquire a Minecraft server please check out <#550958398410194974> and open a ticket by doing `s!new`", color=0x363942)
        embed.set_footer(text=f"We now have {member.server.member_count} members")
        embed.set_thumbnail(url=member.avatar_url)
        welcome = await bot.send_message(bot.get_channel('573607051297685551'), embed=embed)
        await bot.add_reaction(welcome, '🇭')
        await bot.add_reaction(welcome, '🇮')
        sec = discord.Embed(title=f"A user has joined! [HIGH RISK]", color=0xff0000)
        sec.add_field(name=":notepad_spiral: User Name:", value=f"{member.display_name}", inline=True)
        sec.add_field(name=":space_invader:  User ID:", value=f"{member.id}", inline=False)
        sec.add_field(name=":robot: Is Bot", value=f"{member.bot}", inline=False)
        sec.add_field(name=":clock1: Account Creation Datetime (UTC)", value=f"{member.created_at}", inline=False)
        sec.add_field(name=":rotating_light:", value="HIGH RISK ACCOUNT - STAFF PLEASE MONITOR")
        sec.set_thumbnail(url=member.avatar_url)
        await bot.send_message(bot.get_channel('565201713951145994'), "@here High Risk Account, Please Monitor")
        await bot.send_message(bot.get_channel('565201713951145994'), embed=sec)#log
    elif risky == False:
        create_user_if_not_exists(member.id)
        ecowarrior = discord.utils.get(member.server.roles, name="👥 Guest")
        await bot.add_roles(member, ecowarrior)
        embed = discord.Embed(title = f"Welcome to the syte.space discord server, {member.display_name}!", description = "If you wish to aquire a Minecraft server please check out <#550958398410194974> and open a ticket by doing `s!new`", color=0x363942)
        embed.set_footer(text=f"We now have {member.server.member_count} members")
        embed.set_thumbnail(url=member.avatar_url)
        welcome = await bot.send_message(bot.get_channel('573607051297685551'), embed=embed)
        await bot.add_reaction(welcome, '🇭')
        await bot.add_reaction(welcome, '🇮')
        sec = discord.Embed(title=f"A user has joined!!", color=embcolor)
        sec.add_field(name=":notepad_spiral: User Name:", value=f"{member.display_name}", inline=True)
        sec.add_field(name=":space_invader:  User ID:", value=f"{member.id}", inline=False)
        sec.add_field(name=":robot: Is Bot", value=f"{member.bot}", inline=False)
        sec.add_field(name=":clock1: Account Creation Datetime (UTC)", value=f"{member.created_at}", inline=False)
        sec.set_thumbnail(url=member.avatar_url)

        await bot.send_message(bot.get_channel('565201713951145994'), embed=sec)#log


@bot.event
async def on_message_delete(message):
    try:
        if message.author == bot.user:
            pass
        elif message.content.startswith('s!'):
            pass
        elif ongoingpurge == True:
            pass
        else:
            content = message.content
            author_name = message.author.display_name
            embed = discord.Embed(title=f"A message has been deleted!", color=embcolor)
            embed.add_field(name=":notepad_spiral: Message Content:", value=f"{content}", inline=False)
            embed.add_field(name=":spy: Message Sender:", value=f"{author_name}", inline=False)
            embed.add_field(name=":tv: Message Channel", value=f"<#{message.channel.id}>")
            embed.set_thumbnail(url="http://icons.iconarchive.com/icons/ramotion/custom-mac-os/512/Trash-empty-icon.png")
            await bot.send_message(bot.get_channel('565201713951145994'), embed=embed)#log
    except discord.errors.HTTPException:
        pass

@bot.event
async def on_message_edit(before, after):
    try:
        before_content = before.content
        after_content = after.content
        if before_content == after_content:
            pass
        else:
            embed = discord.Embed(title=f"A message has been edited!", color=embcolor)
            embed.add_field(name=":notepad_spiral: Before:", value=f"{before_content}", inline=True)
            embed.add_field(name=":notepad_spiral: After:", value=f"{after_content}", inline=True)
            embed.add_field(name=":spy: Message Sender:", value=f"{before.author.display_name}", inline=False)
            embed.add_field(name=":spy: Message Sender ID:", value=f"{before.author.id}", inline=False)
            embed.add_field(name=":tv: Message Channel", value=f"<#{before.channel.id}>")
            embed.set_thumbnail(url="https://www.freeiconspng.com/uploads/edit-icon-orange-pencil-0.png")
            await bot.send_message(bot.get_channel('565201713951145994'), embed=embed)#log
    except discord.errors.HTTPException:
        pass


@bot.event
async def on_member_remove(member: discord.Member):
    sec = discord.Embed(title=f"A user has left!", color=embcolor)
    sec.add_field(name=":notepad_spiral: User Name:", value=f"{member.display_name}", inline=True)
    sec.add_field(name=":space_invader:  User ID:", value=f"{member.id}", inline=False)
    sec.add_field(name=":robot: Is Bot", value=f"{member.bot}", inline=False)
    sec.add_field(name=":clock1: Joined Server at", value=member.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
    sec.set_thumbnail(url=member.avatar_url)
    await bot.send_message(bot.get_channel('565201713951145994'), embed=sec)#log




@bot.event
async def on_message(message):
    create_economypp(message.author.id)
    create_activity(message.author.id)
    add_messages(message.author.id)
    boost = getbooster(message.author.id)
    ping = False
    if len(message.raw_mentions) + len(message.raw_role_mentions) > 0:
        ping = True
    if message.author.id in spams:
        if ping:
            spams[message.author.id]['pings'].append([message, datetime.utcnow()])
        spams[message.author.id]['msgs'].append([message, datetime.utcnow()])
    else:
        if ping:
            spams[message.author.id] = {"pings": [[message, datetime.utcnow()]], "msgs": [[message, datetime.utcnow()]]}
        else:
            spams[message.author.id] = {"pings": [], "msgs": [[message, datetime.utcnow()]]}
    #if_tk = random.choice([True, False, False, False, False])
    if boost == True:
        if_tk_boost = secrets.choice([True, False])
        if if_tk_boost == True:
            amount = int(random.randint(1, 5))
            add_tk(message.author.id, amount)
        else:
            pass
    elif boost == False:
        if_tk = secrets.choice([True, False, False, False, False])
        if if_tk == True:
            add_tk(message.author.id, 1)
        else:
            pass
    await bot.process_commands(message)

bot.loop.create_task(spamcheck())
# bot.loop.create_task(update_leaderboards()) 

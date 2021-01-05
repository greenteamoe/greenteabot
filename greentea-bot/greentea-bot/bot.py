import discord
from discord.ext import commands, tasks
import random
import time
import emoji
from datetime import date
from datetime import datetime
import os
from discord.ext.commands import MissingRequiredArgument
import asyncio
import psycopg2
from dotenv import load_dotenv
load_dotenv()

# @greenteamoe
# Moe#9496

client = commands.Bot(case_insensitive=True, command_prefix='.', help_command=None)
ver = 2.0


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(type=discord.ActivityType.watching, name=emoji.emojize("your server! :eyes: | .help")))
    print("Bot is ready.")


@client.command()
async def ping(ctx):
    await ctx.send(emoji.emojize(":ping_pong: Pong! **{0}ms** of latency.".format(round(client.latency * 1000))))


@client.command()
async def pong(ctx):
    await ctx.send(emoji.emojize(":ping_pong: Ping! **{0}ms** of latency.".format(round(client.latency * 1000))))


@client.command(aliases=['ver'])
async def version(ctx):
    await ctx.send("This bot is currently running at version {0}".format(ver))
    time.sleep(5)
    #await ctx.channel.purge(limit=2)


@client.command(aliases=['clean', 'prune', 'purge'])
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("**[ {0} ] messages got deleted!**".format(amount))
    time.sleep(2)
    await ctx.channel.purge(limit=1)


@client.command()
async def kick(ctx, member: discord.Member, *, reasons=None):
    today = datetime.today().strftime('%d/%m/%Y')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await member.kick(reason=reasons)
    em = discord.Embed(title=emoji.emojize("{0} has been kicked".format(member)),
                        description="day: {0}\ntime: {1}".format(today, current_time),
                        color=0xf0e89e)
    await ctx.send(embed=em)


@client.command()
async def ban(ctx, member: discord.Member, *, reasons=None):
    today = datetime.today().strftime('%d/%m/%Y')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await member.ban(reason=reasons)
    em = discord.Embed(title=emoji.emojize("{0} has been banned".format(member)),
    description="day: {0}\ntime: {1}".format(today, current_time),
                       color=0xf0e89e)
    await ctx.send(embed=em)


@client.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send("{0} has been unbanned.".format(user.mention))
            return
        else:
            await ctx.send(emoji.emojize(":warning: User {0} not found.".format(member)))


@client.command()
async def pog(ctx):
    await ctx.send("shark pog")
    await ctx.send("https://tenor.com/view/pog-shark-gif-18177920")


@client.command()
async def avatar(ctx, *, avatarmember: discord.Member = None):
    if avatarmember is None:
        avatarmember = ctx.message.author
        em = discord.Embed(title="Full image here",
                           url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}?size=1024".format(
                               avatarmember),
                           color=0x9ef0b2)
        userAvatarUrl = avatarmember.avatar_url
        em.set_image(url=userAvatarUrl)
        await ctx.send(embed=em)
    else:
        em = discord.Embed(description='requested by:\n{0}'.format(ctx.author), title="Full image here",
                           url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}?size=1024".format(
                               avatarmember),
                           color=0x9ef0b2)
        userAvatarUrl = avatarmember.avatar_url
        em.set_image(url=userAvatarUrl)
        await ctx.send(embed=em)


@client.command(aliases=['8ball', 'question'])
async def _8ball(ctx, *, question):
    responses = ["Yes",
                 "No",
                 "Nah.",
                 "No... I mean yes... Well... Ask again later.",
                 "The answer is unclear... Seriously... I double checked.",
                 "It's a coin flip really...",
                 "Yes, he will... Sorry I wasn't really listening...",
                 "I could tell you but I'd have to permanently ban you.",
                 "Yes, No, Maybe... I don't know, could you repeat the question?",
                 "If you think I'm answering that, you're clearly mistaking me for NotSoBot.",
                 "Do you REALLY want me to answer that? It's kinda obvious.",
                 "YesNoYesNoYesNoYesNoYesNo.",
                 "Yesn't.",
                 "Ask yourself this question in the mirror three times, the answer will become clear.",
                 "You want an answer? OK, here's your answer: "]
    await ctx.send(
        emoji.emojize("Question: {0}\n:speech_balloon: Answer: **{1}**".format(question, random.choice(responses))))


@client.command(aliases=['command', 'commands'])
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", url="https://gist.github.com/cblastin/432dc1bda68b0123b5b4a06c347f3c7b",
                          description="list of commands from greentea bot!", color=0x9ef0b2)
    embed.set_thumbnail(url="https://i.imgur.com/rz8EUMO.png")
    embed.add_field(name="Admin commands:",
                    value="```ban @user     ""\nunban @user#id      ""\nkick @user      ""\nclear 'value'       ```\n",
                    inline=True)
    embed.add_field(name="Function ",
                    value="```\nban users         ""\nunban users         ""\nkick users          ""\nclear chat message         ```",
                    inline=True)

    await ctx.send(embed=embed)
    embed = discord.Embed(color=0x9ef0b2)
    embed.add_field(name="Fun commands:",
                    value="```ping     ""\nver/version         ""\nquestion           \navatar @user           ```",
                    inline=True)
    embed.add_field(name="Function ",
                    value="```\nshows bot latency""\nchecks current version""\nreplies using random answer\nshows user avatar\n```",
                    inline=True)
    await ctx.send(embed=embed)


# COMMAND ERROR HANDLER -- DO NOT REMOVE!!!
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        em = discord.Embed(title=emoji.emojize(":wrench: Command not found..."),
                           description="Please, type .help to see all the commands!", color=0xe74c3c)
        await ctx.send(embed=em)
    elif isinstance(error, commands.MemberNotFound):
        em = discord.Embed(title=emoji.emojize(":mag: User not found..."),
                           description="Please, enter the member name correctly!", color=0xe74c3c)
        await ctx.send(embed=em)
    elif isinstance(error, commands.BotMissingPermissions):
        em = discord.Embed(title=emoji.emojize(":hammer: Missing permissions..."),
                           description="The bot is missing permissions!", color=0xe74c3c)
        await ctx.send(embed=em)
    elif isinstance(error, commands.BadArgument):
        em = discord.Embed(title=emoji.emojize(":no_entry_sign: Bad argument..."),
                           description="The value must be a number!", color=0xe74c3c)
        await ctx.send(embed=em)
    elif isinstance(error, commands.CommandInvokeError):
        em = discord.Embed(title=emoji.emojize(":closed_lock_with_key: Invoke error..."),
                           description="The bot is missing permissions!", color=0xe74c3c)
        await ctx.send(embed=em)

@client.event
async def on_member_join(member, ctx):
    await ctx.send("{0} has joined the server.".format(member))


@client.event
async def on_member_remove(member, ctx):
    await ctx.send("{0} has left the server.".format(member))


@client.event
async def on_message(message):
    responses = ['https://media1.tenor.com/images/1c5b339df666dde2a03276e8da9c66bd/tenor.gif?itemid=12660748',
                 'https://tenor.com/view/pino-ergo-proxy-galatiosy-darkville-anime-gif-12660742',
                 'https://tenor.com/view/pino-ergo-proxy-galatiosy-darkville-anime-gif-12660749',
                 'https://tenor.com/view/pino-ergo-proxy-galatiosy-darkville-anime-gif-12660751',
                 'https://tenor.com/view/pino-ergo-proxy-galatiosy-darkville-anime-gif-12660741',
                 'https://tenor.com/view/pino-ergo-proxy-galatiosy-darkville-anime-gif-12660754',
                 'https://tenor.com/view/pino-ergo-proxy-galatiosy-darkville-anime-gif-12660753',
                 'https://tenor.com/view/pino-ergo-proxy-galatiosy-darkville-anime-gif-12660745',
                 'https://tenor.com/view/pino-ergo-proxy-galatiosy-darkville-anime-gif-12660743',
                 'https://data.whicdn.com/images/246578964/original.gif',
                 'https://i.pinimg.com/originals/5b/4b/76/5b4b762b7267fa0919d22a529eac8c16.gif',
                 'https://64.media.tumblr.com/310319232ac33a7fa939748fd7b06a78/tumblr_n0rf5mhCL51swmg9to1_r1_500.gif',
                 'https://i.imgur.com/NeuCKPx.gif',
                 'https://gifdownload.net/wp-content/uploads/2019/02/ergo-proxy-pino-gif-6.gif',
                 'https://pa1.narvii.com/5745/9106409bfcc6e400e4180938de8dfa1484572dc8_hq.gif',
                 'https://i.imgur.com/mcq1ySr.gif',
                 'https://i.imgur.com/cSN73XV.gif',
                 'https://avatarfiles.alphacoders.com/946/94677.gif',
                 'https://data.whicdn.com/images/246579610/original.gif',
                 'https://i.imgur.com/6GvsrKp.gif',
                 'https://64.media.tumblr.com/fd9d5d4680ad77b0aeeec312293b911a/tumblr_n0kbdh74bo1sfd142o5_500.gif',
                 'https://i.imgur.com/Ymy6JwK.gif']

    if "PINO" in message.content.upper() or "ピノ" in message.content:
        if message.author != client.user:
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()
            query = "UPDATE pino SET qtd = qtd + 1 WHERE id = 1 RETURNING qtd;"
            cursor.execute(query)
            result = cursor.fetchone()
            conn.commit()
            conn.close()
            await message.channel.send("PINO! Pino's name has been sent {0} times!".format(result[0]))
            await message.channel.send(random.choice(responses))
    await client.process_commands(message)

client.run('Nzg0OTM2OTkzODgzODE1OTM3.X8wjig.MCRmIXPIq0lmtNYygVp2IE7rWNk')

import discord
from discord.ext import commands
import asyncio
import re
import random
from time import perf_counter

class InvalidTimeException(Exception):
    pass

intents = discord.Intents.default()
intents.message_content = True

bot = commands.AutoShardedBot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot Activated!\n')
    print('------------------------------\n')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    while True:
        act = f'debates in {len(bot.guilds)} servers'
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=act))
        await asyncio.sleep(1800)

# def time_parser(time_str : str) -> (int ,int):
#     match = re.search('^(?P<min>[0-5]?[0-9]m){0,1}(?P<sec>[0-5]?[0-9]s){0,1}$', time_str)
#     if match != None:
#         minutes = match.group('min')
#         minutes = minutes[:-1] if minutes != None and minutes != '' else '0'
#         seconds = match.group('sec')
#         seconds = seconds[:-1] if seconds != None and seconds != '' else '0'
#         print(f'value : {minutes} {seconds}')
#         return (int(minutes), int(seconds)) 
#     raise InvalidTimeException('**Invalid Tim for Timer**')
    
# @bot.tree.command(description = 'Specify time using format XmYs or Ym, where X=minutes and Y=seconds e.g. 7m15s or 7m')
# async def timer (interaction):
#     args = interaction.message
#     try:
#         has_reached_one_minute = False
#         minutes, seconds = time_parser(args)
#         time = minutes * 60 + seconds
#         await ctx.response.send_message(f'⏱️ **Timer started for {minutes}m {seconds}s** {ctx.author.mention}')
#         timestamp = perf_counter()
#         timer = 0
#         clock = await ctx.send(f'⏳ **Timer** `{str(int(time / 60)).zfill(2)}m{str(int(time % 60)).zfill(2)}s`')
#         while timer < time: 
#             await clock.edit(content=f'⏳ **Timer** `{str(int((time - timer) / 60)).zfill(2)}m{str(int((time - timer) % 60)).zfill(2)}s`')
#             if time - timer < 60 and not has_reached_one_minute:
#                 has_reached_one_minute = True
#                 await ctx.send(f'🟠 **1 minute left!** {ctx.author.mention}')
#             await asyncio.sleep(float(1))
#             timer = perf_counter() - timestamp
            
#         await clock.edit(content=f'⏳ **Timer** `{str(0).zfill(2)}m{str(0).zfill(2)}s`')        
#         await ctx.send(f'🔴 **Time finished for** {ctx.author.mention}')
#     except InvalidTimeException:
#         ctx.send(f'**Invalid Time for Timer**')

@bot.tree.command(name='coinflip',description = "Chooses between heads and tails, useful for vetoes")
async def coinflip(interaction):
    coin = ['Head', 'Tails']
    await interaction.response.send_message(random.choice(coin))

# @bot.command(name="commands",description="Lists commands for the Hear Hear bot.")
# async def commands(ctx):
#     embed = discord.Embed()
#     embed.title = "List of Commands for the PolyDebat Bot"
#     embed.set_image(url="https://i.imgur.com/7Lw4CRt.gif")
#     embed.description = f"""
# `/ping`
# Checks response time between client and Hear Hear! bot.

# `/commands`
# Displays list of commands.

# `/coinflip`
# Randomly chooses between heads and tails. Useful for vetoes.

# `/getmotion`
# Displays a random motion from the hellomotions motion bank.

# `/time`
# Times a speech with format *XmYs*, e.g. *7m*, *5m30s*, *30s*.
# """
#     #embed.set_footer(text="Message <@704206757681037362> or <@696777012110688296> for technical help.",icon_url="https://i.imgur.com/RaQy5so.png")
#     await ctx.send(embed=embed)


bot.run('MTE0NjUyNDY2ODIxMjI4MTQzNg.GzRVFY.gnc9wtg5VGvx6CvjPQm9KPZG8xktqLoijvYZys')

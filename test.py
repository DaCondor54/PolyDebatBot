#DaCondor Try at creating the Timer. Hear Hear Bot was better and proven 

import discord
from discord.ext import commands
from discord import app_commands
import random
import re
from time import perf_counter
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents = intents)

class InvalidTimeException(Exception):
    pass

@client.tree.command(name='coinflip', description='Chooses between heads and tails, useful for vetoes')
async def coinflip(interaction):
    faces = ['Head', 'Tails']
    await interaction.response.send_message(random.choice(faces))


def time_parser(time_str : str) -> (int ,int):
    match = re.search('^(?P<min>[0-5]?[0-9]m){0,1}(?P<sec>[0-5]?[0-9]s){0,1}$', time_str)
    if match != None:
        minutes = match.group('min')
        minutes = minutes[:-1] if minutes != None and minutes != '' else '0'
        seconds = match.group('sec')
        seconds = seconds[:-1] if seconds != None and seconds != '' else '0'
        print(f'value : {minutes} {seconds}')
        return (int(minutes), int(seconds)) 
    raise InvalidTimeException('**Invalid Tim for Timer**')
    
@client.tree.command(name='timer',description = 'Specify time using format XmYs or Ym, where X=minutes and Y=seconds e.g. 7m15s or 7m')
@app_commands.describe(args="Specify time using format XmYs or Ym, where X=minutes and Y=seconds e.g. 7m15s or 7m")
async def set_timer (interaction : discord.Interaction, args: str):
    try:
        has_reached_one_minute = False
        
        minutes, seconds = time_parser(args)
        time = minutes * 60 + seconds
        await interaction.response.send_message(f'⏱️ **Timer started for {minutes}m {seconds}s** {interaction.user.mention}')
        timestamp = perf_counter()
        timer = 0
        clock = await interaction.channel.send(f'⏳ **Timer** `{str(int(time / 60)).zfill(2)}m{str(int(time % 60)).zfill(2)}s`')
        while timer < time: 
            await clock.edit(content=f'⏳ **Timer** `{str(int((time - timer) / 60)).zfill(2)}m{str(int((time - timer) % 60)).zfill(2)}s`')
            if time - timer < 60 and not has_reached_one_minute:
                has_reached_one_minute = True
                await interaction.channel.send(f'🟠 **1 minute left!** {interaction.user.mention}')
            await asyncio.sleep(float(1))
            timer = perf_counter() - timestamp
            
        await clock.edit(content=f'⏳ **Timer** `{str(0).zfill(2)}m{str(0).zfill(2)}s`')        
        await interaction.channel.send(f'🔴 **Time finished for** {interaction.user.mention}')
    except InvalidTimeException:
        interaction.channel.send(f'**Invalid Time for Timer**')

#Sync Commands
@client.command(name='sync', description='Use by the Owner to sync the command tree and have access to /slash commands')
async def sync(ctx):
    print("sync command")
    if ctx.author.id == 422556147887767574:
        synced = await client.tree.sync()
        await ctx.send(f'Command tree synced {synced}.')
    else:
        await ctx.send('You must be the owner to use this command!')



client.run('TOKEN')
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

class Timer(discord.ui.View):
    def __init__(self,mins,secs):
        super().__init__()
        self.mins = mins
        self.secs = secs
        self.paused = False
        self.stopped = False
        self.time1 = int(mins)*60 + int(secs)
        self.time2 = self.time1
        self.time3 = 0
        self.buttonPause = discord.ui.Button(label="Pause ✋", style=discord.ButtonStyle.grey)
        self.buttonStop = discord.ui.Button(label="Stop Timer 🛑", style=discord.ButtonStyle.blurple)

    async def time(self, interaction):
        msg = interaction.message
        
        if interaction.response.is_done():
            await msg.edit(view=self)
        else:
            await interaction.response.edit_message(view=self)

        n = float(1)
        while self.time2 >= 0 and not self.paused and not self.stopped:
            await msg.edit(content=f"⏳ **Timer**   `{str(int(self.time2/60)).zfill(2)} : {str(self.time2%60).zfill(2)}`")
            j = self.time2%5
            if j:
                self.time2 -= j
                self.time3 += j
                await msg.edit(content=f"⏳ **Timer**   `{str(int(self.time2/60)).zfill(2)} : {str(self.time2%60).zfill(2)}`")
            await asyncio.sleep(4+float(n))
            self.time2 -= 5
            self.time3 += 5
            if self.time3 == 60:
                await interaction.channel.send(f"\n\n🟢  **1 minute done!** {interaction.user.mention}")
            if self.time2 == 60:
                await interaction.channel.send(f"\n\n🟠  **1 minute left!** {interaction.user.mention}")
            if self.time2 == 0:
                self.buttonPause.disabled = True
                self.buttonStop.disabled = True
                await msg.edit(content="Timer stopped! Use `/time` to start a new timer.",view=self)
                await interaction.channel.send(f"\n\n🔴  **Time's up!** {interaction.user.mention}")
    

    @discord.ui.button(label="Start Timer ⏱️", style=discord.ButtonStyle.green)
    async def buttonStart(self, interaction: discord.Interaction, button: discord.ui.Button):

        async def pause(interaction: discord.Interaction):
            self.buttonStop.disabled = not self.buttonStop.disabled
            self.paused = not self.paused
            if self.paused:
                self.buttonPause.label = "Resume 👍"
                if interaction.response.is_done():
                    await interaction.message.edit(content=f"⏸️   **PAUSED**   `{str(int(self.time2/60)).zfill(2)} : {str(self.time2%60).zfill(2)}`",view=self)
                else:
                    await interaction.response.edit_message(content=f"⏸️  **PAUSED**   `{str(int(self.time2/60)).zfill(2)} : {str(self.time2%60).zfill(2)}`",view=self)
            if not self.paused:
                self.buttonPause.label = "Pause ✋"
                await self.time(interaction)              
        async def stop(interaction: discord.Interaction):
            self.buttonPause.disabled = True
            self.buttonStop.disabled = True
            self.stopped = True
            await interaction.response.edit_message(content="Timer stopped! Use `/time` to start a new timer.",view=self)
        self.buttonPause.callback = pause
        self.buttonStop.callback = stop
        button.disabled = True
        self.add_item(self.buttonPause)
        self.add_item(self.buttonStop)
        await self.time(interaction)

@client.tree.command(name="settimer", description="Times a debate speech.")
@app_commands.describe(time="Specify time using format XmYs or Ym, where X=minutes and Y=seconds e.g. 7m15s or 7m")
async def settimer(interaction: discord.Interaction, time: str):
    pattern = re.compile("^([0-9]{1,2}m[0-9]{1,2}s)|([0-9]{1,2}m)|([0-9]{1,2}s)$")
    if not re.match(pattern, time):
        await interaction.response.send_message("Invalid syntax! Please use the format `XmYs`, e.g. `7m15s`.")
        return

    time = time.split("m")
    if len(time)==2:
        mins = time[0].zfill(2)
        secs = time[1][:-1].zfill(2)
    else:
        mins = "00"
        secs = time[0][:-1].zfill(2)


    await interaction.response.send_message(f"⏳ **Timer**   `{mins} : {secs}`", view=Timer(mins,secs))

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
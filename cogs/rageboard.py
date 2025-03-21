import discord
import os
from discord.ext import commands
from discord.utils import format_dt
from discord import app_commands
from dotenv import load_dotenv
from discord import app_commands, Embed, ui
from datetime import datetime

load_dotenv('../.version', override=True)
load_dotenv('../.config', override=True)
rageboard_status = os.getenv('CONFIG_RAGEBOARD')
rageboard_id = int(os.getenv('CONFIG_RAGEBOARD_CHANNEL_ID'))
server_id = int(os.getenv('CONFIG_SERVER_ID'))
booster_id = int(os.getenv('CONFIG_SERVER_BOOSTER_ID'))
version = os.getenv('VERSION')

class Postui(ui.Modal, title='Posting to Rageboard'):
   body = ui.TextInput(label='Body text', placeholder="Rage about something here!", style=discord.TextStyle.long)
   image = ui.TextInput(label='Image link', placeholder="Paste an image link here if you have one!", style=discord.TextStyle.short, required=False)
   green = ui.TextInput(label='Make greentext', placeholder="Write 'true' to make the embed a green text.", style=discord.TextStyle.short, required=False)

   async def on_submit(self, interaction: discord.Interaction):
       await interaction.response.send_message(f'Sending to Rageboard...')
       default_color = discord.Colour(27010)
       embed = discord.Embed(
           color=discord.Colour.dark_green() if self.green.value.lower() == "true" else default_color,
           description=self.body.value
       )
       embed.set_author(
           name=interaction.user,
           icon_url=interaction.user.avatar,
       )
       if self.image.value:
           embed.set_thumbnail(url=self.image.value)
           
       unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
       embed.set_footer(text=f"Rageboard | {version}")
       rageboard_channel = interaction.client.get_channel(rageboard_id)
       message = await rageboard_channel.send(f"{format_dt(datetime.now(), style='F')}", embed=embed)
       mid = message.id
       await message.add_reaction("♥️")
       thread = await message.create_thread(name=f'Rageboard thread {mid}')

   async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
       if interaction.response.is_done():
           embed = discord.Embed(title="[Errno 4] Unknown error!", description="God give us strength.", colour=0xa51d2d)
           embed.set_image(url=f'https://http.cat/{error.status}.jpg')
           embed.set_footer(text=f"Ragecord Utils {version}")
           await interaction.send_message(embed=embed)
       else:
           embed = discord.Embed(title="[Errno 4] Unknown error!", description="God give us strength.", colour=0xa51d2d)
           embed.set_image(url=f'https://http.cat/{error.status}.jpg')
           embed.set_footer(text=f"Ragecord Utils {version}")
           await interaction.send_message(embed=embed)
        
class Postuipremium(ui.Modal, title='Posting to Rageboard with premium'):
   body = ui.TextInput(label='Body text', placeholder="Rage about something here!", style=discord.TextStyle.long)
   image = ui.TextInput(label='Image link', placeholder="Paste an image link here if you have one!", style=discord.TextStyle.short, required=False)
   bigimage = ui.TextInput(label='Big image link', placeholder="Paste a bigger image link here if you have one!", style=discord.TextStyle.short, required=False)
   green = ui.TextInput(label='Make greentext', placeholder="Write 'true' to make the embed a green text.", style=discord.TextStyle.short, required=False)

   async def on_submit(self, interaction: discord.Interaction):
       await interaction.response.send_message(f'Sending to Rageboard as a Premium user...')
       default_color = discord.Colour(14695336)
       
       embed = discord.Embed(
           color=discord.Colour.dark_green() if self.green.value.lower() == "true" else default_color,
           description=self.body.value
       )
       embed.set_author(
           name=f"{interaction.user}",
           icon_url=interaction.user.avatar,
       )
       if self.image.value:
           embed.set_thumbnail(url=self.image.value)
           
       if self.bigimage.value:
           embed.set_image(url=self.bigimage.value)
           
       unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
       embed.set_footer(text=f"Rageboard Premium | {version}", icon_url="https://cdn.discordapp.com/emojis/1350579789823742042.gif?size=80&quality=lossless")
       rageboard_channel = interaction.client.get_channel(rageboard_id)
       message = await rageboard_channel.send(f"{format_dt(datetime.now(), style='F')}", embed=embed)
       mid = message.id
       await message.add_reaction("⭐")
       thread = await message.create_thread(name=f'Rageboard thread {mid}')

   async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
       if interaction.response.is_done():
           embed = discord.Embed(title="[Errno 4] Unknown error!", description="God give us strength.", colour=0xa51d2d)
           embed.set_image(url=f'https://http.cat/{error.status}.jpg')
           embed.set_footer(text=f"Ragecord Utils {version}")
           await interaction.send_message(embed=embed)
       else:
           embed = discord.Embed(title="[Errno 4] Unknown error!", description="God give us strength.", colour=0xa51d2d)
           embed.set_image(url=f'https://http.cat/{error.status}.jpg')
           embed.set_footer(text=f"Ragecord Utils {version}")
           await interaction.send_message(embed=embed)
           
class Rageboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @app_commands.command(
        name="post",
        description="Post a thread on Rageboard"
    )
    @app_commands.guilds(discord.Object(id=server_id))
    async def post(self, interaction:discord.Interaction):
        role = interaction.guild.get_role(booster_id)
        def checkBooster():
            if role in interaction.user.roles:
                return True
            else:
                return False
            
        if checkBooster():
            modal = Postuipremium()
            await interaction.response.send_modal(modal)
        else:
            modal = Postui()
            await interaction.response.send_modal(modal)

async def setup(bot: commands.Bot):
    await bot.add_cog(Rageboard(bot))

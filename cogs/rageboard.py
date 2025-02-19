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
version = os.getenv('VERSION')

class Postui(ui.Modal, title='Posting to Rageboard'):
   body = ui.TextInput(label='Body text', placeholder="Rage about something here!", style=discord.TextStyle.long)
   image = ui.TextInput(label='Image link', placeholder="Paste an image link here if you have one!", style=discord.TextStyle.short, required=False)
   green = ui.TextInput(label='Make greentext', placeholder="Write 'true' (case sensitive, write without commas) to make the embed a green text.", style=discord.TextStyle.short, required=False)

   async def on_submit(self, interaction: discord.Interaction):
       await interaction.response.send_message(f'Sending to Rageboard...')
       embed = discord.Embed(
           color=discord.Colour.dark_green() if self.green.value == "true" else 2183,
           description=self.body.value
       )
       embed.set_author(
           name=interaction.user,
           icon_url=interaction.user.avatar,
       )
       if self.image.value:
           embed.set_thumbnail(url=self.image.value)
           
       unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
       embed.set_footer(text=f"@Rageboard | {version}")
       rageboard_channel = interaction.client.get_channel(rageboard_id)
       message = await rageboard_channel.send(f"{format_dt(datetime.now(), style='F')}", embed=embed)
       mid = message.id
       thread = await message.create_thread(name=f'Rageboard thread {mid}')

   async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
       if interaction.response.is_done():
           print(f"Error occurred: {error}")
       else:
           await interaction.response.send_message(f"{error}\n## Rageboard modal created successfully, but an ***extremely rare fatal error*** occured. Report this to the development team. Bailing out, you are on your own. Good luck.", ephemeral=True)
        
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
        modal = Postui()
        await interaction.response.send_modal(modal)

async def setup(bot: commands.Bot):
    await bot.add_cog(Rageboard(bot))
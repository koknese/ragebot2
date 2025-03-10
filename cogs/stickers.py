import discord
import os
import json
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from discord import app_commands, Embed, ui
from typing import Literal

load_dotenv('../version', override=True)
load_dotenv('../.config', override=True)
server_id = os.getenv('CONFIG_SERVER_ID')
version = os.getenv('VERSION')

class Stickers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @app_commands.command(name='create-sticker', description='Create a sticker. Useful on mobile.')
    @app_commands.guilds(discord.Object(id=server_id))
    async def createstickers(self, interaction: discord.Interaction, name: str, description: str, emoji: str, image: discord.Attachment):
        try:
            sticker = await create_sticker(name=name, description=description, emoji=emoji, file=image, reason=f"Sticker {name} was created by {interaction.user}")
            embed = discord.Embed(title="Sticker created successfully!", colour=0x26a269)
            embed.set_footer(text=f"Ragecord Utils {version}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await interaction.followup.send(sticker, ephemeral=True)
        except Forbidden:
            embed = discord.Embed(title="[Errno 2] You lack permissions to create stickers!", colour=0xa51d2d)
            embed.set_footer(text=f"Ragecord Utils {version}")
            await interaction.send_message(embed=embed, ephemeral=True)
        except HTTPException:
            embed = discord.Embed(title="[Errno 3] HTTP Exception", description="There has been rare, mythical, impossible and catastrophical error with the Discord API. If you see this, pick a god and pray, because the gates of hell have opened. Try again later!", colour=0xa51d2d)
            embed.set_footer(text=f"Ragecord Utils {version}")
            await interaction.send_message(embed=embed, ephemeral=True)
            
async def setup(bot: commands.Bot):
    await bot.add_cog(Stickers(bot))

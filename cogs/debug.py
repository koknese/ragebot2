import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

load_dotenv('../.config', override=True)
server_id = os.getenv('CONFIG_SERVER_ID')

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @app_commands.command(
        name="hello",
        description="DEBUG: Ping"
    )
    @app_commands.guilds(discord.Object(id=server_id))
    async def hello(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # in ms
        await interaction.response.send_message(f"haii! :3 {interaction.user.display_name}, latency is {latency}ms.")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Debug(bot))
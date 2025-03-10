import discord
import os
import os.path
import json
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from discord import app_commands, Embed

load_dotenv('../version', override=True)
load_dotenv('../.config', override=True)
server_id = os.getenv('CONFIG_SERVER_ID')
version = os.getenv('VERSION')

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @app_commands.command(name='create-tag', description='Create a tag!')
    @app_commands.guilds(discord.Object(id=server_id))
    async def createTag(self, interaction: discord.Interaction, name: str, content: str):
        if not os.path.exists("tags"):
            os.makedirs("tags")

        path = f"tags/{name}.json"
        fileExists = os.path.exists(path)
        if fileExists:
            embed_dict = {
                "name": name,
                "creator": interaction.user.name,
                "content": content
            }

            with open(f'tags/{name}.json', 'w') as f:
                json.dump(embed_dict, f, indent=4)
            print(f"{interaction.user} created a tag")
            await interaction.response.send_message(f"Tag {name} created!")
        else:
            await interaction.response.send_message(f"Tag {name} already exists!", ephemeral=True)
    
    @app_commands.command(name='tag', description='Read a tag')
    @app_commands.guilds(discord.Object(id=server_id))
    @app_commands.describe(tag="Tag to read")
    async def readTag(self, interaction: discord.Interaction, tag: str):
        try:
            with open(f'tags/{tag}.json', 'r') as f:
                data = json.load(f) 
            name = data["name"]
            creator = data["creator"]
            content = data["content"]
            
            await interaction.response.send_message(f"`tags/{tag}.json` || {content}\n-# tag created by {creator}")
        except FileNotFoundError:
            await interaction.response.send_message(f"***[Errno 1]***: tags/{tagname}.json does not exist")
            
    @app_commands.command(name='delete-tag', description='Delete a tag')
    @app_commands.guilds(discord.Object(id=server_id))
    @discord.app_commands.checks.has_permissions(manage_messages=True)
    async def deleteTag(self, interaction: discord.Interaction, tag: str, reason: str):
        try:
            os.remove(f"tags/{tag}.json")
            embed = discord.Embed(title=f"Removed tag {tag}", description=f"Reason:\n{reason}", colour=0xff7800)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message(f"***[Errno 1]***: File not found")

async def setup(bot: commands.Bot):
    await bot.add_cog(Tags(bot))
        
        
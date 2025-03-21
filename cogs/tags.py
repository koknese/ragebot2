import discord
import os
import os.path
import json
from misc.paginator import Pagination
from discord.ext import commands
from discord import app_commands, Embed
from dotenv import load_dotenv
from discord.app_commands import Group, command
from discord.ext.commands import GroupCog

load_dotenv('../version', override=True)
load_dotenv('../.config', override=True)
server_id = os.getenv('CONFIG_SERVER_ID')
version = os.getenv('VERSION')

class Tags(GroupCog, group_name='tags', group_description='tags, short snippets of information'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @command(name='create', description='Create a tag!')
    async def createTag(self, interaction: discord.Interaction, name: str, content: str):
        if not os.path.exists("tags"):
            os.makedirs("tags")

        path = f"tags/{name}.json"
        fileExists = os.path.exists(path)
        if not fileExists:
            tag_dict = {
                "name": name,
                "creator": interaction.user.name,
                "content": content
            }

            with open(f'tags/{name}.json', 'w') as f:
                json.dump(tag_dict, f, indent=4)
            print(f"{interaction.user} created a tag")
            await interaction.response.send_message(f"Tag {name} created!")
        else:
            await interaction.response.send_message(f"Tag {name} already exists!", ephemeral=True)
            
    
    @command(name='show', description='Read a tag')
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
            embed = discord.Embed(title="[Errno 1] File does not exist!", colour=0xa51d2d)
            embed.set_image(url=f'https://http.cat/404.jpg')
            embed.set_footer(text=f"Ragecord Utils {version}")
            await interaction.response.send_message(embed=embed)
            
    @command(name='remove', description='Delete a tag')
    @discord.app_commands.checks.has_permissions(manage_messages=True)
    async def deleteTag(self, interaction: discord.Interaction, tag: str, reason: str):
        try:
            os.remove(f"tags/{tag}.json")
            embed = discord.Embed(title=f"Removed tag {tag}", description=f"Reason:\n{reason}", colour=0xff7800)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_footer(text=f"Ragecord Utils v.{version}")
            await interaction.response.send_message(embed=embed)
        except FileNotFoundError:
            embed = discord.Embed(title="[Errno 1] File does not exist!", colour=0xa51d2d)
            embed.set_image(url=f'https://http.cat/404.jpg')
            embed.set_footer(text=f"Ragecord Utils {version}")
            await interaction.response.send_message(embed=embed)
    
    # What you're about to see is the prime definition of being held together by gum & string
    @command(name='list', description='List tags')
    async def show(self, interaction: discord.Interaction):
        def get_taglist():
            taglist = os.listdir("tags")
            lst = [os.path.splitext(x)[0] for x in taglist]
            return lst

        taglist = get_taglist()
        L = 10
        async def get_page(page: int):
            emb = discord.Embed(title="Tag list", description="")
            offset = (page-1) * L
            for tag in taglist[offset:offset+L]:
                emb.description += f"`{tag}`\n"
            emb.set_author(name=f"Requested by {interaction.user}")
            n = Pagination.compute_total_pages(len(taglist), L)
            emb.set_footer(text=f"Page {page} from {n}")
            return emb, n

        await Pagination(interaction, get_page).navegate()
async def setup(bot: commands.Bot):
    await bot.add_cog(Tags(bot), guild=discord.Object(id=server_id))
        
        
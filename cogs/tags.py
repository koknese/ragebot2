import discord
import os
import os.path
import json
from misc.paginator import Pagination
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from discord import app_commands, Embed

load_dotenv('../version', override=True)
load_dotenv('../.config', override=True)
server_id = os.getenv('CONFIG_SERVER_ID')
tagbanned_id = os.getenv('CONFIG_TAGS_BANNED_ID')
version = os.getenv('VERSION')

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @app_commands.command(name='create-tag', description='Create a tag!')
    @app_commands.guilds(discord.Object(id=server_id))
    @discord.ext.commands.has_role(tagbanned_id)
    async def createTag(self, interaction: discord.Interaction, name: str, content: str):
        try:
            await interaction.response.send_message("You were banned from creating tags")
        except discord.ext.commands.MissingRole:
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
            embed.set_footer(text=f"Ragecord Utils v.{version}")
            await interaction.response.send_message(embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message(f"***[Errno 1]***: File not found")
    
    # What you're about to see is the prime definition of being held together by gum & string
    @app_commands.command(name='list-tags', description='List tags')
    @app_commands.guilds(discord.Object(id=server_id))
    async def show(self, interaction: discord.Interaction):
        def get_taglist():
            taglist = os.listdir("tags")
            return taglist

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

    @app_commands.command(name='tag-ban', description='Ban a user from making tags')
    @app_commands.guilds(discord.Object(id=server_id))
    @app_commands.describe(user="User to ban from tags")
    @discord.app_commands.checks.has_permissions(manage_roles=True)
    async def banTag(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        try:
            role = discord.Object(id=tagbanned_id)
            await user.add_roles(role)
            
            embed = discord.Embed(title=f"Tagbanned {user}", description=f"Reason:\n{reason}", colour=0xff7800)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_footer(text=f"Ragecord Utils v.{version}")
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("You do not have sufficient permissions.", ephemeral=True)
        except discord.HTTPException:
            embed = discord.Embed(title="[Errno 3] HTTP Exception", description="There has been rare, mythical, impossible and catastrophical error with the Discord API. If you see this, pick a god and pray, because the gates of hell have opened. Try again later!", colour=0xa51d2d)
            embed.set_footer(text=f"Ragecord Utils {version}")
            await interaction.send_message(embed=embed, ephemeral=True)
            
    @app_commands.command(name='tag-unban', description='Unban a user from making tags')
    @app_commands.guilds(discord.Object(id=server_id))
    @app_commands.describe(user="User to unban from tags")
    @discord.app_commands.checks.has_permissions(manage_roles=True)
    async def unbanTag(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        try:
            role = discord.Object(id=tagbanned_id)
            await user.remove_roles(role)
            
            embed = discord.Embed(title=f"Untagbanned {user}", description=f"Reason:\n{reason}", colour=0xff7800)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_footer(text=f"Ragecord Utils v.{version}")
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("You do not have sufficient permissions.", ephemeral=True)
        except discord.HTTPException:
            embed = discord.Embed(title="[Errno 3] HTTP Exception", description="There has been rare, mythical, impossible and catastrophical error with the Discord API. If you see this, pick a god and pray, because the gates of hell have opened. Try again later!", colour=0xa51d2d)
            embed.set_footer(text=f"Ragecord Utils {version}")
            await interaction.send_message(embed=embed, ephemeral=True)
            
async def setup(bot: commands.Bot):
    await bot.add_cog(Tags(bot))
        
        
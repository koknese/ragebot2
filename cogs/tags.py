import discord
import os
import os.path
import time
import sqlite3
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
        try:
            conn = sqlite3.connect('data.sqlite')
            c = conn.cursor()
        
            c.execute("""CREATE TABLE IF NOT EXISTS tags(
                         tag_name string NOT NULL,
                         tag_content TEXT NOT NULL,
                         tag_author NOT NULL
                         )""")
            c.execute("SELECT 1 FROM tags WHERE tag_name = ? LIMIT 1;", (name,))
            if c.fetchone():
                embed = discord.Embed(title="Tag already exists!", colour=0xc01c28, description=f"A tag with the name `{name}` already exists.")
                embed.set_footer(text=f"Ragecord Utils v.{version}")
                await interaction.response.send_message(embed=embed)
                c.close()
                conn.close()
                return
        
            c.execute("""INSERT INTO tags (tag_name, tag_content, tag_author)
                         VALUES (?, ?, ?);
                      """, (name, content, interaction.user.id))
        
            embed = discord.Embed(title=f"Tag {name} created!", colour=0x2ec27e)
            embed.set_footer(text=f"Ragecord Utils v.{version}")
            
            conn.commit()
            c.close()
            conn.close()

            await interaction.response.send_message(embed=embed)
        except sqlite3.Error as e:
            embed = discord.Embed(title="An SQL error occured!", colour=0xc01c28, description=f"***Traceback:***\n```\n{e}\n```")
            embed.set_footer(text=f"Ragecord Utils v.{version}")
            await interaction.response.send_message(embed=embed)

    
    @command(name='show', description='Read a tag')
    @app_commands.describe(tag="Tag to read")
    async def readTag(self, interaction: discord.Interaction, tag: str):
        try:
            conn = sqlite3.connect('data.sqlite')
            c = conn.cursor()
            c.execute("SELECT * FROM tags WHERE tag_name = ?", (tag,))
            row = c.fetchone()
            if row:
                name = row[0]
                content = row[1]
                author = await self.bot.fetch_user(row[2])
                await interaction.response.send_message(f"`data.sqlite/{name}` || {content}\n-# tag created by {author}")
            else:
                embed = discord.Embed(title="Tag not found!", colour=0xc01c28)
                embed.set_footer(text=f"Ragecord Utils v.{version}")
                await interaction.response.send_message(embed=embed)
        except sqlite3.OperationalError:
                embed = discord.Embed(title="SQL: Table not found!", colour=0xc01c28, description="Perhaps a database hasn't been generated yet? Creating a tag creates one!")
                embed.set_footer(text=f"Ragecord Utils v.{version}")
                await interaction.response.send_message(embed=embed)
            
    @command(name='remove', description='Delete a tag')
    @discord.app_commands.checks.has_permissions(manage_messages=True)
    async def deleteTag(self, interaction: discord.Interaction, tag: str, reason: str):
        try:
            conn = sqlite3.connect('data.sqlite')
            c = conn.cursor()
            c.execute("DELETE from tags where tag_name = ?", (tag,)) 
            conn.commit()
            c.close()
            conn.close()
            
            embed = discord.Embed(title=f"Removed tag {tag}", description=f"Reason:\n{reason}", colour=0xff7800)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_footer(text=f"Ragecord Utils v.{version}")
            await interaction.response.send_message(embed=embed)
        except sqlite3.Error as e:
            embed = discord.Embed(title="SQL exception!", colour=0xa51d2d, description=f"***Traceback***:\n{e}")
            embed.set_image(url=f'https://http.cat/404.jpg')
            embed.set_footer(text=f"Ragecord Utils {version}")
            await interaction.response.send_message(embed=embed)
    
    # What you're about to see is the prime definition of being held together by gum & string
    @command(name='list', description='List tags')
    async def show(self, interaction: discord.Interaction):
        conn = sqlite3.connect('data.sqlite')
        c = conn.cursor()
        c.execute("SELECT tag_name FROM tags;")
        taglist = [row[0] for row in c.fetchall()]
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
        
        
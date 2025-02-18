import discord
import json
from discord import app_commands, Embed
from discord.utils import get # New import
from discord.ext import commands
from dotenv import load_dotenv
from typing import Literal
import os
intents = discord.Intents.all()
intents.members = True
load_dotenv()
server_id = 1301977681449189437
version = "v.1.0.0-rc.4"
token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix="sudo ", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await tree.sync(guild=discord.Object(id=server_id))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"YouTube poops"))
    print(discord.__version__)

def parse_embed_json(json_file):
    embeds_json = loads(json_file)['embeds']

    for embed_json in embeds_json:
        embed = Embed().from_dict(embed_json)
        yield embed

@bot.event
async def on_member_join(member):
    patientID = 1301977681474224173
    role_patient = discord.Object(id=patientID)
    await member.add_roles(role_patient)

@tree.command(
        name='hello',
        description='haii',
        guild=discord.Object(id=server_id)
)
async def hello (interaction: discord.Interaction):
		await interaction.response.send_message("guh")

@tree.command(
        name='profile-edit',
        description='Edit your ragecord profile!',
        guild=discord.Object(id=server_id)
)
#@app_commands.describe(name)
async def profileEdit (interaction: discord.Interaction, bio: str, banner: discord.Attachment, name: str, pronouns: str, location: str = "", status: str = "", ):
    class Buttons(discord.ui.View):
        def __init__(self, *, timeout=180):
            super().__init__(timeout=timeout)
        @discord.ui.button(label="All good!",style=discord.ButtonStyle.green)
        async def acceptEdits(self, interaction:discord.Interaction, view: discord.ui.View):
            embed_dict = embed.to_dict()
            with open(f'profiles/{interaction.user}.json', 'w') as f:
              json.dump(embed_dict, f, indent=4)
            print(f"{interaction.user} created a profile")

    embed = discord.Embed(
        title=f"{interaction.user} profile",
        color=4321431
    )

# Set the author
    embed.set_author(
      name=f"Ragecord Utils {version}",
    )

# Add fields
    embed.add_field(
      name="Pronouns",
      value=pronouns,
      inline=False
    )
    embed.add_field(
      name="Status",
      value=status,
      inline=False
    )
    embed.add_field(
      name="Bio",
      value=bio,
      inline=False
  )

    embed.set_thumbnail(url=banner.url)
    embed.set_footer(text="created 4 Ragecord by dainis koknese ")

    await interaction.response.send_message(embed=embed, ephemeral=True, view=Buttons())
    
@tree.command(
    name="profile",
    description="View your or other user profiles",
    guild=discord.Object(id=server_id)
)
async def viewProfile(interaction: discord.Interaction, user: discord.Member = None):
    def json_to_embed(profile_path):
        with open(profile_path, 'r') as profile:
            parsedProfile = json.load(profile)
            profileEmbed = discord.Embed.from_dict(parsedProfile)
            return profileEmbed

    if user == None:
        embed = json_to_embed(f"profiles/{interaction.user}.json")
        embed.set_author(name=f"Ragecord Utils {version}")
        await interaction.response.send_message(embed=embed)
    if user != None:
        try:
            embed = json_to_embed(f"profiles/{user}.json")
            embed.set_author(name=f"Ragecord Utils {version}")
            await interaction.response.send_message(embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message("[Rageutils] ***Errno 1*** File not found. (Does this user have a profile set up?) Stop.")
        
bot.run(token)


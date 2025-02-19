import discord
import json
from discord import app_commands, Embed, ui
from discord.utils import get, format_dt
from discord.ext import commands
from dotenv import load_dotenv
from typing import Literal
import os
from datetime import datetime
intents = discord.Intents.all()
intents.members = True
version = "v.1.1.2-beta"

load_dotenv('.config', override=True)
server_id = os.getenv('CONFIG_SERVER_ID')
token = os.getenv('CONFIG_TOKEN')

bot = commands.Bot(command_prefix="sudo ", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await tree.sync(guild=discord.Object(id=server_id))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"YouTube poops"))
    print(discord.__version__)

@bot.event
async def on_member_join(member):
    sauceRole = 1301977681474224173
    sauceRole = discord.Object(id=patientID)
    await member.add_roles(sauceRole)

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
@app_commands.describe(bio="Your bio", banner="Your banner/image you want displayed on your profile", name="Your name you wish to be referred as", location="Country/location you'd like to display", status="Your short status")
async def profileEdit (interaction: discord.Interaction, bio: str, banner: discord.Attachment, name: str, pronouns: str, colour: Literal["4red", "Eiffel 65 blue", "alien green", "simpson yellow", "annoying orange", "classic white", "YTP brown", "brony pink", "ourple"], location: str = "", status: str = "", birthday: str = ""):
    class Buttons(discord.ui.View):
        def __init__(self, *, timeout=180):
            super().__init__(timeout=timeout)
        @discord.ui.button(label="All good!",style=discord.ButtonStyle.green)
        async def acceptEdits(self, interaction:discord.Interaction, view: discord.ui.View):
            embed_dict = embed.to_dict()
            with open(f'profiles/{interaction.user}.json', 'w') as f:
              json.dump(embed_dict, f, indent=4)
            print(f"{interaction.user} created a profile")
            await interaction.response.send_message("Profile created!")
            
    def colourDetermine():
        match colour:
            case "4red":
                return 7996160
            case "Eiffel 65 Blue":
                return 2183
            case "alien green":
                return 23559
            case "simpson yellow":
                return 16757248
            case "annoying orange":
                return 16738304
            case "classic white":
                return 16777215
            case "brony pink":
                return 16732323
            case "ourple":
                return 10312191
        
        
    embed = discord.Embed(
        title=f"{interaction.user} profile",
        color=colourDetermine()
    )

    embed.set_author(
      name=f"Ragecord Utils {version}",
    )

    embed.add_field(
      name="Pronouns",
      value=pronouns,
      inline=False
    )
    embed.add_field(
      name="Location",
      value=location,
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
    embed.add_field(
      name="Birthday",
      value=birthday,
      inline=False
  )

    embed.set_image(url=banner.url)
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
        try:
            embed = json_to_embed(f"profiles/{interaction.user}.json")
            embed.set_author(name=f"Ragecord Utils {version}")
            await interaction.response.send_message(embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message("[Rageutils] ***Errno 1*** File not found. (Does this user have a profile set up?) Stop.")
    if user != None:
        try:
            embed = json_to_embed(f"profiles/{user}.json")
            embed.set_author(name=f"Ragecord Utils {version}")
            await interaction.response.send_message(embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message("[Rageutils] ***Errno 1*** File not found. (Does this user have a profile set up?) Stop.")
            
 
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
        rageboard = bot.get_channel(1341507240762540147)
        message = await rageboard.send(f"{format_dt(datetime.now(), style='F')}", embed=embed)
        mid = message.id
        thread = await message.create_thread(name=f'Rageboard thread {mid}')

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        if interaction.response.is_done():
            print(f"Error occurred: {error}")
        else:
            await interaction.response.send_message(f"{error}\n## Rageboard modal created successfully, but an ***extremely rare fatal error*** occured. Report this to the development team. Bailing out, you are on your own. Good luck.", ephemeral=True)
        

@tree.command(
    name="post",
    description="Post a thread on Rageboard",
    guild=discord.Object(id=server_id)
)
async def post(interaction:discord.Interaction):
    modal = Postui()
    await interaction.response.send_modal(modal)
bot.run(token)


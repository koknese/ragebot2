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

class ProfileEditUI(ui.Modal, title='Creating a profile'):
        status = ui.TextInput(label='Status', placeholder="Place a quote/feelings here!", style=discord.TextStyle.short)
        pronouns = ui.TextInput(label='Pronouns', placeholder="Your pronouns", style=discord.TextStyle.short)
        birthday = ui.TextInput(label='Birthday', placeholder="Your birthday", style=discord.TextStyle.short, required=False)
        bio = ui.TextInput(label='Bio', placeholder="Your bio", style=discord.TextStyle.long)
        image = ui.TextInput(label='Image link', placeholder="Paste an image link here if you have one!", style=discord.TextStyle.short, required=False)
        
        async def on_submit(self, interaction: discord.Interaction):
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
            
            embed = discord.Embed(
                title=f"{interaction.user} profile",
                color=2183
            )
            
            if self.image != None:
                embed.set_image(url=self.image)
                
            embed.set_author(
              name=f"Ragecord Utils {version}",
            )

            embed.add_field(
              name="Pronouns",
              value=self.pronouns,
              inline=False
            )
            embed.add_field(
              name="Status",
              value=self.status,
              inline=False
            )
            embed.add_field(
              name="Bio",
              value=self.bio,
              inline=False
            )
            embed.add_field(
              name="Birthday",
              value=self.birthday,
              inline=False
            )

            embed.set_footer(text="created 4 Ragecord by dainis koknese ")

            await interaction.response.send_message(embed=embed, ephemeral=True, view=Buttons())

class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @app_commands.command(name='profile-edit', description='Edit your profile!')
    @app_commands.guilds(discord.Object(id=server_id))
    async def profileEdit(self, interaction: discord.Interaction):
        modal = ProfileEditUI()
        await interaction.response.send_modal(modal)

    @app_commands.command(
        name="profile",
        description="View your or other user profiles",
    )
    @app_commands.guilds(discord.Object(id=server_id))
    async def viewProfile(self, interaction: discord.Interaction, user: discord.Member = None):
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
async def setup(bot: commands.Bot):
    await bot.add_cog(Profiles(bot))
import data_management
import os
import discord
import discord_embeds
import discord_logic
import discord_ui
import info_msgs

from discord import app_commands
from discord.ext import commands

# Discord token from environment
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# Bot initialization
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="/start")
bot = commands.Bot(command_prefix='/', intents=intents, activity=activity)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="start", description="Creates a new character")
async def start(interaction: discord.Interaction):
    await discord_logic.create_character(interaction)

@bot.tree.command(name="help", description="Shows all commands")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=discord_embeds.embed_help_msg(interaction))

@bot.tree.command(name="tutorial", description="Shows the tutorial")
async def tutorial(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} - {info_msgs.TUTORIAL_MSG}")

@bot.tree.command(name="fight", description="Makes the player fight a random enemy from current area")
async def fight(interaction: discord.Interaction):
    await discord_logic.begin_fight(interaction, discord_ui.ActionMenu(interaction))

@bot.tree.command(name="boss", description="Makes the player fight the boss of current area")
async def boss(interaction: discord.Interaction):
    await discord_logic.begin_boss_fight(interaction, discord_ui.ActionMenu(interaction))

@bot.tree.command(name="attack", description="Attack enemy fighting the player")
async def attack(interaction: discord.Interaction):
    await discord_logic.attack(interaction)

@bot.tree.command(name="rest", description="Fully recovers the player")
async def rest(interaction: discord.Interaction):
    await discord_logic.rest(interaction)

@bot.tree.command(name="inventory", description="Shows player's inventory")
async def inventory(interaction: discord.Interaction):
    await discord_logic.inventory(interaction)

@bot.tree.command(name="profile", description="Shows player's profile")
async def profile(interaction: discord.Interaction):
    await discord_logic.profile(interaction, None)

@bot.tree.command(name="menu", description="Shows main menu with player's profile and interaction buttons")
async def menu(interaction: discord.Interaction):
    await discord_logic.profile(interaction, discord_ui.PlayerMenu(interaction))

@bot.tree.command(name="shop", description="Shows the shop of the current area")
async def shop(interaction: discord.Interaction):
    await discord_logic.shop(interaction)

@bot.tree.command(name="equipment", description="Shows player's equipment")
async def equipment(interaction: discord.Interaction):
    await discord_logic.equipment(interaction)

@bot.tree.command(name="job", description="Shows player's job info and allows changing it")
async def job(interaction: discord.Interaction):
    await discord_logic.job(interaction)

@bot.tree.command(name="skills", description="Shows player's skills info")
async def skills(interaction: discord.Interaction):
    await discord_logic.show_skills(interaction)

@bot.tree.command(name="dungeon", description="Shows all dungeons in current area")
async def dungeon(interaction: discord.Interaction):
    await discord_logic.dungeon(interaction)

@bot.tree.command(name="duel", description="Makes the player fight another player")
async def duel(interaction: discord.Interaction, enemy_name: str):
    await discord_logic.duel(interaction, enemy_name.lower())

def msgs_to_msg_str(msgs: list) -> str:
    return "\n".join(msgs)

if __name__ == "__main__":
    data_management.load_everything()
    bot.run(DISCORD_TOKEN)
import discord
from discord import app_commands
from discord.ext import commands
import os

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD_ID = 1264525618381455401  # ✅ Your updated server ID
ALLOWED_ROLE_ID = 1264526284298518528  # ✅ The role allowed to use commands

# Initialize bot
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="/", intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot is online as {client.user}")
    try:
        synced = await client.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"✅ Synced {len(synced)} commands.")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

@client.tree.command(name="announce", description="Send a DM to all members with a specific role")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def announce(interaction: discord.Interaction, role: discord.Role, message: str):
    if ALLOWED_ROLE_ID not in [r.id for r in interaction.user.roles]:
        await interaction.response.send_message("❌ You do not have permission to use this command!", ephemeral=True)
        return
    
    members = [member for member in role.members if not member.bot]
    if not members:
        await interaction.response.send_message(f"❌ No members found with the role **{role.name}**.", ephemeral=True)
        return
    
    await interaction.response.send_message(f"📨 Sending messages to **{role.name}**...", ephemeral=True)
    success, fail = 0, 0
    
    for member in members:
        try:
            await member.send(message)
            success += 1
        except:
            fail += 1
    
    await interaction.followup.send(f"✅ **Message sent to {success} members in the role {role.name}.**\n❌ **Failed to send to {fail} members.**", ephemeral=True)

@client.tree.command(name="nickall", description="Adds text to the beginning and end of nicknames for members with a specific role")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def nickall(interaction: discord.Interaction, role: discord.Role, front: str, back: str):
    if ALLOWED_ROLE_ID not in [r.id for r in interaction.user.roles]:
        await interaction.response.send_message("❌ You do not have permission to use this command!", ephemeral=True)
        return
    
    members = [member for member in role.members if member.guild.me.guild_permissions.manage_nicknames]
    if not members:
        await interaction.response.send_message(f"❌ No members found with the role **{role.name}** or lacking permissions.", ephemeral=True)
        return
    
    await interaction.response.send_message(f"🔄 Updating nicknames for members with role **{role.name}**...", ephemeral=True)
    success, fail = 0, 0
    
    for member in members:
        new_nick = f"{front} {member.display_name} {back}".strip()
        try:
            await member.edit(nick=new_nick)
            success += 1
        except:
            fail += 1
    
    await interaction.followup.send(f"✅ **Nicknames updated for {success} members.**\n❌ **Failed for {fail} members.**", ephemeral=True)

@client.tree.command(name="resetnicks", description="Removes all nicknames from members")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def resetnicks(interaction: discord.Interaction):
    if ALLOWED_ROLE_ID not in [r.id for r in interaction.user.roles]:
        await interaction.response.send_message("❌ You do not have permission to use this command!", ephemeral=True)
        return
    
    members = [member for member in interaction.guild.members if member.nick and member.guild.me.guild_permissions.manage_nicknames]
    if not members:
        await interaction.response.send_message("❌ No members with nicknames to reset.", ephemeral=True)
        return
    
    await interaction.response.send_message("🔄 Removing nicknames for all members...", ephemeral=True)
    success, fail = 0, 0
    
    for member in members:
        try:
            await member.edit(nick=None)
            success += 1
        except:
            fail += 1
    
    await interaction.followup.send(f"✅ **Nicknames reset for {success} members.**\n❌ **Failed for {fail} members.**", ephemeral=True)

client.run(TOKEN)

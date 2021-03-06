import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="#", intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="2.0v"))
    client.reaction_roles = []
    
@client.command(aliases=["Clear"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.event
async def on_raw_reaction_add(payload):
    for role, msg, emoji in client.reaction_roles:
        if msg.id == payload.message_id and payload.emoji.name:
            await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    for role, msg, emoji in client.reaction_roles:
        if msg.id == payload.message_id and payload.emoji.name:
            await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
@client.command()
@commands.has_permissions(manage_messages=True)
async def set_reaction(ctx, role: discord.Role=None, msg: discord.Message=None, emoji=None):
    if role != None and msg != None and emoji != None:
        await msg.add_reaction(emoji)
        client.reaction_roles.append((role, msg, emoji))

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} wurde gekickt")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} wurde gebannt")

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_user = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_user:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} wurde Endbannt")
            return


@client.event
async def on_connect():
    print('Email geladen')


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.author != message.author.bot:
        if not message.guild:
            await client.get_guild(765213091398287361).get_channel(765213091398287368).send(f"**User meniton {message.author.mention}**\n**Username: {message.author}**\n**User-ID: {message.author.id}**\n\n__**Nachricht:**__\n**{message.content}**")
    await client.process_commands(message)


@client.command()
@commands.has_permissions(manage_messages=True)
async def mail(ctx, member: discord.Member, *, text):
    await member.send(text)


@client.event
async def on_resumed():
    print('Email neugeladen')

client.run(os.environ["TOKEN"],  reconnect=True)

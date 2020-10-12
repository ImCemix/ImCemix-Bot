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

@client.command()
async def teamhelp(ctx):
    embed = discord.Embed(color = discord.Colour.green())
    embed.add_field(name="ImCemix Regelwerk", value="Wir haben ein kleines, aber strenges Regelwerk auf unserem Server. Bitte lesen Sie sie durch und nehmen Sie sie mit an Bord. Wenn Sie eine Regel nicht verstehen oder einen Vorfall melden müssen, senden Sie bitte eine direkte Nachricht an <@747477908880097481>!", inline=False)
    embed.add_field(name="§1.1 Namensgebung", value="Nicknames dürfen keine beleidigenden oder anderen verbotenen oder geschützen Namen oder Namensteile enthalten.", inline=False)
    embed.add_field(name="§1.2 Avatar", value="Avatare dürfen keine pornographischen, rassistischen oder beleidigenden Inhalte beinhalten.", inline=False)
    embed.add_field(name="§2.1 Umgangston", value="Der Umgang mit anderen Discord Benutzern sollte stets freundlich sein. Verbale Angriffe gegen andere User sind strengstens untersagt.", inline=False)
    embed.add_field(name="§2.2 Gespräche aufnehmen", value="Das Mitschneiden von Gesprächen ist auf dem gesamten Server nur nach Absprache mit den anwesenden Benutzern des entsprechenden Channels erlaubt. Willigt ein User nicht der Aufnahme ein, ist die Aufnahme des Gesprächs verboten.", inline=False)
    embed.add_field(name="§2.3 Abwesenheit", value="Bei längerer Abwesenheit wird der Benutzer gebeten in den entsprechnden AFK-Channel zu gehen.", inline=False)
    embed.add_field(name="§3.1 Kicken/Bannen", value="Ein Kick oder Bann ist zu keinem Zeitpunkt unbegründet, sondern soll zum Nachdenken der eigenen Verhaltensweise anregen. Unangebrachte Kicks/Banns müssen den zuständigen Admins gemeldet werden.", inline=False)
    embed.add_field(name="§3.2 Discord Rechte", value="Discord Rechte werden nicht wahllos vergeben, sondern dienen immer einem bestimmten Grund. Bei Bedarf von Rechten kann sich an den zuständigen Admin gewandt werden.", inline=False)
    embed.add_field(name="§3.3 Weisungsrecht", value="Server Admins, Moderatoren oder anderweitig befugte Admins haben volles Weisungsrecht. Das Verweigern einer bestimmten Anweisung kann zu einem Kick oder Bann führen.", inline=False)
    embed.add_field(name="§4.1 Werbung", value="Jegliche Art von Werbung ist auf diesem Server untersagt. Ggf. kann sich an einen zuständigen Admin gewandt werden, um über eine Möglichkeit zur Werbung zu verhandeln.", inline=False)
    embed.add_field(name="§4.2 Datenschutz", value="Private Daten wie Telefonnummern, Adressen, Passwörter und ähnlichem dürfen nicht öffentlich ausgetauscht werden.", inline=False)
    embed.add_field(name="§5.1 Eigene Musik/Töne", value="Das Einspielen von eigener Musik, oder das Übetragen von anderen nicht erwünschten Tönen ist untersagt.", inline=False)
    embed.add_field(name="§5.2 Bots (insb. Musik-Bots)", value="Es dürfen keine Bots mit dem Discord Server verbunden werden. Bots dürfen nur in ausgewiesenen Channels verbunden werden und auch nur dann, wenn kein weiterer Bot in dem Channel aktiv ist.", inline=False)
    embed.add_field(name="§6.1 Meldepflicht", value="Es sind alle Benutzer angehalten, die Discord-Server Regeln zu beachten. Sollte ein Regelverstoß von einem Benutzer erkannt werden, ist dieser umgehend einem Admin zu melden.", inline=False)
    embed.set_footer(text="Zum akzeptieren hier klicken.")
    await ctx.send(embed=embed)
    
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

def check_team(ctx):
    return client.get_guild(747436143863136288).get_role(764814416188276769) in ctx.author.roles


@client.event
async def on_connect():
    print('Email geladen')


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.author != message.author.bot:
        if not message.guild:
            await client.get_guild(747436143863136288).get_channel(764814611387645973).send(f"**User meniton {message.author.mention}**\n**Username: {message.author}**\n**User-ID: {message.author.id}**\n\n__**Nachricht:**__\n**{message.content}**")
    await client.process_commands(message)


@client.command()
@commands.has_permissions(manage_messages=True)
@commands.check(check_team)
async def mail(ctx, member: discord.Member, *, text):
    await member.send(text)


@client.event
async def on_resumed():
    print('Email neugeladen')

client.run(os.environ["TOKEN"],  reconnect=True)

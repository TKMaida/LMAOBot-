import requests
import json
import discord
from discord.ext import commands
import os
from keep_alive import keep_alive


# Get prefixes from file
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix, intents=intents)

@client.event
async def on_ready():
    print("LMAOBot online as {0.user}".format(client))


@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@client.command()
async def changeprefix(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


def check_range(rank, x, y):
    if x < rank < y:
        return True


def assign_role(rank, user):
    if check_range(rank, 5000, 10000):
        return discord.utils.get(user.guild.roles, name="Top 10k")

    if check_range(rank, 4000, 5000):
        return discord.utils.get(user.guild.roles, name="Top 5k")

    if check_range(rank, 3000, 4000):
        return discord.utils.get(user.guild.roles, name="Top 4k")

    if check_range(rank, 2000, 3000):
        return discord.utils.get(user.guild.roles, name="Top 3k")

    if check_range(rank, 1000, 2000):
        return discord.utils.get(user.guild.roles, name="Top 2k")

    if check_range(rank, 500, 1000):
        return discord.utils.get(user.guild.roles, name="Top 1k")

    if check_range(rank, 400, 500):
        return discord.utils.get(user.guild.roles, name="Top 500")

    if check_range(rank, 300, 400):
        return discord.utils.get(user.guild.roles, name="Top 400")

    if check_range(rank, 200, 300):
        return discord.utils.get(user.guild.roles, name="Top 300")

    if check_range(rank, 100, 200):
        return discord.utils.get(user.guild.roles, name="Top 200")

    if check_range(rank, 50, 100):
        return discord.utils.get(user.guild.roles, name="Top 100")

    if check_range(rank, 1, 50):
        return discord.utils.get(user.guild.roles, name="Top 50")


@client.command()
async def link(ctx, url):
    id = url[-17:]
    user = ctx.author
    profileRequest = requests.get(
        f"https://new.scoresaber.com/api/player/{id}/full"
    ).json()
    profileName = profileRequest["playerInfo"]["playerName"]

    if "LMAO|" in profileName.replace(" ", ""):
        await user.add_roles(discord.utils.get(ctx.guild.roles, name="LMAOers"))

    """
  PlayerInfo Keys:
  'avatar':
  'badges':
  'banned':
  'country':
  'countryRank':
  'history': 
  'inactive':
  'permissions':
  'playerId':
  'playerName':
  'pp':
  'rank':
  'role':
  """
    rank = int(profileRequest["playerInfo"]["rank"])

    await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Newbie"))
    await user.add_roles(assign_role(rank, ctx.author))
    await ctx.send(f"{user.mention} Your profile has been successfully linked")


role_list = [
    806706721866252368,  # 10k
    806706723934830632,  # 5k
    806919195140554802,  # 4k
    806919221862727690,  # 3k
    806919363294396466,  # 2k
    806706725549506590,  # 1k
    806706785746419712,  # 500
    806706787243917333,  # 400
    806706790792167444,  # 300
    806706792650113044,  # 200
    806706871700422656,  # 100
    806714230237691934,  # 50
]


@client.command()
async def update(ctx, url):

    id = url[-17:]
    user = ctx.author
    profileRequest = requests.get(f"https://new.scoresaber.com/api/player/{id}/full").json()
    profileName = profileRequest["playerInfo"]["playerName"]

    if "LMAO|" in profileName.replace(" ", ""):
        await user.add_roles(discord.utils.get(ctx.guild.roles, name="LMAOers"))

    rank = int(profileRequest["playerInfo"]["rank"])

    def check_range(rank, x, y):
        if x < rank < y:
            return True

    for role in user.roles:
        if role.id in role_list:
            await user.remove_roles(discord.utils.get(ctx.guild.roles, id=role.id))

    await user.add_roles(assign_role(rank, ctx.author))
    await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Newbie"))

    await ctx.send(f"Sucessfully updated roles for {user.mention} ")


@client.event
async def on_member_join(member):
    await member.send(
        "Welcome to the LMAO Clan discord! Make sure to link your scoresaber profile in #bot-commands!"
    )
    role = discord.utils.get(member.guild.roles, name="Newbie")
    await member.add_roles(role)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "lol" in message.content.split():
        await message.channel.purge(limit=1)
        await message.channel.send("You will be sorry for that")
    await client.process_commands(message)
    
keep_alive()
client.run(os.getenv("TOKEN"))

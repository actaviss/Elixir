import discord
from discord.ext import commands
import pymongo
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

from cogs.AntiChannel import AntiChannel
from cogs.AntiRemoval import AntiRemoval
from cogs.AntiPermissions import AntiPermissions
from cogs.AntiWebhook import AntiWebhook

mongoClient = pymongo.MongoClient(os.environ["MONGO_DB_URL"].replace("<password>", os.environ["MONGO_DB_PASSWORD"]))
db = mongoClient.get_database("botdb").get_collection("whitelists")

webhook = discord.Webhook.partial(
    os.environ["WEBHOOK_ID"],
    os.environ["WEBHOOK_TOKEN"],
    adapter=discord.RequestsWebhookAdapter(),
)

client = commands.Bot(description="elixir, by mitch", command_prefix=">")

client.add_cog(AntiChannel(client, db, webhook))
client.add_cog(AntiRemoval(client, db, webhook))
client.add_cog(AntiPermissions(client, db, webhook))
client.add_cog(AntiWebhook(client, db, webhook))

def is_owner(ctx):
    return ctx.message.author.id == 148471759211855872

def is_whitelisted(ctx):
    return ctx.message.author.id in db.find_one({ "guild_id": ctx.guild.id })["users"] or ctx.message.author.id == 148471759211855872
    
def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 148471759211855872


@client.event
async def on_member_join(member):
    whitelistedUsers = db.find_one({ "guild_id": member.guild.id })["users"]
    if member.bot:
        async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.bot_add):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await member.ban()
            await i.user.ban()


@client.event
async def on_ready():
    for i in client.guilds:
            if not db.find_one({ "guild_id": i.id }):
                db.insert_one({
                    "users": [],
                    "guild_id": i.id
                })
                
    webhook.send(embed=discord.Embed(description=f"Elixir is online | Loaded {len(client.guilds)} whitelists"))

    print("Elixir loaded")

@client.event
async def on_guild_join(guild):
    db.insert_one({
        "users": [guild.owner_id],
        "guild_id": guild.id
    })

    webhook.send(embed=discord.Embed(description=f"Joined {guild.name} - {guild.member_count} members"))

@client.event
async def on_guild_leave(guild):
    db.delete_one({ "guild_id": guild.id })

    webhook.send(embed=discord.Embed(description=f"Left {guild.name} - {guild.member_count} members"))
           

@client.command()
@commands.check(is_whitelisted)
async def whitelist(ctx, user: discord.User):
    if not user:
        await ctx.send("You need to provide a user.")
        return

    if not isinstance(user, discord.User):
        await ctx.send("Invalid user.")
        return

    if user.id in db.find_one({ "guild_id": ctx.guild.id })["users"]:
        await ctx.send("That user is already in the whitelist.")
        return

    db.update_one({ "guild_id": ctx.guild.id }, { "$push": { "users": user.id }})

    await ctx.send(f"{user} has been added to the whitelist.")

@client.command()
@commands.check(is_whitelisted)
async def dewhitelist(ctx, user: discord.User):
    if not user:
        await ctx.send("You need to provide a user")

    if not isinstance(user, discord.User):
        await ctx.send("Invalid user")

    if user.id not in db.find_one({ "guild_id": ctx.guild.id })["users"]:
        await ctx.send("That user is not in the whitelist.")
        return

    db.update_one({ "guild_id": ctx.guild.id }, { "$pull": { "users": user.id }})

    await ctx.send(f"{user} has been removed from the whitelist.")

@client.command()
@commands.check(is_whitelisted)
async def massunban(ctx):
    async for i in ctx.guild.bans():
        print(i)

@client.command()
@commands.check(is_whitelisted)
async def whitelisted(ctx):
    data = db.find_one({ "guild_id": ctx.guild.id })['users']

    embed = discord.Embed(title=f"Whitelist for {ctx.guild.name}", description="")

    for i in data:
        embed.description += f"{client.get_user(i)} - {i}\n"

    await ctx.send(embed=embed)

@client.command()
async def info(ctx):
    await ctx.send(embed=discord.Embed(title="Elixir Info", description=f"{len(client.guilds)} servers, {len(client.users)} users | Database is {'connected' if db.find_one({ 'guild_id': ctx.guild.id })['users'] else 'disconnected'}."))

client.run(os.environ["NzQwMjMzNzYwOTI2MzM0OTc2.XymCaQ.NU8P6ikN2kDWvQ54l6niV1QcsV0"])

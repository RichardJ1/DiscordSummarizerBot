# Hello
import discord
from discord.ext import commands
from discord.ext import tasks
import random
from datetime import datetime
import asyncio
import psutil
from xkcd import *
import os
from keepAlive import keepAlive

intents = discord.Intents.all()
#intents = discord.Intents.default()
prefixes = ["x!", "X!", "sudo ", "Sudo "]
bot = commands.Bot(command_prefix = prefixes, case_insensitive = True, intents = intents) # intents = intents
bot.remove_command("help")
#bot = commands.Bot(command_prefix = "xkcd ", case_insensitive = True, intents = intents)
#bot.remove_command("help")


xkcdWebsiteURL = "https://xkcd.com/"
CueBotTOPGGURL = "https://top.gg/bot/747163157318860940"
errorEmoji = "<:error:759595263341494292>"

# bot on initialization
@bot.event
async def on_ready():
	
	bot.starttime = datetime.now()
	await bot.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = f"{len(bot.users)} Users • x!help"))
	print(f"""
   _____           ____        _   
  / ____|         |  _ \      | |  
 | |    _   _  ___| |_) | ___ | |_ 
 | |   | | | |/ _ \  _ < / _ \| __|
 | |___| |_| |  __/ |_) | (_) | |_ 
  \_____\__,_|\___|____/ \___/ \__|
                                   \n""")

# on join server event
@bot.event
async def on_guild_join(guild):
	await bot.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = f"{len(bot.users)} Users | x!help"))
	print("JOINED Server")

# on exit server event
@bot.event
async def on_guild_remove(guild):
	await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(type = discord.ActivityType.watching, name = f"{len(bot.users)} Users | x!help"))
	print("LEFT Server")

# on member join event
@bot.event
async def on_member_join(member):
	await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(type = discord.ActivityType.watching, name = f"{len(bot.users)} Users | x!help"))
	print(f"MEMBER Left Server ({member.guild.id} - {member.id}")

# on member exit event
@bot.event
async def on_member_remove(member):
	await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(type = discord.ActivityType.watching, name = f"{len(bot.users)} Users | x!help"))
	print(f"MEMBER Left Server ({member.guild.id} - {member.id}")

# on CommandNotFound event
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(f"{errorEmoji} That isn't a valid command \nUse `x!help` to view all the commands")

# test
@bot.command(aliases=['testingcom'])
async def testing(ctx):
	print(bot.user.name)
	print(bot.user.avatar.url)
	embed = discord.Embed()
	embed.set_image(url=bot.user.avatar.url)

	await ctx.send(embed=embed)

# embed test
@bot.command(aliases=['emtest'])
async def testembed(ctx):
	embed = discord.Embed(title = "XKCD Command Page", description = "`x!xkcd` (aliases: `comic`, `sudo`) \n\nUsage: \n`x!xkcd` returns the latest xkcd comic \n `x!xkcd 999` returns xkcd 999 \n`x!xkcd random` returns a random xkcd",color = 0xFFFFFE, timestamp = datetime.utcnow())
	embed.set_author(name="test")
	embed.add_field(name="test", value="test", inline=False)
	embed.set_footer(text="test")
	await ctx.send(embed=embed)


# xkcd command
@bot.command(aliases=["comic", "sudo"])
async def xkcd(ctx, *, query = None):
	print("XKCD Command Called (1)")
	latest = getLatestComicNum()
	com = None
	rand = None

  # return comics
	if not query:
		com = Comic(latest)
	
	elif query.isdigit():
		try:
			com = Comic(query)
		except:
			await ctx.send(f"{errorEmoji} That comic is out of range. \nMake sure your number is between 1 and `{latest}`.")
	
	elif query.lower().startswith("r"):
		rand = random.randint(1, latest)
		com = Comic(rand)
	
	
	elif query.lower().startswith("h"):
		embed = discord.Embed(title = "XKCD Command Page", description = "`x!xkcd` (aliases: `comic`, `sudo`) \n\nUsage: \n`x!xkcd` returns the latest xkcd comic \n `x!xkcd 999` returns xkcd 999 \n`x!xkcd random` returns a random xkcd",color = 0xFFFFFE, timestamp = datetime.utcnow())
		embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
		embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
		embed.set_thumbnail(url = bot.user.avatar.url)
		await ctx.send(embed = embed)

	else:
		await ctx.send(f"{errorEmoji} I didn't understand that \nUse `x!help` for help, or type `x!help xkcd` for help on this command")
	
	if com:
		embed = discord.Embed(title = f"{com.getTitle()} (#`{rand if rand else query if query else latest}`)", description = com.getAltText(), color = 0xFFFFFE, timestamp = datetime.utcnow())
		embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
		embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
		embed.set_image(url = com.getImageLink())
		await ctx.send(embed = embed)
    # await ctx.send(f"Number: {rand if rand else query if query else latest} \nTitle: {com.getTitle()} \nAlt Text: {com.getAltText()}")
    # await ctx.send(com.getImageLink())
	
	print("XKCD Command Called")

# explain commmand (Uses the getExplanation() feature from the xkcd python API. It's not perfect, but it's much better than trying to do it myself.)

@bot.command()
async def kill(ctx):
	await ctx.trigger_typing()
	if ctx.author.id in [410590963379994639, 665633515756585031]:
		await ctx.send(f"{bot.checkmarkEmoji} Ending process! (start manually in repl)")
		await bot.close()
	else:
		await ctx.send(f"{bot.errorEmoji} You do not have access to use this command!")


@bot.command(aliases=["?", "exp", "explainxkcd", "man"])
async def explain(ctx, *, query = None):
  latest = getLatestComicNum()

  if not query:
    await ctx.send(f"Here is the explaination for the latest comic, {latest} - \"{Comic(latest).getTitle()}\" \n{Comic(latest).getExplanation()}")

  elif query.isdigit():
    try:
      await ctx.send(f"Here is the explaination for {query} - \"{Comic(query).getTitle()}\" \n{Comic(query).getExplanation()}")
    except:
      await ctx.send(f"I couldn't find that. Make sure you give a number between 1 and {latest}")

  elif query.lower().startswith("r"):
    rand = random.randint(1, latest)
    await ctx.send(f"Here is the explanation for a random comic, {rand} - \"{Comic(rand).getTitle()}\" \n{Comic(rand).getExplanation()}")
	

  elif query.lower().startswith("h"):
    embed = discord.Embed(title = "EXPLAIN Command Page", description = "`x!explain` (aliases: `?`, `exp`, `man`) \n\nUsage: \n`x!explain` returns the latest xkcd explanation \n `x!explain 999` returns the explanation for xkcd 999 \n`x!explain random` returns an explanation for a random xkcd",color = 0xFFFFFE, timestamp = datetime.utcnow())
    embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
    embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
    embed.set_thumbnail(url = bot.user.avatar.url)

    await ctx.send(embed = embed)

  else:
    await ctx.send(f"{errorEmoji} I didn't understand that. \nUse `x!help` for help, or type `x!help explain` for help on this command")

  print("EXPLAIN Command Called")

# link command
@bot.command(aliases=["url"])
async def link(ctx, *, query = None):
  latest = getLatestComicNum()

  # return links
  if not query:
    await ctx.send(f"Here is the link to the latest comic, {latest} - \"{Comic(latest).getTitle()}\". \nhttps://www.xkcd.com/{latest}")

  elif query.isdigit():
    try:
      await ctx.send(f"Here is the link to {query} - \"{Comic(query).getTitle()}\" \nhttps://www.xkcd.com/{query}")
    except:
      await ctx.send(f"I couldn't find that. Make sure you give a number between 1 and {latest}")

  elif query.lower().startswith("r"):
    rand = random.randint(1, latest)
    await ctx.send(f"Here is the link to a random comic, {rand} - \"{Comic(rand).getTitle()}\" \nhttps://www.xkcd.com/{rand}")
	

  elif query.lower().startswith("h"):
    embed = discord.Embed(title = "LINK Command Page", description = "`x!link` (alias: `url`) \n\nUsage: \n`x!link` returns the latest xkcd link \n `x!link 999` returns the link to xkcd 999 \n`x!link random` returns a random xkcd link",color = 0xFFFFFE, timestamp = datetime.utcnow())
    embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
    embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
    embed.set_thumbnail(url = bot.user.avatar.url)
    await ctx.send(embed = embed)

  else:
    await ctx.send(f"{errorEmoji} I didn't understand that.\nUse `x!help` for help, or type `x!help link` for help on this command")

  print("LINK Command Called")

# whatif command
@bot.command(aliases=["wif"])
async def whatif(ctx, *, query = None):
  await ctx.send("This feature is temporarily unavailable. Check out the What If? site at https://what-if.xkcd.com/")
  print("1")
  latest = getLatestWhatIfNum()
  print("2")

  if not query:
    await ctx.send(f"Here is the latest What If? post, {latest} - \"{getWhatIf(latest).getTitle()}\" \n{getWhatIf(latest).getLink()}")

  elif query.isdigit():
    try:
      await ctx.send(f"Here is What If? #{query} - \"{getWhatIf(query).getTitle()}\" \n{getWhatIf(query).getLink()}")
    except:
      await ctx.send(f"I couldn't find that. Make sure you give a number between 1 and {latest}")

  elif query.lower().startswith("r"):
    rand = random.randint(1, latest)
    await ctx.send(f"Here is a random What If? article, {rand} - \"{getWhatIf(rand).getTitle()}\" \n{getWhatIf(rand).getLink()}")

  elif query.lower().startswith("h"):
    embed = discord.Embed(title = "WHAT IF? Command Page", description = "`x!whatif` (alias: `wif`) \n\nUsage: \n`x!whatif` returns the latest What If? article \n `x!whatif 17` returns What If? #17 \n`x!whatif random` returns a random What If? article",color = 0xFFFFFE, timestamp = datetime.utcnow())
    embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
    embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
    embed.set_thumbnail(url = bot.user.avatar.url)
    await ctx.send(embed = embed)

  else:
    await ctx.send(f"{errorEmoji} I didn't understand that. \nUse `x!help` for help, or type `x!help whatif` for help on this command")


  print("WHAT IF Command Called")

# bun command
@bot.command()
async def bun(ctx):
    await ctx.send(":gear: Under Development")
    print("BUN Command Called")

# secret command
@bot.command()
async def secret(ctx):
	message = await ctx.send("This is not the secret command")
	await asyncio.sleep(3)
	await message.edit(content = "Just kidding, it is")
	print("SECRET Command Called")

# help command
@bot.command(aliases=["info"])
async def help(ctx, *, query = None):

	if not query:
		embed = discord.Embed(title = "Help Page", color = 0xFFFFFE, timestamp = datetime.utcnow())
		embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
		embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
		embed.set_thumbnail(url = bot.user.avatar.url)
		
		embed.add_field(name = "Main Commands", value = "•  `x!xkcd` returns the latest xkcd comic \n• `x!xkcd 999` returns xkcd 999\n• `x!xkcd random` returns a random xkcd\n• `x!xkcd help` shows a help page\n\nTo get explanations, links, and What If? articles, just replace `xkcd` with `exp`, `link`, or `whatif`.", inline = False)


		embed.add_field(name = "Other Stuff", value = "`x!help` (`x!info`)\nreturns this page \n`x!botinfo` (`x!binfo`)\nreturns info about the bot\n`x!ping` (`x!latency`)\nreturns the bot's latency and other statistics\n\n P.S. You can also write `sudo ` in place of `x!`", inline = False)

		await ctx.send(embed = embed)
		print("HELP Command Called")

	else:
		if (query.lower() == "xkcd") or (query.lower() == "comic") or (query.lower() == "sudo"):
			embed = discord.Embed(title = f"{query.upper()} Command Page", description = "`x!xkcd` (aliases: `comic`, `sudo`) \n\nUsage: \n`x!xkcd` returns the latest xkcd comic \n `x!xkcd 999` returns xkcd 999 \n`x!xkcd random` returns a random xkcd",color = 0xFFFFFE, timestamp = datetime.utcnow())
			embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
			embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
			embed.set_thumbnail(url = bot.user.avatar.url)

			await ctx.send(embed = embed)
			print(f"HELP ({query.upper()}) Command Called")
		
		elif (query.lower() == "explain") or (query.lower() == "?") or (query.lower() == "exp"):
			embed = discord.Embed(title = f"{query.upper()} Command Page", description = "`x!explain` (aliases: `?`, `exp`) \n\nUsage: \n`x!explain` returns the latest xkcd explanation \n `x!explain 999` returns the explanation for xkcd 999 \n`x!explain random` returns an explanation for a random xkcd",color = 0xFFFFFE, timestamp = datetime.utcnow())
			embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
			embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
			embed.set_thumbnail(url = bot.user.avatar.url)

			await ctx.send(embed = embed)
			print(f"HELP ({query.upper()}) Command Called")
		
		elif (query.lower() == "link") or (query.lower() == "url"):
			embed = discord.Embed(title = f"{query.upper()} Command Page", description = "`x!link` (alias: `url`) \n\nUsage: \n`x!link` returns the latest xkcd link \n `x!link 999` returns the link to xkcd 999 \n`x!link random` returns a random xkcd link",color = 0xFFFFFE, timestamp = datetime.utcnow())
			embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
			embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
			embed.set_thumbnail(url = bot.user.avatar.url)

			await ctx.send(embed = embed)
			print(f"HELP ({query.upper()}) Command Called")
		
		elif (query.lower() == "whatif") or (query.lower() == "wif"):
			embed = discord.Embed(title = f"{query.upper()} Command Page", description = "`x!whatif` (alias: `wif`) \n\nUsage: \n`x!whatif` returns the latest What If? article \n `x!whatif 17` returns What If? #17 \n`x!whatif random` returns a random What If? article", color = 0xFFFFFE, timestamp = datetime.utcnow())
			embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
			embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
			embed.set_thumbnail(url = bot.user.avatar.url)

			await ctx.send(embed = embed)
			print(f"HELP ({query.upper()}) Command Called")

		elif (query.lower() == "help") or (query.lower() == "info"):
			await ctx.send("Really?")
			print(f"HELP ({query.upper()}) Command Called")

		elif (query.lower() == "botinfo") or (query.lower() == "binfo"):
			await ctx.send("This command returns information about the bot \nRun `x!botinfo` or `x!binfo`")
			print(f"HELP ({query.upper()}) Command Called")
			
		elif (query.lower() == "ping") or (query.lower() == "latency"):
			await ctx.send("This command returns the latency or response time of the bot \nRun `x!ping` or `x!latency`")
			print(f"HELP ({query.upper()}) Command Called")
		
		else:
			await ctx.send(f"{errorEmoji} Sorry, but `{query}` isn't a valid command\nView all the commands with `x!help`")

# botinfo command
@bot.command(aliases=["binfo"])
async def botinfo(ctx):
	embed = discord.Embed(title = "Bot Info", color = 0xFFFFFE, timestamp = datetime.utcnow())
	embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
	embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
	embed.set_thumbnail(url = bot.user.avatar.url)
	embed.add_field(name = "Developer", value = "Main: <@665633515756585031> (Owner)\nDesign: <@410590963379994639>", inline = False)
	embed.add_field(name = "Language", value = "Python and the [discord.py](https://discordpy.readthedocs.io/en/latest/) library", inline = False)
	embed.add_field(name = "Hosting Platform", value = "[Repl.it](https://repl.it/)", inline = False)
	embed.add_field(name = "Github Repository", value = "[Link](https://github.com/NotRichardNixon/CueBot-Github)", inline = False)
	
	await ctx.send(embed = embed)
	print("BOTINFO Command Called")

# ping command
@bot.command(aliases=["latency"])
async def ping(ctx):
	print("PING Command Called")
	time = datetime.now() - bot.starttime
	days = time.days
	hours, remainder = divmod(time.seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	dunit = "day" if days == 1 else "days"
	hunit = "hour" if hours == 1 else "hours"
	munit = "minute" if minutes == 1 else "minutes"
	sunit = "second" if seconds == 1 else "seconds"
	
	embed = discord.Embed(title = "🏓 Pong!", color = 0xFFFFFE, timestamp = datetime.utcnow())
	embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar.url)
	embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
	embed.add_field(name = ":signal_strength: Latency", value = (f"`{round(bot.latency * 1000)}`ms"), inline = True)
	embed.add_field(name = ":robot: Hardware", value = (f"Cores → `{psutil.cpu_count()}` \nCPU → `{round(psutil.cpu_percent())}`% \nRAM → `{round(psutil.virtual_memory()[2])}`%"), inline = True)
	embed.add_field(name = ":chart_with_upwards_trend: Uptime", value = (f"`{days}` {dunit} \n`{hours}` {hunit} \n`{minutes}` {munit} \n`{seconds}` {sunit}"), inline = True)
	await ctx.send(embed = embed)
	
	print("PING Command Called (2)")

keepAlive()
bot.run(os.environ.get("token"), reconnect = True) #bot = True,
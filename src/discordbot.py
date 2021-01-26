import discord
from discord.ext import commands
from name_that_hash import runner
import json
import cracking
import hashsearch


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def hash(ctx, hash):
    types = []
    JSON = json.loads(runner.api_return_hashes_as_json(hash.split("\n")))
    [types.append(i) for i in JSON[hash]]
    embed_types = discord.Embed(title=hash, colour=discord.Colour(0xFF9F1C))
    for i in range(len(types)):
        if i == 6:
            break
        embed_types.add_field(name=types[i]['name'], value=types[i]['description'], inline=False)
    await ctx.send(embed=embed_types)

bot.run('MzM0NzExNTYzMzI1ODAwNDU5.WWY6bw.kpE4pBua63XpIYJxvVyYHIINvz8')
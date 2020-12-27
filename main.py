import requests
import json
from discord.ext import commands
import discord
import os
import asyncio
bot = commands.Bot(command_prefix='[')

headers={
    'x-rapidapi-key': os.environ['APIKEY'],
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

@bot.event
async def on_ready():
    print(f'Activated as {bot.user.name}, {bot.user.id}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='[help'))

@bot.command()
async def searcht(ctx, arg):
    argbckup = arg.title()
    arg = arg.replace(' ', '%20')
    embed = discord.Embed(title=f':mag_right: Search Results: {argbckup} (?/?)', color=discord.Color.green(), description='Loading...')
    sended = await ctx.send(embed=embed)
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/search/"+arg
    response = requests.request("GET", url, headers=headers).json()
    result_num = response['api']['results']
    if result_num == 0:
        embed = discord.Embed(title=f':mag_right: Search Results: {argbckup} (0/0)', color=discord.Color.red(), description='None')
        await sended.edit(embed=embed)
        return None
    embed = []
    j = 0
    if result_num % 12 == 0: embed_num = result_num / 12
    else: embed_num = int(result_num / 12) + 1
    for i in range(0, embed_num):
        embed.append(discord.Embed(title=f':mag_right: Search Results: {argbckup} ({i+1}/{embed_num})', color=discord.Color.green(), description=f'I found {result_num} teams!'))
        embed[i].set_footer(text='❗ You need to clear the emoji and press it again when not on a server!')
        for j in range(j, result_num):
            embed[i].add_field(name=str(j+1)+'. '+response['api']['teams'][j]['name'], value=f"`{response['api']['teams'][j]['venue_name']}` (id: {response['api']['teams'][j]['team_id']})")
            if j >=  (i+1) * 12 - 1:
                j += 1
                break
    page = 0
    await sended.edit(embed=embed[0])
    await sended.add_reaction('⬅')
    await sended.add_reaction('➡')
    def checkemoji(reaction, user):
        check = reaction.emoji == '➡' or reaction.emoji == '⬅'
        return user == ctx.message.author and check and reaction.message == sended
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=checkemoji)
        except asyncio.TimeoutError: break
        if reaction.emoji == '➡':
            if page == embed_num-1: 
                page = 0
            else: 
                page += 1
        elif reaction.emoji == '⬅':
            if page == 0: 
                page = embed_num-1
            else: 
                page -= 1
        if isinstance(ctx.channel, discord.channel.TextChannel):
            await sended.remove_reaction(emoji=reaction.emoji, member=user)
        await sended.edit(embed=embed[page])

@bot.command()
async def searchp(ctx, arg):
    argbckup = arg.title()
    arg = arg.replace(' ', '%20')
    embed = discord.Embed(title=f':mag_right: Search Results: {argbckup} (?/?)', color=discord.Color.green(), description='Loading...')
    sended = await ctx.send(embed=embed)
    url = "https://api-football-v1.p.rapidapi.com/v2/players/search/"+arg
    response = requests.request("GET", url, headers=headers).json()
    result_num = response['api']['results']
    if result_num == 0:
        embed = discord.Embed(title=f':mag_right: Search Results: {argbckup} (0/0)', color=discord.Color.red(), description='None')
        await sended.edit(embed=embed)
        return None
    embed = []
    j = 0
    if result_num % 12 == 0: embed_num = result_num / 12
    else: embed_num = int(result_num / 12) + 1
    for i in range(0, embed_num):
        embed.append(discord.Embed(title=f':mag_right: Search Results: {argbckup} ({i+1}/{embed_num})', color=discord.Color.green(), description=f'I found {result_num} players!'))
        embed[i].set_footer(text='❗ You need to clear the emoji and press it again when not on a server!')
        for j in range(j, result_num):
            embed[i].add_field(name=str(j+1)+'. '+response['api']['players'][j]['player_name'], value=f"`{response['api']['players'][j]['position']}` (id: {response['api']['players'][j]['player_id']})")
            if j >=  (i+1) * 12 - 1:
                j += 1
                break
    page = 0
    await sended.edit(embed=embed[0])
    await sended.add_reaction('⬅')
    await sended.add_reaction('➡')
    def checkemoji(reaction, user):
        check = reaction.emoji == '➡' or reaction.emoji == '⬅'
        return user == ctx.message.author and check and reaction.message == sended
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=checkemoji)
        except asyncio.TimeoutError: break
        if reaction.emoji == '➡':
            if page == embed_num-1: 
                page = 0
            else: 
                page += 1
        elif reaction.emoji == '⬅':
            if page == 0: 
                page = embed_num-1
            else: 
                page -= 1
        if isinstance(ctx.channel, discord.channel.TextChannel):
            await sended.remove_reaction(emoji=reaction.emoji, member=user)
        await sended.edit(embed=embed[page])

@bot.command()
async def player(ctx, arg):
    pass
    
        
@bot.command()
async def invite(ctx):
    await ctx.send('https://discord.com/oauth2/authorize?client_id=790497395217137693&scope=bot&permissions=1074265168')

@bot.command()
async def team(ctx, arg):
    pass

@bot.command()
async def embed(ctx):
    embed = discord.Embed(title=':rocket: TEST', color=discord.Colour.green())
    embed.add_field(name='j', value='Success')
    await ctx.send(embed=embed)

bot.run(os.environ['TOKEN'])
bot.remove_command('help')
import discord
from discord.ext import commands
import urllib
import json
from typing import Optional
from datetime import datetime
from discord import Member, Embed

bot_token = '####################' #PUT YOUR TOKEN HERE
serverChannelId = '###################' # PUT YOUR DISCORD SERVER CHANNEL ID

client = discord.Client()
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'))
client.get_channel(serverChannelId)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))

@client.event
async def on_message(message):
    message_data = message.content
    if message.author == client.user:
        return

    if message.content.startswith('!info'):
        message_user = message_data.split(' ')
        userIdraw = message_user[1].replace('<@!', '')
        userId = userIdraw.replace('>', '')
        target = client.get_user(int(userId))
        print(target)
    
        # target = user
        embed = discord.Embed(
            title = 'User info',
            colour = discord.Colour(0x3e038c),
            timestamp = datetime.utcnow()
        )
        embed.set_image(url = target.avatar_url)

        fields = [
            ("ID", target.id, False),
            ("Name", str(target), True),
            ("Bot?", target.bot, True)

        ]
    
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await message.channel.send(embed=embed)
    
    if message.content.startswith('!help'):
        embed = discord.Embed(title="Here:", colour=discord.Colour(0x3e038c))

        embed.add_field(name=f"!find", value="example: !find eromanga sensei", inline=False)
        embed.add_field(name=f"!schedule", value="show day latest release. example: !schedule monday", inline=False)
        embed.add_field(name=f"!info", value="User info. example: !info @user", inline=False)
        
        await message.channel.send(embed=embed)

    if message.content.startswith('!find'):
        Message = message_data.split(' ')
        MessageData = (Message[1])
        anime_title = MessageData.replace(" ", "%20")
        request = json.load(urllib.request.urlopen('https://api.jikan.moe/v3/search/anime?q={}&page=1&limit=1'.format(anime_title)))
        embed = discord.Embed(title="Results:", colour=discord.Colour(0x3e038c))
        for data in request['results']:
            embed.add_field(name=f"Title:", value=data['title'])
            embed.add_field(name=f"Synopsis:", value=data['synopsis'])
            embed.add_field(name=f"Types:", value=data['type'])
            embed.add_field(name=f"Episode:", value=data['episodes'])
            embed.set_thumbnail(url=data['image_url'])
        await message.channel.send(embed=embed)

    if message.content.startswith('!schedule'):
        Message = message_data.split(' ')
        MessageData = (Message[1])
        request = json.load(urllib.request.urlopen('https://api.jikan.moe/v3/schedule/{}'.format(MessageData)))
        embed = discord.Embed(title="Weekly schedule: {}".format(MessageData), colour=discord.Colour(0x3e038c))
        
        for data in request['{}'.format(MessageData)]:
            
            embed.add_field(name=f"Title:", value=data['title'])
            embed.add_field(name=f"Types:", value=data['type'])
            embed.add_field(name=f"Episode:", value=data['episodes'])
            # embed.set_thumbnail(url=data['image_url'])
        await message.channel.send(embed=embed)

client.run(bot_token)
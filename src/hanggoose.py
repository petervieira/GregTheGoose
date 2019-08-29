# new class for organization

import discord
import asyncio
import os
from os import path

running = False
accepting = False
current_hang_message_id = -1
hang_participants = []

async def hang_run(reaction, user, client):
    global running
    running = True
    global accepting
    accepting = True
    hang_embed = discord.Embed(description = '', color = 0xfc0703)
    hang_embed.set_image(url = 'https://i.imgur.com/kEPUeck.png')
    hang_message = await reaction.message.channel.send(embed = hang_embed)
    await hang_message.add_reaction('👍')
    global current_hang_message_id
    current_hang_message_id = hang_message.id
    
    string = '============================================='
    waiting_message = await reaction.message.channel.send(string)
    for i in range(0,15):
        await asyncio.sleep(1)
        string = string[0:len(string)-3]
        await waiting_message.edit(content = string)
    accepting = False
    
    players = []
    for player in hang_participants:
        players.append(client.get_user(player))
    await reaction.message.channel.send('Players: ' + ''.join(e.mention + ' ' for e in players))
    
    #await reaction.message.channel.send('', file = discord.File(path.join(path.dirname(path.realpath(__file__)), 'images/hang_goose0.jpg')))
    #await reaction.message.channel.send('', file = discord.File(path.join(path.dirname(path.realpath(__file__)), 'images/hang_goose1.jpg')))
    #await reaction.message.channel.send('', file = discord.File(path.join(path.dirname(path.realpath(__file__)), 'images/hang_goose2.jpg')))
    #await reaction.message.channel.send('', file = discord.File(path.join(path.dirname(path.realpath(__file__)), 'images/hang_goose3.jpg')))
    #await reaction.message.channel.send('', file = discord.File(path.join(path.dirname(path.realpath(__file__)), 'images/hang_goose4.jpg')))
    #await reaction.message.channel.send('', file = discord.File(path.join(path.dirname(path.realpath(__file__)), 'images/hang_goose5.jpg')))
    #await reaction.message.channel.send('', file = discord.File(path.join(path.dirname(path.realpath(__file__)), 'images/hang_goose6.jpg')))
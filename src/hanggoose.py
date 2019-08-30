# new class for organization

import discord
import asyncio
import os
import random
from os import path

running = False
accepting = False
current_hang_message_id = -1
hang_participants = []
word = ''
word_progress = []
count = 0

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
    
    if len(hang_participants) != 0:
        players = []
        for player in hang_participants:
            players.append(client.get_user(player))
        await reaction.message.channel.send('Players: ' + ''.join(e.mention + ' ' for e in players))

        file = open("dictionary.txt", "r")
        rint = random.randint(0,84036)
        global word
        word = file.readlines()[rint]
        file.close()
        
        global word_progress
        for i in range(0, len(word.rstrip())):
            word_progress.append('\_ ')
        
        await reaction.message.channel.send('', file = discord.File(path.join(path.dirname(path.realpath(__file__)), 'images/hang_goose0.jpg')))
        await reaction.message.channel.send(''.join(word_progress))
        
    else:
        running = False
        

async def guess(message, client):
    global count
    global word_progress
    global word
    global hang_participants
    global running
    compare_word = word_progress.copy()
    if len(message.content) != 1:
        await message.channel.send('Invalid letter')
    else:
        for x in range(0,len(word)):
            if str(word[x]) == message.content:
                compare_word[x] = message.content
        if compare_word == word_progress:
            # wrong guess
            count += 1
            if count < 6:
                await message.channel.send('', file = discord.File(path.join(path.dirname(path.realpath(__file__)), 'images/hang_goose' + str(count) + '.jpg')))
            else:
                await message.channel.send('', file = discord.File(path.join(path.dirname(path.realpath(__file__)), 'images/hang_goose6.jpg')))
                await message.channel.send('GAME OVER')
                running = False
                hang_participants = []
                count = 0
                word = ''
                word_progress = []
                # END GAME
        else:
            # correct guess
            word_progress = compare_word.copy()
            await message.channel.send(''.join(word_progress))
            if ''.join(word_progress).strip() == word.rstrip():
                await message.channel.send('You\'ve confounded the gaggle!')
                running = False
                hang_participants = []
                count = 0
                word = ''
                word_progress = []
                # END GAME
    
    await asyncio.sleep(0)
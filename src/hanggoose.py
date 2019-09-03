# new class for organization

import discord
import asyncio
import os
import random
from os import path

running = False
accepting = False
current_hang_message_id = -1
current_replay_message_id = -1
hang_participants = []
word = ''
word_progress = []
count = 0
guesses = []

async def hang_run(reaction, user, client, speed):
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
    if speed:
        for i in range(0,5):
            await asyncio.sleep(1)
            string = string[0:len(string)-9]
            await waiting_message.edit(content = string)
    else:
        for i in range(0,15):
            await asyncio.sleep(1)
            string = string[0:len(string)-3]
            await waiting_message.edit(content = string)
    await asyncio.sleep(1)
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
        
        hang_start_embed = discord.Embed(description = '', color = 0xfc0703)
        hang_start_embed.set_image(url = 'https://i.imgur.com/zfa9li6.jpg')
        await reaction.message.channel.send(embed = hang_start_embed)
        await reaction.message.channel.send(''.join(word_progress))
    else:
        running = False
        

async def guess(message, client):
    global count
    global word_progress
    global word
    global hang_participants
    global running
    global guesses
    global current_replay_message_id
    compare_word = word_progress.copy()
    if len(message.content) != 1:
        await message.channel.send('Invalid letter')
    elif message.content in guesses:
        await message.channel.send('You already guessed that!')
    else:
        guesses.append(message.content)
        for x in range(0,len(word)):
            if str(word[x]) == message.content:
                compare_word[x] = message.content
        if compare_word == word_progress:
            # wrong guess
            count += 1
            hang_stage_embed = discord.Embed(description = 'Letters guessed: ' + ', '.join(str(e) for e in guesses), color = 0xfc0703)
            if count < 6:
                if count == 1:
                    hang_stage_embed.set_image(url = 'https://i.imgur.com/ppEvygg.jpg')
                elif count == 2:
                    hang_stage_embed.set_image(url = 'https://i.imgur.com/2bBns9G.jpg')
                elif count == 3:
                    hang_stage_embed.set_image(url = 'https://i.imgur.com/IaxyBSm.jpg')
                elif count == 4:
                    hang_stage_embed.set_image(url = 'https://i.imgur.com/d1B5fBQ.jpg')
                elif count == 5:
                    hang_stage_embed.set_image(url = 'https://i.imgur.com/SGvRuhz.jpg')
                await message.channel.send(embed = hang_stage_embed)
                await message.channel.send(''.join(word_progress))
            else:
                hang_stage_embed.set_image(url = 'https://i.imgur.com/jhWzNH6.jpg')
                await message.channel.send(embed = hang_stage_embed)
                await message.channel.send('GAME OVER')
                replay_embed = discord.Embed(description = 'The word was ' + word + 'Replay?', color = 0xfc0703)
                running = False
                hang_participants = []
                count = 0
                word = ''
                word_progress = []
                guesses = []
                # END GAME
                
                replay_message = await message.channel.send(embed = replay_embed)
                current_replay_message_id = replay_message.id
                await replay_message.add_reaction('🤔')
           
        else:
            # correct guess
            word_progress = compare_word.copy()
            await message.channel.send(''.join(word_progress))
            if ''.join(word_progress).strip() == word.rstrip():
                replay_embed = discord.Embed(description = 'You\'ve confounded the gaggle!', color = 0xfc0703)
                running = False
                hang_participants = []
                count = 0
                word = ''
                word_progress = []
                guesses = []
                # END GAME
                
                replay_message = await message.channel.send(embed = replay_embed)
                current_replay_message_id = replay_message.id
                await replay_message.add_reaction('🤔')
    
    await asyncio.sleep(0)
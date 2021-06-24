import discord
import asyncio
import random

running = False
accepting = False
current_connect_message_id = -1
current_replay_message_id = -1
connect_participants = []
count = 0
messages_to_clear = []
pictures_to_clear = []


async def game_run(reaction, client, speed):
    global running
    running = True
    global accepting
    accepting = True
    connect_embed = discord.Embed(description='', color=0x3461eb)
    connect_embed.set_image(url='https://i.imgur.com/DQADM9K.png')
    connect_message = await reaction.message.channel.send(embed=connect_embed)
    await connect_message.add_reaction('👍')
    global current_connect_message_id
    current_connect_message_id = connect_message.id

    string = '============================================='
    if speed:
        waiting_message = await reaction.message.channel.send(string)
        for i in range(0, 4):
            await asyncio.sleep(1)
            string = string[0:len(string) - 9]
            await waiting_message.edit(content=string)
        await connect_message.delete()
    else:
        waiting_message = await reaction.message.channel.send(string)
        for i in range(0, 14):
            await asyncio.sleep(1)
            string = string[0:len(string) - 3]
            await waiting_message.edit(content=string)
        await connect_message.delete()
    await asyncio.sleep(1)
    accepting = False

    if len(connect_participants) > 1:
        players = []
        for player in hang_participants:
            players.append(client.get_user(player))
        await reaction.message.channel.send('Players: ' + ''.join(e.mention + ' ' for e in players))

      

        hang_start_embed = discord.Embed(description='', color=0xfc0703)
        hang_start_embed.set_image(url='https://i.imgur.com/zfa9li6.jpg')
        global messages_to_clear
        global pictures_to_clear
        pictures_to_clear.append(await reaction.message.channel.send(embed=hang_start_embed))
        messages_to_clear.append(await reaction.message.channel.send(''.join(word_progress)))
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
    global messages_to_clear
    global pictures_to_clear
    #print(messages_to_clear)
    #print(pictures_to_clear)
    #print("")
    
    compare_word = word_progress.copy()
    lower_guess = message.content.lower()
    if len(lower_guess) != 1 or not lower_guess.isalpha():
        await message.channel.send('Invalid letter')
    elif lower_guess in guesses:
        await message.channel.send('You already guessed that!')
    else:
        guesses.append(lower_guess)
        for x in range(0, len(word)):
            if str(word[x]) == lower_guess:
                compare_word[x] = lower_guess
        if compare_word == word_progress:
            # wrong guess
            for mess in messages_to_clear:
                await mess.delete()
            messages_to_clear = []
            for pic in pictures_to_clear:
                await pic.delete()
            pictures_to_clear = []
            count += 1
            hang_stage_embed = discord.Embed(description='Letters guessed: ' + ', '.join(str(e) for e in guesses),
                                             color=0xfc0703)
            if count < 6:
                if count == 1:
                    hang_stage_embed.set_image(url='https://i.imgur.com/ppEvygg.jpg')
                elif count == 2:
                    hang_stage_embed.set_image(url='https://i.imgur.com/2bBns9G.jpg')
                elif count == 3:
                    hang_stage_embed.set_image(url='https://i.imgur.com/IaxyBSm.jpg')
                elif count == 4:
                    hang_stage_embed.set_image(url='https://i.imgur.com/d1B5fBQ.jpg')
                elif count == 5:
                    hang_stage_embed.set_image(url='https://i.imgur.com/SGvRuhz.jpg')
                pictures_to_clear.append(await message.channel.send(embed=hang_stage_embed))
                messages_to_clear.append(await message.channel.send(''.join(word_progress)))
            else:
                hang_stage_embed.set_image(url='https://i.imgur.com/jhWzNH6.jpg')
                await message.channel.send(embed=hang_stage_embed)
                await message.channel.send('GAME OVER')
                replay_embed = discord.Embed(description='The word was ' + word + 'Replay?', color=0xfc0703)
                running = False
                hang_participants = []
                count = 0
                word = ''
                word_progress = []
                guesses = []
                # END GAME

                replay_message = await message.channel.send(embed=replay_embed)
                current_replay_message_id = replay_message.id
                await replay_message.add_reaction('🤔')

        else:
            # correct guess
            word_progress = compare_word.copy()
            for mess in messages_to_clear:
                await mess.delete()
            messages_to_clear = []
            if ''.join(word_progress).strip() == word.rstrip():
                await message.channel.send(''.join(word_progress))
                replay_embed = discord.Embed(description='You\'ve confounded the gaggle!', color=0xfc0703)
                running = False
                hang_participants = []
                count = 0
                word = ''
                word_progress = []
                guesses = []
                # END GAME

                replay_message = await message.channel.send(embed=replay_embed)
                current_replay_message_id = replay_message.id
                await replay_message.add_reaction('🤔')
            else:
                messages_to_clear.append(await message.channel.send(''.join(word_progress)))

    await asyncio.sleep(0)

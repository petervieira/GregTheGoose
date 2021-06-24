import discord
import asyncio
import datetime
import sys
import os
from os import path
from ids import *
import hanggoose
import connectfour

sys.path.insert(0, '/Users/peter/OneDrive/Documents/GitHub/Mandelbrothers/src')
import mandelbrothers
import asyncdriver

game_1 = os.path.abspath('Mandelbrothers/src')

current_game_message_id = -1


class MyClient(discord.Client):
    async def on_ready(self):
        print(self.user.name)
        print(self.user.id)
        print('------')
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(name="quack tracks",
                                                                                           type=discord.ActivityType.listening))

    async def on_typing(self, channel, user, when):
        # change id to that of annoying target
        if user.id == aaron_id or user.id == vinny_id or user.id == mike_id or user.id == eman_id:
            await channel.send("CLOSE YOUR DAMN BEAK {0.user.mention}")

    async def on_message(self, message):
        if str(message.channel) in channels:
            # prevents the bot from replying to itself
            if message.author.id == self.user.id:
                return
            if message.author.id in hanggoose.hang_participants:
                if message.content.startswith('?leave'):
                    hanggoose.hang_participants.remove(message.author.id)
                    await message.channel.send("{0.author.mention} has left the game!".format(message))
                    if len(hanggoose.hang_participants) == 0:
                        hanggoose.running = False
                        hanggoose.hang_participants = []
                        hanggoose.count = 0
                        hanggoose.word = ''
                        hanggoose.word_progress = []
                        hanggoose.guesses = []
                else:
                    if not hanggoose.accepting:
                        await hanggoose.guess(message, client)
                        return
            if message.content.startswith('?speak'):
                await message.channel.send(
                    "SQUAWK! Hi there, {0.author.mention}.  I'm Greg, The Gregarious Gaming Goose!".format(message))
            elif message.content.startswith('?help'):
                await message.channel.send("Calling in the goose tech team...", file=discord.File(
                    path.join(path.dirname(path.realpath(__file__)), 'images/goose_tech.jpg')))
                await message.channel.send(embed=discord.Embed(
                    description='?speak Says hi!\n?members Counts your goslings\n?game Opens game selection menu\n?leave'
                                ' Leaves current game\n?chastise I dare you...\n?close (Admin only) Gives me some rest',
                    color=0xfc7f03))
            elif message.content.startswith('?members'):
                mem_count = message.guild.member_count - 1
                if mem_count == 1:
                    await message.channel.send(
                        f'There is {mem_count} friend of the goose in this server')
                else:
                    await message.channel.send(
                        f'There are {mem_count} friends of the goose in this server')
            elif message.content.startswith('?game'):
                game_embed = discord.Embed(description="""```yaml\n                   Greg\'s Games```""",
                                           color=0x03fc0f)
                game_embed.add_field(name='================================================',
                                     value="""\t\tDon't worry about the cost to play these games -- I put it on my bill""",
                                     inline=False)
                game_embed.add_field(name='HangGoose', value='I would prefer it if you did not...', inline=False)
                game_embed.add_field(name='Connect Four', value='No, a V shape does not count as a line', inline=False)
                game_embed.add_field(name='Trivia', value='How much do you know about your avian buddies?', inline=False)
                game_embed.add_field(name='Mandelbrothers', value='A tile-based RPG unrelated to geese', inline=False)
                game_embed.add_field(name='~~Snake~~ Goose', value='Eat the berries; extend your neck', inline=False)
                game_embed.set_image(url='https://i.imgur.com/aygIxu7.jpg')  # credit to WikiHow for this masterpiece
                bot_message = await message.channel.send(embed=game_embed)
                global current_game_message_id
                current_game_message_id = bot_message.id
                await bot_message.add_reaction('🇭')
                await bot_message.add_reaction('🔴')
                await bot_message.add_reaction('📚')
                await bot_message.add_reaction('🏹')
                await bot_message.add_reaction('🐍')
            elif message.content.startswith('?chastise'):
                await message.channel.send("What the duck did you just ducking say about me, {0.author.mention}? "
                                           "I'll have you know I graduated top of my flock in the Navy Geese, and "
                                           "I've been involved in numerous secret raids on Al-Quackda, and I have "
                                           "left over 300 confirmed peck marks. I am trained in avian warfare and I'm"
                                           " the top sniper in the entire Canadian winged forces. You are nothing to me"
                                           " but just another bread crumb. I will wipe you the duck out with precision "
                                           "the likes of which has never been seen before in this marsh, mark my ducking"
                                           " squawks. You think you can get away with saying that shit to me over the "
                                           "Internet? Have another gander, ducker. As we speak I am contacting my secret"
                                           " wetwork of spies across the USA and Canada and your IP is being traced right"
                                           " now so you better prepare for the birdemic, maggot. The one that wipes out"
                                           " the pathetic little thing you call your life. You're ducking dead, kid. I "
                                           "can be anywhere, anytime, and I can kill you in over seven hundred ways, and"
                                           " that's just with my naked wings. Not only am I extensively trained in "
                                           "beakless combat, but I have access to the entire arsenal of the United States"
                                           " Marine Corps and I will use it to its full extent to wipe your miserable "
                                           "feathers off the face of the continent, you little shit. If only you could"
                                           " have known what unholy retribution your little 'clever' comment was about to"
                                           " bring down upon you, maybe you would have shut your ducking beak. But you "
                                           "couldn't, you didn't, and now you're paying the price, you goddamn idiot. I "
                                           "will shit fury all over you and you will drown in it. You're ducking dead, "
                                           "kiddo.".format(message))
            elif message.content.startswith('?close') and message.author.id == admin_id:
                if 3 <= datetime.datetime.now().month <= 5:
                    await message.channel.send("Flying north for the summer...")
                    await client.close()
                elif 6 <= datetime.datetime.now().month <= 8:
                    await message.channel.send("Going for a summer swim...")
                    await client.close()
                elif 9 <= datetime.datetime.now().month <= 11:
                    await message.channel.send("Flying south for the winter...")
                    await client.close()
                else:
                    await message.channel.send("Going to 'chill' with the gaggle")
                    await client.close()
            elif message.content.startswith('?spamgrfn'):
                while (True):
                    await message.channel.send("{0.mention} goon".format(client.get_user(griffen_id)))
                    await asyncio.sleep(3)

    async def on_message_delete(self, message):
        # prevents the owner and bot itself from getting caught
        if message.author.id != admin_id and message.author.id != self.user.id:
            await message.channel.send(
                "No one escapes the Goosish Inquisition!\n{0.author.mention} deleted the following message:\n".format(
                    message) + message.content)

    async def on_reaction_add(self, reaction, user):
        if user.id != self.user.id:
            if reaction.message.id == current_game_message_id:
                if reaction.emoji == '🇭':
                    if hanggoose.running:
                        await reaction.message.channel.send('There is a game in progress!')
                    else:
                        await hanggoose.hang_run(reaction, client, False)
                elif reaction.emoji == '🔴':
                    if connectfour.running:
                        await reaction.message.channel.send('There is a game in progress!')
                    else:
                        await connectfour.game_run(reaction, client, False)
                elif reaction.emoji == '📚':
                    await asyncio.sleep(0)
                elif reaction.emoji == '🏹':
                    # await asyncdriver.main() #this simply runs the mandelbrothers game on the host's computer
                    await asyncio.sleep(0)
                elif reaction.emoji == '🐍':
                    await asyncio.sleep(0)

            if reaction.message.id == hanggoose.current_hang_message_id:
                if reaction.emoji == '👍' and hanggoose.accepting:
                    if user.id not in hanggoose.hang_participants:
                        hanggoose.hang_participants.append(user.id)
            
            if reaction.message.id == hanggoose.current_replay_message_id:
                if reaction.emoji == '🤔' and not hanggoose.running:
                    await hanggoose.hang_run(reaction, client, True)
                    
            if reaction.message.id == connectfour.current_connect_message_id:
                if reaction.emoji == '👍' and connectfour.accepting:
                    if user.id not in connectfour.connect_participants:
                        connectfour.connect_participants.append(user.id)

client = MyClient(prefix='', intents=discord.Intents().all())  # creates client as subclass of discord.Client and overrides the events (avoids decorators)

# client runs the bot token
client.run(TOKEN)

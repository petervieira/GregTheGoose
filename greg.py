import discord
import asyncio
import datetime
from ids import *
import sys
import os
from game import *
sys.path.insert(0, '/Users/peter/OneDrive/Documents/GitHub/Mandelbrothers/src')
import mandelbrothers
import asyncdriver

game_1 = os.path.abspath('Mandelbrothers/src')

class MyClient(discord.Client):
    async def on_ready(self):
        print(self.user.name)
        print(self.user.id)
        print('------')
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(name="quack tracks", type=discord.ActivityType.listening))

    async def on_typing(self, channel, user, when):
        # change id to that of annoying target
        if user.id == vinny_id:
            await channel.send("CLOSE YOUR DAMN BEAK")
    async def on_message(self, message):
        if str(message.channel) in channels:
            # prevents the bot from replying to itself
            if message.author.id == self.user.id:
                return
            if message.content.startswith('!speak'):
                await message.channel.send("SQUAWK! Hi there, {0.author.mention}.  I'm Greg, The Gregarious Gaming Goose!".format(message))
            elif message.content.startswith('!help'):
                await message.channel.send("Calling in the goose tech team...", file = discord.File("images/goose_tech.jpg"))
                await message.channel.send(embed = discord.Embed(description = '!speak Says hi!\n!members Counts your gooslings\n!game Opens game selection menu\n!chastise I dare you...\n!close Gives me some rest', color = 0xfc7f03))
            elif message.content.startswith('!members'):
                await message.channel.send(f'There are {message.guild.member_count - 1} friends of the goose in this server')
            elif message.content.startswith('!game'):
                await asyncdriver.main() #this simply runs the mandelbrothers game on the host's computer
                await message.channel.send("(Insert challenge for pygame module here)")
            elif message.content.startswith('!chastise'):
                await message.channel.send("What the duck did you just ducking say about me, {0.author.mention}? I'll have you know I graduated top of my flock in the Navy Geese, and I've been involved in numerous secret raids on Al-Quackda, and I have left over 300 confirmed peck marks. I am trained in avian warfare and I'm the top sniper in the entire Canadian winged forces. You are nothing to me but just another bread crumb. I will wipe you the duck out with precision the likes of which has never been seen before in this marsh, mark my ducking squawks. You think you can get away with saying that shit to me over the Internet? Have another gander, ducker. As we speak I am contacting my secret wetwork of spies across the USA and Canada and your IP is being traced right now so you better prepare for the birdemic, maggot. The one that wipes out the pathetic little thing you call your life. You're ducking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my naked wings. Not only am I extensively trained in beakless combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable feathers off the face of the continent, you little shit. If only you could have known what unholy retribution your little 'clever' comment was about to bring down upon you, maybe you would have shut your ducking beak. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're ducking dead, kiddo.".format(message))
            elif message.content.startswith('!close') and message.author.id == peter_id:
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
                
    async def on_message_delete(self, message):
        # prevents the owner and bot itself from getting caught
        if message.author.id != peter_id or self.user.id:
            await message.channel.send("No one escapes the Goosish Inquisition!\n{0.author.mention} deleted the following message:\n".format(message) + message.content)

client = MyClient() # creates client as subclass of discord.Client and overrides the events (avoids decorators)

# client runs the bot token
client.run(TOKEN)
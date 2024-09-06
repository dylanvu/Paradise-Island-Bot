import datetime
import os
from dotenv import load_dotenv
import discord
load_dotenv()

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if (message.author == self.user):
            return
        # convert the datetime object to a more readable format
        readable_date = message.created_at.strftime("%B %d, %Y, %I:%M %p")
        message_information = f'Message from {message.author} at {readable_date} in channel {message.channel}: \"{message.content}\"'
        print(message_information)
        await message.add_reaction('👍')
        await message.reply(message_information)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('BOT_TOKEN'))
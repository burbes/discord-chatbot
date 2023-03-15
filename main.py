import os
import discord
import openai

# Set up OpenAI API
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.messages = True

class ChatBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'{self.user} is connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        input_content = message.content

        if message.attachments:
            for attachment in message.attachments:
                image_bytes = await attachment.read()
                input_content += f" {attachment.filename}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": input_content}]
        )

        assistant_response = response['choices'][0]['message']['content']
        await message.channel.send(assistant_response)

client = ChatBot(intents=intents)
client.run(DISCORD_TOKEN)

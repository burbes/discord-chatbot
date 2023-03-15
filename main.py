import os
import discord
import openai

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

class ChatBot (discord.Client):
    async def on_ready(self):
        print(f'{self.user} is connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        input_content = [message.content]

        if message.attachments:
            for attachment in message.attachments:
                image_bytes = await attachment.read()
                input_content.append({"image": image_bytes})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", “content”: input_content}]
        )

        assistant_response = response['choices'][0]['message']['content']
        await message.channel.send(assistant_response)

client = ChatBot()
client.run(DISCORD_TOKEN)


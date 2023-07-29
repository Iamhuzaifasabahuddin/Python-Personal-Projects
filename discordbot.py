import discord
import requests
import json

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

TOKEN = 'MTEzNDY3OTQyMzk3OTg5Njk1Ng.GujfpB.ae__8Qmu7fua524uUG8g6FjPvZ0xIVGsi5fqzI'


def quote_generator():
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.content)
    print(data)
    quote = data[0]['q'] + "-" + data[0]['a']

    return quote


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello {message.author.mention}!')

    if message.content.startswith('$inspire'):
        quote = quote_generator()
        await message.channel.send(quote)

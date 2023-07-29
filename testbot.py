import discord
from discord.ext import commands
import requests
import json
from botcalendar import *
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


def quote_generator():
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.content)
    print(data)
    quote = data[0]['q'] + "-" + data[0]['a']

    return quote


@bot.group(name='functions', help="Group of bot functions.")
async def bot_functions(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid command. Use $help functions to see available subcommands.")


@bot_functions.command(name="hello", help="Greets the user with a hello message.")
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')


@bot_functions.command(name="inspire", help="Get an inspirational quote.")
async def inspire(ctx):
    quote = quote_generator()
    await ctx.send(quote)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')


@bot.command()
async def inspire(ctx):
    quote = quote_generator()
    await ctx.send(quote)


@bot.command()
async def add(ctx, description: str, duration: float):
    add_event(creds, description, duration)
    await ctx.send(f'Event added: {description}, Duration: {duration} hours.')


@bot.command()
async def view(ctx, num: int):
    # Calls your existing get_Hours function
    output = get_Hours_from_database(num)
    await ctx.send(output)


@bot.command()
async def commit(ctx, date: str = None):
    """Command to commit hours to the database for a specific date (optional)."""
    # Calls your existing commit_hours function
    commit_hours(creds, date)
    await ctx.send("Coding hours added to database successfully")


@bot.command()
async def events(ctx, date: str):
    """Command to fetch events from the Google Calendar on a specific date."""
    # Calls your existing get_events function
    events_list = get_events1(creds, date)

    # Send the result back to the user in the Discord channel
    if not events_list:
        await ctx.send(f"No events found for date {date}.")
    else:
        event_info = "\n".join(events_list)
        await ctx.send(f"Event IDs on {date}:\n{event_info}")


@bot.command()
async def remove(ctx, event_id: str):
    """Command to remove an event from Google Calendar using its ID."""
    success = remove_event(creds, event_id)

    # Send the result back to the user in the Discord channel
    if success:
        await ctx.send(f"Event with ID {event_id} has been removed from Google Calendar.")
    else:
        await ctx.send(f"An error occurred while removing the event with ID {event_id}.")


# Load your Google Calendar API credentials and start the bot
SCOPES = ['https://www.googleapis.com/auth/calendar']

if __name__ == '__main__':
    # Load your credentials here
    creds = None
    if os.path.exists('token2.json'):
        creds = Credentials.from_authorized_user_file('token2.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('Calendar_Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token2.json', 'w') as token:
            token.write(creds.to_json())

    bot.run('MTEzNDY3OTQyMzk3OTg5Njk1Ng.GujfpB.ae__8Qmu7fua524uUG8g6FjPvZ0xIVGsi5fqzI')

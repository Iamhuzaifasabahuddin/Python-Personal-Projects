import os
import discord
import json
import requests  # type: ignore
from Google.botcalendar import add_event, commit_hours, get_Hours_from_database, get_events1, remove_event
from discord.ext import commands
from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

apikey = json.load(open("Search_Engine_Credentials.json", "r"))["KEYS"]["API"]
engineid = json.load(open("Search_Engine_Credentials.json", "r"))["KEYS"]["ENGINEID"]



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


def quote_generator():
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.content)
    quote = data[0]['q'] + "-" + data[0]['a']
    return quote


def Search(query, nums, sorting=None):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": apikey,
        "cx": engineid,
        # "searchType": "text" or image
        "num": nums,
        "sort": sorting

    }
    response = requests.get(url, params=params)
    data = response.json()
    search_results = []
    if "items" in data:
        for item in data["items"]:
            Title = item.get("title", "No Title")
            Link = item.get("link", "No Link")
            search_results.append(f"Found result {Title} and link {Link}")
    return search_results


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def hello(ctx):
    """command to greet"""
    await ctx.send(f'Hello {ctx.author.mention}!')


@bot.command()
async def inspire(ctx):
    """provides with a random generated quote"""
    quote = quote_generator()
    await ctx.send(quote)


@bot.command()
async def google_search(ctx, *, query_and_params):
    params = query_and_params.split()
    query = params[0]
    nums = int(params[1]) if len(params) > 1 else 5  # Default value if not provided
    sorting = params[2] if len(params) > 2 else None  # Default value if not provided

    results = Search(query, nums, sorting)
    output_msg = "\n".join(results)
    await ctx.send("Showing results:\n" + output_msg)

@bot.command()
async def add(ctx, description: str, duration: float):
    """adds event to the calendar"""
    add_event(creds, description, duration)
    await ctx.send(f'Event added: {description}, Duration: {duration} hours.')


@bot.command()
async def view(ctx, num: int):
    """Command to fetch hours from the database for a specific number of days."""

    hours_info, total_hours, average_hours = get_Hours_from_database(num)

    output_msg = "\n".join(hours_info)
    output_msg += f"\nTotal hours: {total_hours}\nAverage hours per day: {average_hours}"

    await ctx.send(f"Hours information for the last {num} days:\n```{output_msg}```")


@bot.command()
async def commit(ctx, date: str = None):  # type: ignore
    """Command to commit hours to the database for a specific date (optional)."""
    commit_hours(creds, date)
    await ctx.send("Coding hours added to database successfully")


@bot.command()
async def events(ctx, date: str):
    """Command to fetch events from the Google Calendar on a specific date."""
    events_list = get_events1(creds, date)
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


SCOPES = ['https://www.googleapis.com/auth/calendar']

if __name__ == '__main__':
    creds = None
    if os.path.exists('token2.json'):
        creds = Credentials.from_authorized_user_file('token2.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('Calendar_Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token2.json', 'w') as token:
            token.write(creds.to_json())

    token = json.load(open(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\DiscordToken.json'))['TOKEN']

    bot.run(token)

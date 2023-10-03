import json
import random

import requests
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/<name>')
def hello_user(name: str) -> str:
    """Greets user
    Args:
        name: str: name of the user
    Returns:
        Greets the user
    """
    return f"Hello, {escape(name)}!"


@app.route('/')
def index() -> str:
    """Displays the main page
    Returns:
        Elements of the main page
    """
    return "Main page by default"


@app.route('/random')
def random_generator() -> str:
    """Generates random numbers from 1 to 1000

    Returns:
        Random generated number
    """
    generated: int = random.randrange(1, 1000)
    return f"Random generated number {generated}!"


@app.route('/random/<int:limit>')
def random_generator_range(limit: int) -> str:
    """Generates a random number between 1 and user specified

    Args:
        limit: int: max range of random numbers

    Returns:
        Random number between 1 and user specified
    """
    generated: int = random.randrange(1, limit + 1)
    return f"Random generated number {generated}!"


def quote() -> str:
    """Fetches the quote from the API"""
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.content)
    quoted = f"{data[0]['q']}  ~  {data[0]['a']}"
    return quoted


@app.route('/quote')
def quote_generator() -> str:
    """Generates a random quote from an API
    Returns:
        Quote
    """
    return f"Quote of the day is: \n{quote()}!"

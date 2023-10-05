import json
import random

import requests
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/hello/')
def hello_user(name: str = None) -> str:
    """Greets user
    Args:
        name: str: name of the user
    Returns:
        Greets the user
    """
    return render_template('Home.html', name=name)


@app.route('/')
def index() -> str:
    """Displays the main page
    Returns:
        Elements of the main page
    """
    return render_template('Home.html')


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))


@app.route('/random/')
@app.route('/random/<int:limit>')
def random_generator_range(limit: int = None) -> str:
    """Generates a random number between 1 and user specified

    Args:
        limit: int: max range of random numbers

    Returns:
        Random number between 1 and user specified
    """
    if limit:
        generated: int = random.randrange(1, limit + 1)
    else:
        generated: int = random.randrange(1, 1000)

    return render_template('random.html', generated=generated)


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
    generated = quote()
    return render_template('quote.html', generated=generated)


if __name__ == '__main__':
    app.run(debug=False, port=8080)

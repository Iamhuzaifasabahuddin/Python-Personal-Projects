import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    # Read data from file
    df = pd.read_csv("epa-sea-level.csv")
    x = df['Year']
    y = df['CSIRO Adjusted Sea Level']

    # Create scatter plot
    fig, ax = plt.subplots()
    plt.scatter(x, y)

    # Create first line of best fit
    res = linregress(x, y)
    x_prediction = pd.Series([i for i in range(1880, 2051)])
    y_prediction = res.slope * x_prediction + res.intercept
    plt.plot(x_prediction, y_prediction, "r")

    # Create second line of best fit
    new = df.loc[df['Year'] >= 2000]
    newx = new['Year']
    newy = new['CSIRO Adjusted Sea Level']
    res = linregress(newx, newy)
    x_prediction = pd.Series([i for i in range(2000, 2051)])
    y_prediction = res.slope * x_prediction + res.intercept
    plt.plot(x_prediction, y_prediction, "green")

    # Add labels and title
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level (inches)")
    ax.set_title("Rise in Sea Level")

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()


draw_plot()

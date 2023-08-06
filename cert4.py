import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'])

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
    ]


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['date'], df['value'], 'r', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


draw_line_plot()


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df_bar = df.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig = df_bar.plot.bar(legend=True, figsize=(20, 5), xlabel="Years", ylabel="Average Page Views").figure
    plt.legend(
        ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
         "December"])
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


draw_bar_plot()


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box["month_num"] = df_box["date"].dt.month
    df_box = df_box.sort_values("month_num")

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

    sns.boxplot(x=df_box["year"], y=df_box["value"], ax=axes[0])
    sns.boxplot(x=df_box["month"], y=df_box["value"], ax=axes[1])

    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')  # Fix the y-axis label
    axes[0].set_title('Year-wise Box Plot (Trend)')  # Fix the title
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig


# Assuming you have already loaded the data into the 'df' DataFrame
draw_box_plot()

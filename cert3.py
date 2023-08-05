import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
bmi = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (bmi > 25).astype(int)

# Normalize data by making 0 always good and 1 always bad
mapping = {1: 0, 2: 1, 3: 1}
df['gluc'] = df['gluc'].replace(mapping)
df['cholesterol'] = df['cholesterol'].replace(mapping)


# Draw Categorical Plot
def draw_cat_plot():
    df_cat = pd.melt(df, id_vars=['cardio'],
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature.
    df_cat = df_cat.groupby(["cardio", "variable", "value"], as_index=False).size()

    # Rename the 'size' column to 'total'
    df_cat.rename(columns={'size': 'total'}, inplace=True)

    fig = sns.catplot(x="variable", y="total", data=df_cat, hue="value", kind="bar", col="cardio").fig
    fig.savefig('catplot.png')
    return fig


print(draw_cat_plot())


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
        ]

    # Calculate the correlation matrix
    corr = df_heat.corr(method="pearson")

    # Generate a mask for the upper triangle
    mask = np.triu(corr)
    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))
    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, annot=True, fmt=".1f", mask=mask, center=0, linewidths=0.5, square=True, cbar_kws={"shrink": 0.5})
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set visual style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 6)

def plot_population_trends(df, countries):
    """Line chart of population over time."""
    filtered_df = df[df['country'].isin(countries)]
    plt.figure()
    sns.lineplot(data=filtered_df, x='year', y='population', hue='country', marker='o')
    plt.title("Population Trends Over Time")
    plt.ylabel("Population")
    plt.xlabel("Year")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_top_populous(df, year):
    """Bar chart of top 10 most populous countries."""
    top_10 = df[df['year'] == year].nlargest(10, 'population')
    plt.figure()
    sns.barplot(data=top_10, x='population', y='country', palette='viridis')
    plt.title(f"Top 10 Most Populous Countries in {year}")
    plt.xlabel("Population")
    plt.tight_layout()
    plt.show()

def plot_growth_heatmap(df):
    """Heatmap of growth rates by country and decade."""
    # Average growth rate per decade
    decade_growth = df.groupby(['country', 'decade'])['growth_rate'].mean().unstack()
    # Filter for countries with significant data
    top_countries = df.groupby('country')['population'].max().nlargest(20).index
    subset = decade_growth.loc[top_countries]
    
    plt.figure(figsize=(14, 8))
    sns.heatmap(subset, annot=True, cmap='RdYlGn', center=0)
    plt.title("Average Yearly Growth Rate (%) by Decade")
    plt.tight_layout()
    plt.show()

def plot_bar_chart_race(df):
    """Animated bar chart race using Plotly."""
    fig = px.bar(
        df, 
        x="population", 
        y="country", 
        color="country",
        animation_frame="year", 
        animation_group="country",
        orientation='h',
        range_x=[0, df['population'].max() * 1.1],
        title="World Population Growth (Bar Chart Race)"
    )
    fig.update_layout(showlegend=False)
    fig.show()

def plot_choropleth(df, year):
    """Choropleth world map using Plotly."""
    fig = px.choropleth(
        df[df['year'] == year],
        locations="iso_code",
        color="population",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"World Population Distribution in {year}"
    )
    fig.show()

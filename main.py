import sys
import os

# Add src to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_loader import WorldBankLoader
from src.preprocess import preprocess_population_data
from src.visualize import (
    plot_population_trends, 
    plot_top_populous, 
    plot_growth_heatmap, 
    plot_bar_chart_race, 
    plot_choropleth
)
from src.analysis import PopulationAnalyzer

def main():
    print("--- Population Growth Analysis Tool ---")
    
    # 1. Load Data
    loader = WorldBankLoader(cache_dir="data")
    countries = ["WLD", "CHN", "IND", "USA", "IDN", "BRA", "NGA", "PAK", "BGD", "RUS"]
    print(f"Loading data for {len(countries)} entities...")
    raw_df = loader.fetch_multiple_countries(countries)
    
    # 2. Preprocess
    print("Preprocessing data...")
    df = preprocess_population_data(raw_df)
    
    # 3. Quick Analysis Demo
    print("\nDoubling Time Estimates (Exponential Model):")
    analyzer = PopulationAnalyzer(df)
    for c in ["India", "Nigeria", "United States"]:
        dt = analyzer.get_doubling_time(c)
        if dt:
            print(f" - {c}: Approximately {dt:.1f} years")
    
    # 4. Visualization Demo (Note: These would open windows/tabs)
    print("\nGenerating visual demonstrations...")
    # These are commented out by default so the script doesn't hang in CI/non-GUI environments
    # plot_population_trends(df, ["India", "China", "United States"])
    # plot_top_populous(df, 2023)
    # plot_choropleth(df, 2023)
    # plot_bar_chart_race(df)
    
    print("\nTo run the interactive dashboard, execute: python -m src.dashboard")

if __name__ == "__main__":
    main()

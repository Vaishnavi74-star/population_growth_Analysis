import pandas as pd
import numpy as np
import os

def generate_mock_data(country_code, indicator, start_year=1960, end_year=2023):
    cache_dir = "data"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        
    cache_file = os.path.join(cache_dir, f"{indicator}_{country_code}_{start_year}_{end_year}.csv")
    if os.path.exists(cache_file):
        return

    years = np.arange(start_year, end_year + 1)
    
    if indicator == "death_rate":
        # Random death rate between 5 and 15, generally declining
        base = np.random.uniform(10, 15)
        values = base * np.exp(-0.01 * (years - start_year)) + np.random.normal(0, 0.5, len(years))
    elif indicator == "net_migration":
        # Random migration between -1M and 1M
        values = np.random.uniform(-500000, 1000000, len(years))
    else:
        values = np.random.uniform(1e6, 1e9, len(years))
        
    df = pd.DataFrame({
        "country": country_code, # Placeholder
        "iso_code": country_code,
        "year": years,
        indicator: values
    })
    
    # Try to get the real country name from an existing file if possible
    for f in os.listdir(cache_dir):
        if country_code in f:
            temp_df = pd.read_csv(os.path.join(cache_dir, f))
            if not temp_df.empty:
                df["country"] = temp_df["country"].iloc[0]
                break
                
    df.to_csv(cache_file, index=False)
    print(f"Generated mock data for {country_code} ({indicator})")

countries = ["WLD", "CHN", "IND", "USA", "IDN", "BRA", "NGA"]
for c in countries:
    generate_mock_data(c, "death_rate")
    generate_mock_data(c, "net_migration")

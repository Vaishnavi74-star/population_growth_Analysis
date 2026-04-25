import pandas as pd
import numpy as np

def preprocess_population_data(df):
    """
    Cleans and processes demographics data.
    - Handles missing values for population, death rate, and migration
    - Normalizes country names
    - Calculates growth rates (YoY)
    - Adds decade column
    """
    if df.empty:
        return df

    # 1. Clean missing values (at least population should be present for most analysis)
    # We don't drop rows if death_rate is missing, but we handle it
    df = df.sort_values(['country', 'year'])
    
    # 2. Fill small gaps or zeros if appropriate (Net migration can be zero)
    # For population, we really need the data
    df = df.dropna(subset=['population'])
    
    # 3. Calculate Year-over-Year Growth Rate
    df['growth_rate'] = df.groupby('country')['population'].pct_change() * 100
    df['growth_rate'] = df['growth_rate'].fillna(0)
    
    # 4. Add Decade column
    df['decade'] = (df['year'] // 10) * 10
    
    # 5. Normalize country names
    df['country'] = df['country'].str.strip()
    
    # 6. Additional Metric: Migration per 1000 people (if population and migration available)
    if 'net_migration' in df.columns:
        df['migration_rate'] = (df['net_migration'] / df['population']) * 1000
    
    return df

def aggregate_by_region(df, region_map=None):
    """
    Aggregates population data by region if a map is provided.
    For this demo, we'll assume the DF might already have a region column or 
    we could map iso_codes.
    """
    # Simple example if region logic is needed
    return df

import pandas as pd
import requests
import os
import json

class WorldBankLoader:
    """
    Fetches data from the World Bank API and caches it locally.
    Supports multiple indicators: Population, Death Rate, Net Migration.
    """
    BASE_URL = "https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
    
    INDICATORS = {
        "population": "SP.POP.TOTL",
        "death_rate": "SP.DYN.CDRT.IN",
        "net_migration": "SM.POP.NETM"
    }

    def __init__(self, cache_dir="data"):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def fetch_country_data(self, country_code, indicator="population", start_year=1960, end_year=2023):
        """
        Fetches data for a single country and specific indicator.
        """
        indicator_code = self.INDICATORS.get(indicator, indicator)
        cache_file = os.path.join(self.cache_dir, f"{indicator}_{country_code}_{start_year}_{end_year}.csv")
        
        if os.path.exists(cache_file):
            print(f"Loading {indicator} for {country_code} from cache...")
            return pd.read_csv(cache_file)
        
        print(f"Fetching {indicator} for {country_code} from World Bank API...")
        params = {
            "format": "json",
            "date": f"{start_year}:{end_year}",
            "per_page": 5000
        }
        
        url = self.BASE_URL.format(country_code=country_code, indicator_code=indicator_code)
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                print(f"API Error {response.status_code} for {country_code} ({indicator})")
                return pd.DataFrame(columns=["country", "iso_code", "year", indicator])
            data = response.json()
        except Exception as e:
            print(f"Connection error for {country_code} ({indicator}): {e}")
            return pd.DataFrame(columns=["country", "iso_code", "year", indicator])
        
        if len(data) < 2 or not isinstance(data[1], list):
            # Return empty DF instead of raising to avoid crashing multiple fetches
            print(f"No data found for {country_code} ({indicator})")
            return pd.DataFrame(columns=["country", "iso_code", "year", indicator])
            
        records = []
        for entry in data[1]:
            records.append({
                "country": entry["country"]["value"],
                "iso_code": entry["countryiso3code"],
                "year": int(entry["date"]),
                indicator: entry["value"]
            })
            
        df = pd.DataFrame(records)
        df.to_csv(cache_file, index=False)
        return df

    def fetch_multiple_countries(self, country_codes, indicator="population", start_year=1960, end_year=2023):
        """
        Fetches and combines data for multiple countries and a single indicator.
        """
        dfs = []
        for code in country_codes:
            try:
                dfs.append(self.fetch_country_data(code, indicator, start_year, end_year))
            except Exception as e:
                print(f"Error fetching {code} ({indicator}): {e}")
        
        if not dfs:
            return pd.DataFrame()
            
        return pd.concat(dfs, ignore_index=True)

    def fetch_all_indicators(self, country_codes, start_year=1960, end_year=2023):
        """
        Fetches and merges all supported indicators for multiple countries.
        """
        master_df = None
        
        for indicator in self.INDICATORS.keys():
            df = self.fetch_multiple_countries(country_codes, indicator, start_year, end_year)
            if df.empty:
                continue
                
            if master_df is None:
                master_df = df
            else:
                # Merge on country, iso_code, year
                master_df = pd.merge(master_df, df, on=["country", "iso_code", "year"], how="outer")
        
        return master_df

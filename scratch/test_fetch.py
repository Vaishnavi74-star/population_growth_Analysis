from src.data_loader import WorldBankLoader
loader = WorldBankLoader(cache_dir="data")
DEFAULT_COUNTRIES = ["WLD", "CHN", "IND", "USA", "IDN", "PAK", "NGA", "BRA", "BGD", "RUS", "MEX", "ETH", "JPN", "PHL", "EGY"]
df = loader.fetch_all_indicators(DEFAULT_COUNTRIES)
print("Fetched rows:", len(df) if df is not None else 0)
if df is not None and not df.empty:
    print("Countries found:", df['country'].unique())

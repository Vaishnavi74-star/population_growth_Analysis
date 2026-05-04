# Population Growth Analysis Project

A comprehensive tool for analyzing, visualizing, and forecasting global population trends using World Bank data.

## Features
- **Data Ingestion**: Automatic fetching from World Bank API with local CSV caching.
- **Preprocessing**: Cleans data, calculates YoY growth rates, and groups by decades.
- **Visualizations**: 
  - Interactive line & bar charts (Matplotlib/Seaborn).
  - Animated Bar Chart Race (Plotly).
  - Global Choropleth Maps (Plotly).
- **Modeling**: Exponential and Logistic growth fitting using Scipy.
- **Interactive Dashboard**: A premium Dash UI with filtering and forecasting tabs.

## Project Structure
```
population_growth_analysis/
├── data/               # Local cache for API data
├── notebooks/          # Analysis walkthrough
├── src/                # Core logic
│   ├── data_loader.py  # API integration
│   ├── preprocess.py   # Cleaning & feature engineering
│   ├── visualize.py    # Plotting functions
│   ├── analysis.py     # Scipy modeling
│   └── dashboard.py    # Plotly Dash UI
├── main.py             # CLI Entry point
└── requirements.txt    # Dependency list
```

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the CLI demo:
   ```bash
   python main.py
   ```
3. Launch the Dashboard:
   ```bash
   python -m src.dashboard
   ```

## Design Aesthetics
The dashboard uses this `LUX` theme for a premium, professional looks, and visualizations are configured with modern color palettes good for the more acurate thing
.

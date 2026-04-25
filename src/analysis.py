import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def exponential_model(t, p0, r):
    return p0 * np.exp(r * t)

def logistic_model(t, k, p0, r):
    return k / (1 + ((k - p0) / p0) * np.exp(-r * t))

class PopulationAnalyzer:
    def __init__(self, df):
        self.df = df

    def fit_growth(self, country_name):
        country_df = self.df[self.df['country'] == country_name].sort_values('year')
        if country_df.empty:
            return None, None
        
        # Normalize years: t=0 is the first year in the dataset
        t = country_df['year'].values - country_df['year'].min()
        p = country_df['population'].values
        
        # Initial guesses
        p0_guess = p[0]
        r_guess = 0.02 # 2% growth
        k_guess = p.max() * 2 # Carrying capacity guess
        
        results = {}
        
        # Exponential Fit
        try:
            popt_exp, _ = curve_fit(exponential_model, t, p, p0=[p0_guess, r_guess])
            results['exponential'] = popt_exp
        except:
            results['exponential'] = None
            
        # Logistic Fit
        try:
            popt_log, _ = curve_fit(logistic_model, t, p, p0=[k_guess, p0_guess, r_guess])
            results['logistic'] = popt_log
        except:
            results['logistic'] = None
            
        return results, country_df['year'].min()

    def predict_future(self, country_name, horizon_years=50):
        fit_results, start_year = self.fit_growth(country_name)
        if not fit_results:
            return None
            
        current_max_year = self.df[self.df['country'] == country_name]['year'].max()
        future_years = np.arange(current_max_year + 1, current_max_year + horizon_years + 1)
        t_future = future_years - start_year
        
        predictions = pd.DataFrame({'year': future_years})
        
        if fit_results['exponential'] is not None:
            predictions['exp_prediction'] = exponential_model(t_future, *fit_results['exponential'])
            
        if fit_results['logistic'] is not None:
            predictions['log_prediction'] = logistic_model(t_future, *fit_results['logistic'])
            
        return predictions

    def get_doubling_time(self, country_name):
        fit_results, _ = self.fit_growth(country_name)
        if fit_results and fit_results['exponential'] is not None:
            r = fit_results['exponential'][1]
            if r > 0:
                return np.log(2) / r
        return None

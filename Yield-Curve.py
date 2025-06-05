import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

FRED_API_KEY  = '3ebb96bdbc5bb4bc7df2868a9acd49a0'


# Dictionary of series IDs with corresponding maturities (in years)
series_ids = {
    'DGS1MO': 1/12, 'DGS3MO': 0.25, 'DGS6MO': 0.5,
    'DGS1': 1, 'DGS2': 2, 'DGS3': 3, 'DGS5': 5,
    'DGS7': 7, 'DGS10': 10, 'DGS20': 20, 'DGS30': 30
}

def get_latest_yield(series_id):
    url = f'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': 5  # Get last 5 in case some are null
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    for obs in data['observations']:
        value = obs['value']
        if value != '.':
            return float(value)
    return None

# Fetch latest yields
yields = {}
for series_id, maturity in series_ids.items():
    yield_value = get_latest_yield(series_id)
    if yield_value is not None:
        yields[maturity] = yield_value

# Convert to DataFrame and sort
df = pd.DataFrame(list(yields.items()), columns=['Maturity (Years)', 'Yield (%)'])
df = df.sort_values('Maturity (Years)')

# Plot the yield curve
plt.figure(figsize=(10, 6))
plt.plot(df['Maturity (Years)'], df['Yield (%)'], marker='o', linestyle='-', color='blue')
plt.title(f'U.S. Treasury Yield Curve ({datetime.today().strftime("%Y-%m-%d")})')
plt.xlabel('Maturity (Years)')
plt.ylabel('Yield (%)')
plt.grid(True)
plt.show()
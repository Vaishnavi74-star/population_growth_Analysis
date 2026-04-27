import requests

url = "https://api.worldbank.org/v2/country/CHN;IND;USA/indicator/SP.POP.TOTL"
params = {"format": "json", "date": "2020:2023", "per_page": 5000}
response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    if len(data) > 1:
        print(f"Success! Fetched {len(data[1])} records.")
        for r in data[1][:3]:
            print(r['country']['value'], r['date'], r['value'])
    else:
        print("No data.")
else:
    print("Failed.", response.status_code)

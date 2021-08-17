import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=FB&outputsize=compact&apikey=X86NOH6II01P7R24"
r = requests.get(url)
data = r.json()

print(data)
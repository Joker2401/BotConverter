import requests

r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
print(r.content)
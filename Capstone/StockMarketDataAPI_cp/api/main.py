import requests

EXCHANGE_ENDPOINT = 'https://api.apilayer.com/exchangerates_data/latest'
API_KEY = 'yx6okuDH1JdzfQeUX6JZOjSvCUm4oO4I'

currency_base = input('Enter the three-letter currency code of your preferred base currency: ').upper()
currency_to_exchange_to = input('Enter the currency code of your preferred one to exchange for: ').upper()
headers = {
    "apikey": API_KEY,
}
params = {
    'base': currency_base,

}

response = requests.get(EXCHANGE_ENDPOINT, params=params, headers=headers)
response_data = response.json()
data = response_data['rates'][str(currency_to_exchange_to)]

# print(response.json())
# print(currency_to_exchange_to)
print(data)
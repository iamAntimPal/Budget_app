import requests

class CurrencyConverter:
    def __init__(self):
        self.rates = {}
        self.update_rates()

    def update_rates(self):
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        self.rates = response.json()['rates']

    def convert(self, amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount
        return amount / self.rates[from_currency] * self.rates[to_currency]
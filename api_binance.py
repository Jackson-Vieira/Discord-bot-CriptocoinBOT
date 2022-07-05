import requests

from settings import COINS

"""
Função utilizada para se conectar a api e extrair as cotações das moedas expecificadas
"""

def api_binance(coins=COINS):
    r = requests.get('https://api.binance.com/api/v3/ticker/price')
    response = {}

    if r.status_code == 200:
        data = r.json()
        for coin in data:
            if coin['symbol'] in coins:
                response[coin['symbol']] = coin['price']

        return response

    else:
        pass
    
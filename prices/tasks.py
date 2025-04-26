from celery import shared_task
from celery.utils.log import get_task_logger
import requests
import json

logger = get_task_logger(__name__)

@shared_task
def sample_task():
    crypto_list = ["BTC", "ETH", "ADA","SCRT", "MANA"]
    #get binance prices
    crypto_list_binance = [f"{crypto}USDT" for crypto in crypto_list]
    crypto_list_processed_binance = json.dumps(crypto_list_binance, separators=(',', ':'))
    crypto_binance_json = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbols={crypto_list_processed_binance}').json()
    crypto_binance_prices = {dict['symbol'].replace("USDT", ""): float(dict['price']) for dict in crypto_binance_json} 
    #get bitkub prices
    crypto_bitkub_json = requests.get(f'https://api.bitkub.com/api/market/ticker').json()
    crypto_bitkub_prices = {}
    for crypto in crypto_list:
        crypto_bitkub = f'THB_{crypto}'
        if crypto_bitkub in crypto_bitkub_json:
            crypto_bitkub_prices[crypto] = float(crypto_bitkub_json[crypto_bitkub]['last']) #already float but convert again just in case
    #get bitkub usdt price    
    usdt_bitkub_price = float(crypto_bitkub_json['THB_USDT']['last'])  #already float but convert again just in case
    #calculate profits
    for crypto in crypto_list:
        usdt_profit_percentage = 1 / crypto_binance_prices[crypto] * crypto_bitkub_prices[crypto] / usdt_bitkub_price * 100 - 100
        thb_profit_percentage = 1 / crypto_bitkub_prices[crypto] * crypto_binance_prices[crypto] * usdt_bitkub_price * 100 - 100
        logger.info(f"Current {crypto} price: [BINANCE] {crypto_binance_prices[crypto]} --- [BITKUB] {crypto_bitkub_prices[crypto]} ||| profits USD: {usdt_profit_percentage}, profits THB: {thb_profit_percentage}")
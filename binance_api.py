from datetime import date, timedelta
import requests
import csv
import time
import pandas as pd

def get_price(coin_id):
    coin_price = []
    for i in range(7):
        start_at = date.today() - timedelta(days=7-i)
        end_at = date.today() - timedelta(days=7-i-1)

        start_at_timestamp = int(time.mktime(start_at.timetuple()))*1000
        end_at_timestamp = int(time.mktime(end_at.timetuple()))*1000

        url = 'https://api.binance.com/api/v3/klines?symbol='+coin_id+'&interval=1d&startTime='+str(start_at_timestamp)+'&endTime='+str(end_at_timestamp)
        response = requests.get(url)
        coin_price += response.json()
    return coin_price

def csv_to_xlsx(fileName):
    csv = pd.read_csv(fileName+'.csv', encoding='utf-8')
    csv.to_excel(fileName+'.xlsx', sheet_name='data')

if __name__ == '__main__':
    # url = 'https://api.binance.com//fapi/v1/ping?weight=1'
    # response = requests.get(url)
    coins_kinds = {'BTCUSDT': 'Bitcoin', 'ETHUSDT': 'Eth', 'XRPUSDT': 'XRP', 'ADAUSDT': 'Cardano', 'DOGEUSDT': 'Dogecoin', 
                  'SOLUSDT': 'Solana', 'MATICUSDT': 'Polygon', 'DOTUSDT': 'Polkadot', 'SHIBUSDT': 'Shiba Inu', 'TRXUSDT': 'TRON', 
                  'LTCUSDT': 'Litecoin', 'AVAXUSDT': 'Avalanche', 'LINKUSDT': 'Chainlink', 'ATOMUSDT': 'Cosmos', 
                  'ETCUSDT': 'Ethereum Classic', 'XMRUSDT': 'Monero', 'XLMUSDT': 'Stellar', 'BCHUSDT': 'Bitcoin Cash', 
                  'ALGOUSDT': 'Algorand', 'NEARUSDT': 'NEAR Protocol', 'QNTUSDT': 'Quant', 'VETUSDT': 'VeChain', 
                  'FILUSDT': 'Filecoin', 'APEUSDT': 'ApeCoin', 'FLOWUSDT': 'Flow', 'ICPUSDT': 'Internet Computer', 
                  'HBARUSDT': 'Hedera', 'EGLDUSDT': 'MultiversX (Elrond)', 'CHZUSDT': 'Chiliz', 'XTZUSDT': 'Tezos', 'EOSUSDT': 'EOS'}
    
    for coin in coins_kinds:
        try:
            with open(f'{coins_kinds[coin]}_binance_api.csv', 'w', encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Date', 'Closing Price', 'Trading Volume'])
                price = get_price(coin)
                totalVolume = 0
                totalPrice = 0
                print(f'Current processing:{coin}')
                
                for date_price in price:
                    closingPrice = date_price[4]
                    tradingVolume = date_price[5]
                    currentDate = time.localtime(date_price[0]/1000)
                    currentDate = time.strftime("%Y-%m-%d %H:%M:%S", currentDate)
                    writer.writerow([currentDate, closingPrice, tradingVolume])
                    totalPrice += float(closingPrice)
                    totalVolume += float(tradingVolume)
                
                averagePrice = totalPrice / 7
                averageVolume = totalVolume / 7
                # writer.writerow(['Average 7 days price', averagePrice])
                # writer.writerow(['Average 7 days volume', averageVolume])
            # csv_to_xlsx(f'{coins_kinds[coin]}_binance_api')

        except:
            print(f"Error occur when processing: {coin}")

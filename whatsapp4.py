#from apscheduler.schedulers.blocking import BlockingScheduler
from twilio.rest import Client
import json
import symbol
import schedule
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

#sched = BlockingScheduler()
#@sched.scheduled_job('interval', seconds=10)
def timed_job():
#global_url = 'https://api.coinmarketcap.com/v2/global/'
    global_url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest?CMC_PRO_API_KEY=bde43dde-3835-4ebf-8141-ed9fd1979407'
#quote_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?limit=100&CMC_PRO_API_KEY=bde43dde-3835-4ebf-8141-ed9fd1979407'

    request = requests.get(global_url)
    results = request.json()

#print(json.dumps(results, sort_keys=True, indent= 4))

    active_currencies = results['data']['active_cryptocurrencies']
    total_currencies = results['data']['total_cryptocurrencies']
    eth_dominance = results['data']['eth_dominance']

    active_markets = results['data']['active_market_pairs']
    bitcoin_percent = results['data']['btc_dominance']
#last_updated = results['data']['last_updated']
    global_cap = results['data']['quote']['USD']['total_market_cap']
    global_volume = results['data']['quote']['USD']['total_volume_24h']
    altcoin_market_cap = results['data']['quote']['USD']['altcoin_market_cap']
    print('Active currencies: ' + str(active_currencies))
    print('Total currencies :' + str(total_currencies))
    print('Total active market pairs: ' + str(active_markets))
    print('Total bitcoin\'s precentage: ' + str(bitcoin_percent))
    print('Total Ethereum\'s precentage: ' + str(eth_dominance))
#print('Last updates on: ' + str(last_updated))
    print('Total global marketcap: ' + str(global_cap))
    print('Total alt coin marketcap :' + str(altcoin_market_cap))
    print('Total 24hrs volume : ' + str(global_volume))


#request = requests.get(quote_url)
#results = request.json()

#print("Enter the name of cryptocurrecny to find the latest price:\n")
#input("Name : ")

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    coin = ['NANO','NEO','MATIC']
    j=0
    for x in coin :
        parameters = {

        'symbol': x

        }
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'bde43dde-3835-4ebf-8141-ed9fd1979407',
        }



        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            name_coin = data['data'][x]['name']
            price = data['data'][x]['quote']['USD']['price']
            cmc_rank = data['data'][x]['cmc_rank']
            percent_change = data['data'][x]['quote']['USD']['percent_change_24h']
            print("Name           : " + str(name_coin))
            print("Rank           : " + str(cmc_rank))
            print("Price          : $" + str(price))
            print("24hrs change   : " + str(percent_change) + "%")

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
        client = Client()

# this is the Twilio sandbox testing number
        from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your own WhatsApp Messaging number
        to_whatsapp_number='whatsapp:+919538769011'

        Dict = {1: name_coin, 2: price, 3: percent_change}
        client.messages.create(body='DETAILS',
                            from_=from_whatsapp_number,
                            to=to_whatsapp_number)
        i = 1
        while (i <= 3):
            print(Dict[i])
            client.messages.create(body=(Dict[i]),
                                from_=from_whatsapp_number,
                                to=to_whatsapp_number)
            i = i + 1
    return

#schedule.every().hour.do(timed_job)
schedule.every(2).minutes.do(timed_job)

while True:
   schedule.run_pending()


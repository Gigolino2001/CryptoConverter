import apikey
import requests

headers = {
    'X-CMC_PRO_API_KEY': apikey.key,
    'Accepts' : 'application/json'
}

url_coin = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
url2 = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
url_fiat = 'https://pro-api.coinmarketcap.com/v1/fiat/map'


class Manager:
    def __init__(self):
        self.__params_coins = {
            'start' : '1', 
            'limit' : '10' 
        }
        self.__params_fiats = {
            'start' : '1',
            'limit' : '25',
        }
        self.__coin = ''
        self.__fiat = ''
    

    def showall(self):
        ''' For Menu option 1 '''
        json = requests.get(url_coin, params=self.__params_coins, headers=headers).json()
        coins = json['data']
        count = 1
        for i in coins:
            print(str(count) + ':', i['name'], '(' + i['symbol'] + ')')
            count += 1
        print()

    def setlimit (self, value):
        ''' For Menu option 1 '''
        self.__params_coins['limit'] = str(value)

 
    def verifyCrypto(self, origin_coin, destination_coin):
        ''' For Menu option 2 '''
        origin_coin = origin_coin.upper().strip()
        destination_coin = destination_coin.upper().strip()
        json = requests.get(url_coin, params=self.__params_coins, headers=headers).json()
        coins = json['data']
        flag1, flag2 = False, False
        if origin_coin == destination_coin:
            return False
        for i in coins:
            if origin_coin == i['symbol']:
                flag1 = True
            elif destination_coin == i['symbol']:
                flag2 = True
        return flag1 and flag2

    def convert_tocrypto(self, origin_coin, quantity_oc, destination_coin):
        ''' For Menu option 2 '''
        params = {
            'symbol': '',
            'convert':'USD'
        }
        origin_coin = origin_coin.upper().strip()
        destination_coin = destination_coin.upper().strip()
        params['symbol'] = str(origin_coin + "," + destination_coin)
        json1 = requests.get(url2, params=params, headers=headers).json()
        coin_origin = json1['data'][origin_coin]['quote']['USD']['price']
        coin_destination = json1['data'][destination_coin]['quote']['USD']['price']
        return (coin_origin*quantity_oc)/coin_destination

    def show_fiats(self):
        ''' For Menu option 3 '''

        json = requests.get(url_fiat, params=self.__params_fiats, headers=headers).json()
        fiats = json['data']
        result = "["
        for i in fiats:
            result = result + i['symbol'] + ", "
        result = result[:-2] + "]"
        print(result)

    def verifyFiat(self, origin, destination):
        ''' For Menu option 3 '''
        origin = origin.upper().strip()
        destination = destination.upper().strip()
        json1 = requests.get(url_coin, params=self.__params_coins, headers=headers).json()
        json2 = requests.get(url_fiat, params=self.__params_fiats, headers=headers).json()
        coins = json1['data']
        fiats = json2['data']
        flag1, flag2 = False, False
        for i in coins:
            if origin == i['symbol']:
                flag1 = True
                self.__coin = origin
            elif destination == i['symbol']:
                flag1 = True
                self.__coin = destination
        for i in fiats:
            if destination == i['symbol']:
                flag2 = True
                self.__fiat = destination
            elif origin == i['symbol']:
                flag2 = True
                self.__fiat = origin
        return flag1 and flag2

    def convert_tofiat(self, origin, quantity, destination):
        ''' For Menu option 3 '''
        params_origin = {
            'symbol': '',
            'convert':''
        }
        origin =origin.upper().strip()
        destination = destination.upper().strip()
        if origin == self.__coin:
            params_origin['symbol'] = origin
            params_origin['convert'] = destination
            json = requests.get(url2, params=params_origin, headers=headers).json()
            coin_origin = json['data'][self.__coin]['quote'][self.__fiat]['price']
            return coin_origin*quantity
        else:
            params_origin['symbol'] = destination
            params_origin['convert'] = origin
            json = requests.get(url2, params=params_origin, headers=headers).json()
            coin_origin = json['data'][self.__coin]['quote'][self.__fiat]['price']
            return quantity/coin_origin

  
        

import requests
import json
from pathlib import Path

#************************CONFIG*******************************
key = None  #Assign your API Key here

cache_path = '' #Path to where the cache file will be stored 
#*************************************************************

headers = {
    'X-CMC_PRO_API_KEY': key,
    'Accepts' : 'application/json'
}

url_id_map = ' https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
url_coin = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
url_specific_query = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
url_fiat = 'https://pro-api.coinmarketcap.com/v1/fiat/map'
url_info = 'https://pro-api.coinmarketcap.com/v1/key/info'
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
        self.__coin_infos = ''
        #Fails if the key is left as None
        if key == None:
            raise ValueError('CoinMarketCap API Key not set! (change the \'key\' variable on the file Manager.py)')
        #loads cache if the file already exists defaults the cache file to folder where the file is located
        global cache_path
        if cache_path == '':
            cache_path = 'coin_info_cache.json'
        if Path(cache_path).exists():
                with open(cache_path, 'r') as cached:
                    self.__coin_infos   = json.load(cached)
        
    def showall(self):
        ''' For Menu option 1 '''
        if self.__coin_infos == '':
            print('Cache file not found, update cache or abort?' + '')
            while True:
                try:
                    
                    option = input('Enter your choice[U/a]:')
                    clean = option.lower().strip()
                    if clean in ['','u']:
                        if not self.update_cache():
                            break
                        break
                    elif clean == 'a':
                        return
                    else:
                        raise ValueError()
                except ValueError:
                    print('Can\'t recognize this option')     
        
        if self.__coin_infos == '':
            print('Can\'t show listing')
            return
        json_info = self.__coin_infos
        coins = json_info['data']
        count = 1
        limit = int(self.__params_coins['limit'])+1
        limit_strlen = len(self.__params_coins['limit'])-1
        for i in coins:
            if count == limit:
                break
            print(str(count) + ':', i['name'], '(' + i['symbol'] + ')', '\tid: '+ str(i['id']))
            count += 1
        print()

    def setlimit (self, value):
        ''' For Menu option 1 '''
        self.__params_coins['limit'] = str(value)

 
    def verifyCrypto(self, origin_coin, destination_coin):
        ''' For Menu option 2 '''
        origin_coin = origin_coin.upper().strip()
        destination_coin = destination_coin.upper().strip()
        request = requests.get(url_coin, params=self.__params_coins, headers=headers)
        if request.status_code == 200:
            json_info = request.json()
            coins = json_info['data']
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
        params['symbol'] = str(origin_coin + ',' + destination_coin)
        request = requests.get(url_specific_query, params=params, headers=headers)
        if request.status_code == 200:
            json1 = request.json()
            coin_origin = json1['data'][origin_coin]['quote']['USD']['price']
            coin_destination = json1['data'][destination_coin]['quote']['USD']['price']
            return (coin_origin*quantity_oc)/coin_destination

    def show_fiats(self):
        ''' For Menu option 3 '''

        json = requests.get(url_fiat, params=self.__params_fiats, headers=headers).json()
        fiats = json['data']
        result = '['
        for i in fiats:
            result = result + i['symbol'] + ', '
        result = result[:-2] + ']'
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
            json = requests.get(url_specific_query, params=params_origin, headers=headers).json()
            coin_origin = json['data'][self.__coin]['quote'][self.__fiat]['price']
            return coin_origin*quantity
        else:
            params_origin['symbol'] = destination
            params_origin['convert'] = origin
            json = requests.get(url_specific_query, params=params_origin, headers=headers).json()
            coin_origin = json['data'][self.__coin]['quote'][self.__fiat]['price']
            return quantity/coin_origin
    
    def update_cache(self):
        '''For menu option 4'''
        try:
            failed_request = True
            if self.get_current_apikey_credits()[1] == 0:
                print('Can\'t update cache,you have no credits left!')
                eta_for_reset = self.get_eta_daily_reset()
                if eta_for_reset:
                    print('Daily credit reset i' + eta_for_reset[1:])
                raise Exception
            elif self.get_current_apikey_credits() is None:
                print('Couldn\'t assess if you currently have API credits left')
                while True:
                    try:
                        print('Cache file not found, update cache or abort?' + '')
                        option = input('Enter your choice[U/a]:')
                        clean = option.lower().strip()
                        if clean in ['','u']:
                            self.update_cache()
                            break
                        elif clean == 'a':
                            return
                        else:
                            raise ValueError()
                    except ValueError:
                        print('Can\'t recognize this option')    

            with open(cache_path,'w+') as cached:
                request = requests.get(url_id_map, headers=headers)
                if request.status_code == 200:
                    json_info = request.json()
                    json.dump(json_info,cached)
                    cached.seek(0)
                    self.__coin_infos = json.load(cached)
                    print('Cache updated successfully!')
                    failed_request = False
            if failed_request:
                raise Exception                    
        except:
            self.__coin_infos = ''
            print('Cache update failed!')
            return False

    def show_apikey_info(self):
        pass
        #json = requests.get(url_info, params=self.__params_coins, headers=headers).json()

    def get_current_apikey_credits(self):
        '''Helper function that returns both the amount of credits used and the amount left '''
        request = requests.get(url_info, headers=headers)
        if request.status_code == 200:
            json_info = request.json()
            return (json_info['data']['usage']['current_day']['credits_used'],json_info['data']['usage']['current_day']['credits_left'])
        else:
            return False
    def get_eta_daily_reset(self):
        '''Helper function that returns a string containing the ETA fro '''
        request = requests.get(url_info, headers=headers)
        if request.status_code == 200:
            json_info = request.json()
            return json_info['data']['plan']['credit_limit_daily_reset']
        else:
            return None
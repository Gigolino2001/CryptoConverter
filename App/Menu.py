from Manager import CACHE_COIN_PATH, CACHE_FIAT_PATH, Manager
class Menu:
    def __init__(self):
        self.__options = {
            1:'Show available Cryptocurrencies (and their Symbol and CoinMarketCap id)', #DONE
            2:'Convert Crypto <-> Crypto', #DONE
            3:'Convert Crypto <-> Fiat',
            4:'Update cache',
            5:'Show your API key info (limits,etc)',
            6:'Exit'  
        }
        

    def print_menu(self,manager):
        print('\t   MENU ')
        api_info = manager.get_current_apikey_credits()
        print('API Credits remaining: '+str(api_info[1]) + '/' + str(api_info[0]+ api_info[1]))
        for key in self.__options.keys():
            print(str(key) + ':', self.__options[key])


    def start(self):
        manager = Manager()
        while True:
            try:
                print("Do you want to update the listing cache?")
                option = input('Enter your choice[Y/n]:')
                clean = option.lower().strip()
                if clean in ["","y"]:
                    manager.update_caches()
                    break
                elif clean == "n":
                    break
                else:
                    raise ValueError()
            except ValueError:
                print("Can't recognize this option")

        while True:
            self.print_menu(manager)
            option = ''
            try:
                option = int(input('Enter your choice:'))
                assert 0 < option < 7
            except (AssertionError,ValueError):
                print("Can't recognize this option. Please choose an option between 1 and 6.\n")
                continue

            if option == 1:
                try:
                    limit = int(input("Enter the limit: "))
                    assert 1 <= limit
                    manager.setlimit(limit)
                    manager.showall_coins()
                except (AssertionError, ValueError, KeyError):
                    print("Enter a valid limit")
                    continue

               
            elif option == 2:
                try:
                    origin_coin = str(input("Convert from: "))
                    quantity_oc = float(input("Insert amount: "))
                    destination_coin = str(input("Convert to: "))
                except:
                    print("Enter a valid option")
                    continue
                if not manager.verifyCrypto(origin_coin, destination_coin):
                    print("Enter a valid option")
                else:
                    result = manager.convert_tocrypto(origin_coin, quantity_oc, destination_coin)
                    print(quantity_oc, origin_coin.upper().strip() + " = " + str(round(result, 5)), destination_coin.upper().strip() +"\n") 
            elif option == 3:
                if manager.show_fiats() == None:
                    continue
                try:
                    origin = str(input("Convert from: "))
                    quantity = float(input("Insert amount: "))
                    destination = str(input("Convert to: "))
                except:
                    print("Enter a valid option")
                    continue
                if not manager.verifyFiat(origin, destination):
                    print("Enter a valid option")
                else:
                    result = manager.convert_tofiat(origin, quantity, destination)
                    print(quantity, origin.upper().strip() + " = " + str(round(result, 5)), destination.upper().strip() +"\n") 
            elif option == 4:
                options = {
                    1: 'Update Cryptocurrencies cache only [1 API credit]',
                    2: 'Update fiat cache only [1 API credit]',
                    3: 'Update both caches  [2 API credits]',
                    4: 'Return to main menu'
                }
                while True:
                    try:
                        print("CACHE UPDATE OPTIONS")
                        for key,text in options.items():
                            print(str(key) + ':',text)
                        suboption = int(input('Enter your choice:'))

                        assert 0 < suboption < 5

                        if suboption == 1:
                            manager.update_cache(CACHE_COIN_PATH)
                        elif suboption == 2:
                            manager.update_cache(CACHE_FIAT_PATH)
                        elif suboption == 3:
                            manager.update_caches()
                        elif suboption == 4:
                            break
                        else:
                            raise ValueError
                        break
                    except (ValueError,AssertionError):
                        print("Can't recognize this option")
            elif option == 5:
                manager.show_apikey_info()
            elif option == 6:
                print("Success!\nExiting...")
                exit()
            


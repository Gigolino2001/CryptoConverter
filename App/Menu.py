from Manager import Manager
class Menu:
    def __init__(self):
        self.__options = {
            1:'Show available coins (and their Symbol and CoinMarketCap id)', #DONE
            2:'Convert Crypto <-> Crypto', #DONE
            3:'Convert Crypto <-> Fiat',
            4:'Update cache',
            5:'Show your API key info (limits,etc)',
            6:'Exit'  
        }
        

    def print_menu(self):
        print('\t   MENU ')
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
                    manager.update_cache()
                    break
                elif clean == "n":
                    break
                else:
                    raise ValueError()
            except ValueError:
                print("Can't recognize this option")

        while True:
            self.print_menu()
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
                    manager.showall()
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
                manager.show_fiats()
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
                manager.update_cache()
            
            elif option == 5:
                pass
            elif option == 6:
                print("Success!\nExiting...")
                exit()
            


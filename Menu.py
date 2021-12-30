from Manager import Manager
class Menu:
    def __init__(self):
        self.__options = {
            1:'Show available coins', #DONE
            2:'Convert Crypto <-> Crypto', #DONE
            3:'Convert Crypto <-> Fiat',
            4:'Exit'
        }
        

    def print_menu(self):
        print('\t   MENU ')
        for key in self.__options.keys():
            print (str(key) + ':', self.__options[key])


    def start(self):
        manager = Manager()
        while(True):
            self.print_menu()
            option = ''
            try:
                option = int(input('Enter your choice:'))
                assert 0 < option < 5
            except (AssertionError,ValueError):
                print("Can't recognize this option. Please choose an option between 1 and 4.\n")
                continue

            if option == 1:
                try:
                    limit = int(input("Enter the limit: "))
                    assert 1 < limit
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
                print("success!")
                exit()
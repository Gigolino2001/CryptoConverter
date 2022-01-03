# CryptoConverter

This application has the goal of giving its user an easier way of controlling and managing their cryptos assets in real time.
The app offers a set of 4 options that the user can choose from:
## Menu Options
- **Option 1:** Show available coins, where the user can choose the number of coins that he wanna see.  
Example : 
            
            "Enter the limit: 15"
            
- **Option 2:** Convert Crypto to Crypto, where the user can choose one crypto to convert to another.  
Example :
            
            "Convert from: BTC"
            "Insert amount: 1"     
            "Convert to: ETH"
- **Option 3:** Convert Crypto to Fiat or Fiat to Crypto, where the user can choose one crypto/fiat to convert to another fiat/crypto.  
Example : 
            
            "Convert from: BTC"
            "Insert amount: 5"
            "Convert to: USD"
- **Option 4:** Exit, where the user can leave the CryptoConverter.

## ApiKey
In order for the program to properly work the user needs an Api key which is private and unique for each user so it is necessary to grab the key before testing the program.
To grab the key the user must:
 - Visit CoinMarketCap website (which is the server responsible for updating and giving the coins information);
 - Go to "products";
 - "Crypto Api";
 - "Get your Api Key now";
 - Sign up to the basic plan;

 Or simply go to https://coinmarketcap.com/api/ and get the key here.
 The final step is to copy the key generated for the user and paste it in the file called [apikey.py](https://github.com/Gigolino2001/CryptoConverter/blob/main/App/apikey.py).

## How to run
- Install Python:

    In your machine, make sure that you have python installed, if not:
  - [Python Instalation Guide](https://www.python.org/downloads/)

- Install Requests:
    
    Make sure that you install Requests after python:

```bash
python -m pip install requests
 ```
 
- Open the console in your machine and run the follow commands:

```bash
cd {Path File}
python "app.py" 
 ```

## Authors
|                                                       |
|-------------------------------------------------------|
| [Gonçalo Nascimento](https://github.com/Gigolino2001) |
| [Mário Viegas](https://github.com/Marioviegas2001)    |


## License
- [License](https://github.com/Gigolino2001/CryptoConverter/blob/main/LICENSE)

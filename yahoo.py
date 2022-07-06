import requests
import time
from bs4 import BeautifulSoup as soup

def main():
    # This is the base URL for the ticker
    base_url = 'https://finance.yahoo.com/quote/'
    
    # List of the stocks what we want to check
    stocks = ["AAPL", "MSFT", "GME", "GOOG", "T"]
   
    for ticker in stocks:
        # Get the source code of the website
        result = requests.get(base_url + ticker)
        
        # If everything is ok, we do this
        if result.status_code == 200:
            # Get the text from the data what we got. This is the source code of the page
            source = result.text
            parsedPage = soup(source, 'html.parser')
            
            # Price element:
            # <fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="AAPL" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="141.56" active="">141.56</fin-streamer>
            #Find the price of the ticker
            try:
                price = parsedPage.find('fin-streamer', attrs={'data-symbol':'AAPL'}, class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text
            except:
                price = parsedPage.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text
            
            # Find the delta of the price
            # <fin-streamer class="Fw(500) Pstart(8px) Fz(24px)" data-symbol="AAPL" data-field="regularMarketChangePercent" data-trend="txt" data-pricehint="2" data-template="({fmt})" value="0.018930433" active="">
                # <span class="C($positiveColor)">
                 # (+1.89%)
                # </span>
            # </fin-streamer>
            try:
                try:
                    delta = parsedPage.find('fin-streamer', attrs={'data-test':'qsp-price-change'}).text
                except:
                    delta = parsedPage.find('fin-streamer', class_= 'Fw(500) Pstart(8px) Fz(24px)').text
            except:
                delta = "Cannot find data"

            # Find the percentage of the price change
            try:
                try:
                    percentage = parsedPage.find('fin-streamer', attrs={'data-field':'regularMarketChangePercent'}, class_= 'Fw(500) Pstart(8px) Fz(24px)').text
                except:
                    percentage = parsedPage.find('fin-streamer', class_= 'Fw(500) Pstart(8px) Fz(24px)').text
            except:
                percentage = "Cannot find data"
            
            # Get the name of the current ticker
            name = parsedPage.find('h1', class_= 'D(ib) Fz(18px)').text
            # Write out the data what we got
            print(name + ": $" + price +" | "+ delta + percentage)
            # Write out the link for the current ticker
            print(f'\t {base_url + ticker}')
            
        else:
            # Write out message if we do not get any data
            print(f'[X] Failed: the request to page {base_url + ticker} failed. Status code: {result.status_code}')
        # Wait a little bit to avoid overload the server
        time.sleep(1)

    return

if __name__ == '__main__':
    main()
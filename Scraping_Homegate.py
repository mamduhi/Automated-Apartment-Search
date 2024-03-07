## Import required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd


# Initializing the list
simple = []

# Defining functions to call later / getting the page
def getLink(page):
    return f"https://www.homegate.ch/rent/apartment/city-zurich/matching-list?ep={page}"

# Accessing data from Homegate.ch web and making it visually nice
def fetch_rental_data():
    cur_page = 1
    while True:
        print("Page ->", cur_page)
        link = getLink(cur_page)
        res = requests.get(link)
        bs = BeautifulSoup(res.text, features='html.parser')

        b = bs.find_all('div', {'class': 'ResultList_listItem_j5Td_'})

        ## if we get zero results then we break the while loop defined earlier (we have usually around 40 pages of results)

        if len(b) == 0:
            break

        for offer in b:
            simple.append(offer)

        print(len(simple))
        cur_page += 1

# Collecting required data for "price", "size", ""number of rooms" and "address".
# The used strings may change in future!
def extractPremiumInfo(block):
    result = {
        'price': None,
        'size': None,
        'rooms': None,
        'address': None
    }
    try:
        price = block.find('span', {'class': 'HgListingCard_price_sIIoV'}).text
        result['price'] = price
    except:
        pass

    try:
        m2 = block.find('div', {'class': 'HgListingRoomsLivingSpace_roomsLivingSpace_FiW9E'}).find_all('span')[1].text
        result['size'] = m2
    except:
        pass

    try:
        rn = block.find('div', {'class': 'HgListingRoomsLivingSpace_roomsLivingSpace_FiW9E'}).find_all('span')[0].text
        result['rooms'] = rn
    except:
        pass

    try:
        address = block.find('address').get_text()
        result['address'] = address
    except:
        pass

    return result

# Main code: creat a CSV file with the required data from the homegate.ch site
if __name__ == '__main__':
    fetch_rental_data()
    finish = []
    for i in simple:
        finish.append(extractPremiumInfo(i))
    print(f"Found {len(finish)}apartments")
    df = pd.DataFrame(finish)
    df.to_csv('Zurich.csv', index=False, encoding='utf-8')
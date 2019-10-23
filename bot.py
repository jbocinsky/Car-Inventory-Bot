import requests
from bs4 import BeautifulSoup 
import re
import csv
import time
import os
import sys
from sms import send_sms


base_path = "J:\\Projects\\OffLeaseBot\\"


URL = 'https://www.offleaseonly.com/used-mazda-cx-9.htm'

r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib') 
# print(soup.prettify()) 

#Get all divs that contain a class name starting with 'vehicle-listing'
divs = soup.select("div[class^=vehicle-listing]")

#Initiate listings dictionary
listings = []

file_name = base_path + 'listings.txt'

with open(file_name) as f:
    prev_listings = [tuple(line) for line in csv.reader(f, delimiter = '\t')]

print('PREVIOUS DATA:')
print(prev_listings)

f = open(file_name, 'a+')

new_car_flag = 0

#Iterate over all listings to create a dictionary of listings
for div in divs:

    # print(div)

    car_name = div.select('a[href^="/used-car"]')[0].text

    mileage_div = div.select('tr[class^="mileage"]')
    mileage = re.search('td>(.*)</td', str(mileage_div[0])).group(1)

    color_div = div.select('tr[class^="exterior-color"]')
    color = re.search('td>(.*)</td', str(color_div[0])).group(1)

    price_div = div.select('div[class^="our-price"]')
    # print(price_div)

    price = re.search('"value">(.*)</div>', str(price_div[0])).group(1)

    # print(car_name)
    # print(mileage)
    # print(color)
    # print(price)

    tup = (car_name, color, mileage, price)
    listings.append(tup)

    if(tup not in prev_listings):
        print('Adding listing:' + str(tup))
        f.write('\t'.join(str(s) for s in tup) + '\n')

        msg = 'New car on ' + URL + '\nName: ' + tup[0] + '\nMileage: ' + tup[2] + '\nColor: ' + tup[1] + '\nPrice: ' + tup[3]
        print(msg)

        #Text user of new car using twillio
        send_sms(msg)

        new_car_flag = 1

if(not new_car_flag):
    msg = "There are no new cars on " + URL
    send_sms(msg)

f.close()
print('Done...')
print('Shutting Down...')
time.sleep(10)

os.system("shutdown /s /f /t 1")
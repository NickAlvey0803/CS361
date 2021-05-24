from bs4 import BeautifulSoup
import json
import requests
title = "Compare Run Times"

# URL = 'https://cs361-ul-scraper.herokuapp.com/List_of_world_records_in_athletics/1'
# page = requests.get(URL)
# table_dict = page.json()
# test_dict = {}
#
# for key, val in table_dict.items():
#     if key != 'W' and key != 'N' and key != 'R' and key != 'V' and key != 'P':
#         test_dict[key] = val
#
# new_dict = {}
#
# for item, val in test_dict.items():
#     for key, data in val.items():
#         try:
#             new_dict[key].append(data)
#         except:
#             new_dict[key] = [data]
#
# print(new_dict)

# URL = 'https://alveyn-cs361-getlocation.herokuapp.com/getlocation'
# page = requests.get(URL)
# loc_dict = page.json()
#
# lat = float(loc_dict["latitude"])
# long = float(loc_dict["longitude"])
#
# print(lat)
# print(long)

URL = 'https://www.geodatatool.com'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
string_list = []

for div in soup.findAll('div', {'class': 'data-item'}):
    # print(div.prettify())

    for string in soup.strings:
        # print(string)
        if string != '\n':
            string_list.append(string)

string_dict = {}


string_dict["latitude"] = string_list[string_list.index('Latitude:') + 1]
# string_dict["IP address"] = string_list[string_list.index('IP Address:') + 1]
# string_dict["MY IP ADD"] = str(ip)
string_dict["City"] = string_list[string_list.index('City:') + 1]
string_dict["Region"] = string_list[string_list.index('Region:') + 1]
string_dict["Zip"] = string_list[string_list.index('Postal Code:') + 1]
string_dict["Country"] = string_list[string_list.index('Country Code:') + 1]
string_dict["longitude"] = string_list[string_list.index('Longitude:') + 1]

print(string_dict)
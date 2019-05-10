import sys
import requests
from bs4 import BeautifulSoup
import csv

reload(sys)
sys.setdefaultencoding('utf8')

base_url = "https://www.tripadvisor.it/RestaurantSearch?Action=FILTER&geo={}&itags=9909%2C9900%2C9901%2C11776%2C10591&sortOrder=relevance&geobroaden=false&o=a{}"
email_address = ''
tel = ''
file_name = 'results'
loc_list = ['194851', '1016807', '1186281', '5978712',
            '1028703', '194830', '4327477', '187903',
            '644273', '644270', '3844674', '1185507',
            '664014', '635877', '1076562', '1025218',
            '1187123']
added_id_list = []

with open('results.csv', mode='a') as result_file:
    res_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for loc_id in loc_list:
        for i in range(0, 120, 30):
            r = requests.get(base_url.format(loc_id, i))
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            for item in soup.findAll('div', class_='listing'):
                try:
                    item_id = item['id'].split('_')[1]
                    if item_id in added_id_list:
                        continue
                except:
                    continue
                try:
                    rating = ((item.find('span', class_='ui_bubble_rating')['alt']).split(' '))[1]
                    name = (item.find('a', class_='property_title').text).replace('\n', '')
                    pop_index = (item.find('div', class_='popIndex').text).replace('\n', '').split(' ')
                except:
                    continue
                if rating == '0' or rating == '0,5' \
                    or rating == '1' or rating == '1,5' \
                    or rating == '2' or rating == '2,5' \
                    or rating == '3':
                    continue
                pop_index_len = len(pop_index)
                tot_items = pop_index[3]
                category = pop_index[4] if pop_index_len < 9 else pop_index[4] + " " + pop_index[6]
                location = pop_index[6] if pop_index_len < 9 else pop_index[8]
                item_url = "https://www.tripadvisor.it" + item.find('a', class_='property_title')['href']
                r1 = requests.get(item_url)
                data1 = r1.text
                soup1 = BeautifulSoup(data1, 'html.parser')
                for a in soup1.select("a[href^=mailto:]"):
                    email_address = a["href"][7:].replace('?subject=?', '')
                    print email_address
                    break
                for a in soup1.select("a[href^=tel:]"):
                    tel = a["href"][4:]
                    print tel
                    break
                res_writer.writerow([item_id, name, category, location, email_address, tel, rating.replace(',', '.')])
                added_id_list.append(item_id)
                email_address = ''
                tel = ''


# [] Pistoia 194851
# [] Pescia 1016807
# [] Massa e Cozzile 1186281
# [] Collodi 5978712
# [] Monsummano 1028703
# [] Montecatini 194830
# [] Montecatini Alto 4327477
# [] Vinci 187903
# [] Carmignano 644273
# [] Artimino 644270

# [] Casalguidi 3844674
# [] Serravalle Pistoiese 1185507
# [] San Baronto 664014
# [] Lamporecchio 635877
# [] Comeana
# [] Montevettolini
# [] Fucecchio 1076562
# [] Buggiano 1025218
# [] Uzzano 1187123
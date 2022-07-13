import requests
import pandas
from bs4 import BeautifulSoup

l = []
base_url = 'https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s='
r = requests.get(base_url)
c = r.content
soup = BeautifulSoup(c, 'html.parser')
all = soup.find_all('div', {'class':'propertyRow'})
page_number = soup.find_all('a', {'class':'Page'})[-1].text

for page in range(0,int(page_number)*10,10):
    r = requests.get(base_url+str(page))

    for item in all:
        dic = {}
        dic['Price'] = item.find('h4', {'class':'propPrice'}).text.replace('\n','').replace(' ','')
        dic['Address'] = item.find_all('span', {'class','propAddressCollapse'})[0].text
        dic['Locality'] = item.find_all('span', {'class','propAddressCollapse'})[1].text
        try:
            dic['Beds'] = item.find('span', {'class','infoBed'}).find('b').text
        except:
            dic['Beds'] = None
        try:
            dic['Full Baths'] = item.find('span', {'class','infoValueFullBath'}).find('b').text
        except:
            dic['Full Baths'] =None
        try:
            dic['Half Bath'] = item.find('span', {'class','infoValueHalfBath'}).find('b').text
        except:
            dic['Half Bath'] = None
        try:
            dic['Area'] = item.find('span', {'class','infoSqFt'}).find('b').text
        except:
            dic['Area'] = None

        for column_group in item.find_all('div', {'class':'columnGroup'}):
            for feature_group, feature_name in zip(column_group.find_all('span', {'class':'featureGroup'}), column_group.find_all('span', {'class':'featureName'})):
                if 'Lot Size' in feature_group.text:
                    dic['Lot Size'] = feature_name.text
        l.append(dic)

df = pandas.DataFrame(l)
df.to_csv('Scrap.csv')
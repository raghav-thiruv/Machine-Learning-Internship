import requests
import csv
from bs4 import BeautifulSoup

# scrape the URL
URL = "https://forums.tapas.io/"
page = requests.get(URL)
temp_list = []
soup = BeautifulSoup(page.content, "html.parser")
# GET all SPAN tags from soup
temp_list = soup.find_all('span')

# get all PROMOTIONS category
count=0
line=0
found=0
promotion_views=0
for items in temp_list:
	#print(count,': ',items)
	if (line == 1):
                s0=str(temp_list[count])
                s1=s0.rpartition('(')
                s2=s1[2].rpartition(')')
                promotion_views=promotion_views+int(s2[0])
                found=0
                line=0
	first_find = str(items)
	if(first_find.find('/c/promotions') > 0):
                #print('first:', first_find, '\n', first_find.find("promotions"))
                found=1
	if(found == 1):
                line=line+1

	count=count+1
print('Promotion Views :', promotion_views)

############
# get all COLLABORATIONS  category
temp_list = soup.find_all('span')
count=0
line=0
found=0
Collaborations_views=0
for items in temp_list:
	#print(count,': ',items)
	if (line == 1):
                s0=str(temp_list[count])
                #print('MATCH2', temp_list[count])
                s1=s0.rpartition('(')
                s2=s1[2].rpartition(')')
                Collaborations_views=Collaborations_views+int(s2[0])
                found=0
                line=0
	first_find = str(items)
	if(first_find.find('/c/collaborations') > 0):
                #print('MATCH', temp_list[count])
                found=1
	if(found == 1):
                line=line+1
	count=count+1
print('Collaborations Views :', Collaborations_views)
############

############
# get all Off Topic  category
temp_list = soup.find_all('span')
count=0
line=0
found=0
OffTopic_views=0
for items in temp_list:
	#print(count,': ',items)
	if (line == 1):
                s0=str(temp_list[count])
                #print('MATCH2', temp_list[count])
                s1=s0.rpartition('(')
                s2=s1[2].rpartition(')')
                OffTopic_views = OffTopic_views+int(s2[0])
                found=0
                line=0
	first_find = str(items)
	if(first_find.find('/c/Off-Topic') > 0):
                #print('MATCH', temp_list[count])
                found=1
	if(found == 1):
                line=line+1
	count=count+1
print('Off-topic Views :', OffTopic_views)
############


# CSV file creation
header = ['Category', 'Views']
data = ['Promotions', promotion_views]
data1 = ['Collaborations', Collaborations_views]
data2 = ['Off-Topic', OffTopic_views]


with open('tapas.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
	#write the data
    writer.writerow(data)
    writer.writerow(data1)
    writer.writerow(data2)

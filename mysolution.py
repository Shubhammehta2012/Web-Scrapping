import os
import re

try:
    from urllib.request import urlopen
except:
    print('trying to install')
    os.system('python -m pip install urllib2')
    from urllib.request import urlopen

try:
    from bs4 import BeautifulSoup
except:
    print('trying to install')
    os.system('python -m pip install BeautifulSoup4')
    from bs4 import BeautifulSoup

try:
    from datetime import datetime, timedelta
except:
    print('trying to install')
    os.system('python -m pip install datetime')
    from datetime import datetime, timedelta

try:
    import copy
except:
    print('trying to install')
    os.system('python -m pip install copy')
    import copy

try:
    import ipywidgets as widgets
except:
    print('trying to install')
    os.system('python -m pip install ipywidgets')
    import ipywidgets as widgets

try:
    from texttable import Texttable
except:
    print('trying to install')
    os.system('python -m pip install texttable')
    from texttable import Texttable


class parseValue:
    post = ''
    date = ''
    location = ''
    catagory = ''
    tags = ''
    
    def __init__(self):
        pass
    

dated = input('Please enter the date you want to select as yyyy-mm-dd')
dates_dis = copy.deepcopy(dated)
if dated and re.match('\d\d\d\d-\d\d-\d\d', dated):
	dated = str(datetime.strptime(dated, '%Y-%m-%d') - timedelta(days=1))[:11].strip()



objects = []
links = []
all_pages = []
now = datetime.now()
now = str(now)[:11]
week = datetime.now() - timedelta(days=7)
week = str(week)[:11]
chk = True
found = False
if dated and re.match('\d\d\d\d-\d\d-\d\d', dated):
    week = dated
    found = True
    
my_link = 'https://www.newswire.com/newsroom'
while(chk):

    page = urlopen(my_link)
    soup = BeautifulSoup(page, 'html.parser')

    for i in soup.find_all("div", class_='chunkination chunkination-centered'):
        for j in i.find_all('a'):
            all_pages.append('https://www.newswire.com/' + str(j.get('href')))

    my_link = all_pages[-1]

    for i in soup.find_all("time", class_='ln-date'):
        objects.append(parseValue())
        objects[-1].date = i.get('datetime')

    for j in soup.find_all("a", class_='content-link'):
        links.append('https://www.newswire.com/' + str(j.get('href')))
        
    if str(objects[-1].date[:11]).strip() == str(week).strip():
        chk = False

w = 0
v = 0
add = []
for k in links:
    page1 = urlopen(k)
    soup1 = BeautifulSoup(page1, 'html.parser')
    post = soup1.find('h1', class_='mb-10 article-header').text
    objects[w].post = post
    loc = soup1.find('strong', class_='date-line color-pr').text
    a = loc.split('\n\t\t\t')
    objects[w].location = a[1]
    cat = soup1.article.find_all('p', class_='mb-0')
    for val in cat:
        try:
            stg = val.find('strong').text
            if stg == 'Categories:':
                chk = val.find('a').text
                objects[w].catagory = chk
            if stg == 'Tags:':
                for th in val.find_all('a'):
                    add.append(th.text)
                objects[w].tags = add
                add = []
        except:
            pass
    w = w+1


t = Texttable()
dis = [['post','Location', 'Catagory', 'Tag']]

for obj in objects:
    if found:
        if str(obj.date)[:len(dates_dis)] == dates_dis:
            dis.append([obj.post, obj.location, obj.catagory, obj.tags])
    else:
        dis.append([obj.post, obj.location, obj.catagory, obj.tags])

t.add_rows(dis) 
print (t.draw())




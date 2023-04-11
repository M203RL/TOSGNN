import requests
from bs4 import BeautifulSoup
import random
import time
from pathlib import Path
import os

def formatTime(time):
    if time<10:
        return '0'+str(time)
    else:
        return str(time)

cd = Path(__file__).parent.resolve()
file = 'Link.txt'
path = os.path.join(cd, file)
target = '神魔之塔'
tStart=time.time()
t = time.localtime()
years = int(time.strftime('%y', t))

result = time.strftime("%Y/%m/%d %H:%M:%S", t)
print(f"Start Time: {result}")

user_agent_list = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', 
                   'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', 
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36', 
                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36', 
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36', 
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36', 
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36', 
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68', 
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36', 
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36']


open(path, 'w').close()

yearlength = years - 12

idx = 0
for k in range(yearlength):
    for j in range(12):
        year = years - k
        month = 12 - j
        url = f'https://gnn.gamer.com.tw/?yy=20{str(year)}&mm={str(month)}'

        headers = {'User-Agent': random.choice(user_agent_list)}
        response = requests.get(url = url, headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')
        tart = soup.find_all("div", {"class": "GN-lbox2B"})
        for i in tart:
            text = str(i)
            if target in text:
                dir = i.find('a')
                if not 'https:' in dir:
                    try:
                        myLink = 'https:' + dir.get('href')
                        response = requests.get(url = myLink, headers = headers)
                        soup = BeautifulSoup(response.text, 'lxml')
                        pArticle = soup.find("div", {"class": "BH-lbox GN-lbox3 gnn-detail-cont"})
                        h1 = pArticle.find('h1').text.strip()
                        fi = open(path, 'r', encoding = 'utf8')
                        rec = fi.read()
                        fi = open(path, 'w', encoding = 'utf8')
                        fi.write(rec + h1 + '\n' + myLink + '\n\n')
                        fi.close()
                    except AttributeError:
                        pass
        tCurrent = time.time()
        tLapsed = round(tCurrent - tStart)
        m, s = divmod(tLapsed, 60)
        h, m = divmod(m, 60)
        h = formatTime(h)
        m = formatTime(m)
        s = formatTime(s)
        print(f'Time Lapsed: {h}:{m}:{s}, Loops: {str(idx)}(20{str(year)}/{str(month)})', end = "\r")
        time.sleep(3)
        idx += 1

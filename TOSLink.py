import requests
from bs4 import BeautifulSoup
import random
import time

def formatTime(time):
    if time<10:
        return '0'+str(time)
    else:
        return str(time)

target = '神魔之塔'
tStart=time.time()
t = time.localtime()

result = time.strftime("%Y/%m/%d %H:%M:%S", t)
print("Start Time: "+result)

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)", "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"]
file='Link.txt'
idx=0
for k in range(2):
    for j in range(12):
        year=23-k
        month=12-j

        url='https://gnn.gamer.com.tw/?yy=20'+str(year)+'&mm='+str(month)
        headers = {'User-Agent': random.choice(user_agent_list)}
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        tart=soup.find_all("div", {"class": "GN-lbox2B"})
        for i in tart:
            text=str(i)
            if target in text:
                dir=i.find('a')
                if not 'https:' in dir:
                    myLink = 'https:'+dir.get('href')
                    response = requests.get(url=myLink, headers=headers)
                    soup = BeautifulSoup(response.text, 'lxml')
                    pArticle = soup.find("div", {"class": "BH-lbox GN-lbox3 gnn-detail-cont"})
                    h1 = pArticle.find('h1').text.strip()
                    fi = open(file, 'r',encoding='utf8')
                    rec = fi.read()
                    fi = open(file, 'w',encoding='utf8')
                    fi.write(rec+h1+'\n'+myLink+'\n\n')
                    fi.close()
        tCurrent=time.time()
        tLapsed=round(tCurrent-tStart)
        m, s = divmod(tLapsed, 60)
        h, m = divmod(m, 60)
        h=formatTime(h)
        m=formatTime(m)
        s=formatTime(s)
        print('Time Lapsed: '+h+':'+m+':'+s+', Loops: '+str(idx)+'(20'+str(year)+'/'+str(month)+')', end="\r")
        delay_choices = [8, 5, 10, 6, 11, 9, 3,1,2,7]  # 延遲的秒數
        delay = random.choice(delay_choices)  # 隨機選取秒數
        time.sleep(delay)
        idx+=1

import requests
from bs4 import BeautifulSoup
import datetime
from pathlib import Path
from urllib.parse import quote
from autoPost import post, initial
import string
import os
import time
import pyperclip
import random
import webbrowser
import re
import json
import numpy as np
##Time Set
(hs,ms,ss)=(17,0,0)

def txt(list):
    try:
        text=''
        for item in list:
            text=text+item+'\n'
        pyperclip.copy(text)
        print('Text Copied')
    except TypeError:
        text=''
        for i in list:
            text=text+str(i)+'\n'
        pyperclip.copy(text)
        print('Text Copied')

kt='\'\\x16\''
def show(key):
    if format( key) == kt:
        # Stop listener
        return False

def formatTime(time):
    if time<10:
        return '0'+str(time)
    else:
        return str(time)

t = time.localtime()
year=int(time.strftime('%y',t))
month=int(time.strftime('%m',t))

result = time.strftime("%Y/%m/%d %H:%M:%S", t)
print("Start Time: "+result)
animation = "|/—\\"
ix = 0

target = '神魔之塔'
local_d = datetime.datetime.today()
d_format = local_d.strftime('%Y%m%d')
cd = os.getcwd()
user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)", "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"]

##test 場外測試
test=False
# test=True

##result 發布文章
result=False
result=True

##timer 設定發文時間
timer=False
timer=True

##LinkSet 指定連結
LinkSet=False
# LinkSet=True

review=''
print("心得: \n"+review)
    

initial(test)

while True:
    hour=int(time.strftime('%H',t))
    min=int(time.strftime('%M',t))
    sec=int(time.strftime('%S',t))
    if timer:
        while hour!=hs or min!=ms or sec<=ss:
            if hour>hs:
                ds=(hs-hour+24)*60*60+(ms-min)*60+(ss-sec)
            else:
                ds=(hs-hour)*60*60+(ms-min)*60+(ss-sec)
            print(' '+animation[round(ix*0.25) % len(animation)]+'T-'+str(ds)+'s         ',end='\r')
            ix+=1
            time.sleep(0.001)
            t = time.localtime()
            hour=int(time.strftime('%H',t))
            min=int(time.strftime('%M',t))
            sec=int(time.strftime('%S',t))
    ts = time.time()
    time.sleep(1)
    url='https://gnn.gamer.com.tw/index.php?k=4'

    # if test:
    #     url = f'https://gnn.gamer.com.tw/index.php?yy=20{year}&mm={month}&k=4'
    headers = {'User-Agent': random.choice(user_agent_list)}
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    # break
    tart = soup.find_all("h1", {"class": "GN-lbox2D"})[0:5]
    for i in tart:
        text = i.text.strip()
        # print(text)
        if target in text or test:
            dir = i.find('a')
            if not 'https:' in dir:
                myLink = 'https:' + dir.get('href')
            if LinkSet:
                myLink = 'https://gnn.gamer.com.tw/detail.php?sn=247111'
            response = requests.get(url=myLink, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            pArticle = soup.find("div", {"class": "BH-lbox GN-lbox3 gnn-detail-cont"})
            h1 = pArticle.find('h1').text.strip()
            break
                
    print(' '+animation[round(ix*1) % len(animation)]+'Waiting...', end="\r")
    ix += 1
    
    try:
        print('\n')
        # target = '神魔之塔'
        if target in h1:
            newResponse = requests.get(url = myLink, headers = headers)
            newSoup = BeautifulSoup(newResponse.text, 'lxml')
            idDiv = newSoup.find("div", {"id": "BH-master"})
            id = str(int(re.search(r'\d+', myLink).group()))
            author = newSoup.find("span", {"class": "GN-lbox3C"}).text.strip()
            author = author[author.index('）')+2:]
            month = int(author[author.index('-')+1:author.index('-')+3])
            day = (author[author.index('-')+4:author.index('-')+6])
            latest = cd + '\\DL.json'
            if not Path(latest).is_file():
                fi = open(latest, 'w')
                data = { "gnn": "",  "announcement": ""}
                json.dump(data, fi)
                fi.write(id+'\n'+rec)
                fi.close()
            with open(latest, 'r') as fi:
                data = json.load(fi)
                rec = data['gnn']
                fi.close()
            if test or id > rec:
                
                print("New GNN Found")
                pTitle = newSoup.find("div", {"class": "BH-lbox GN-lbox3 gnn-detail-cont"})
                title = pTitle.find('h1').text.strip()
                pArticle = newSoup.find("div", {"class": "GN-lbox3B"})
                figAll = newSoup.find("div", {"class": "GN-lbox3B"})
                ptable = pArticle.find('div')

                allParts = pArticle.find_all()

                allitems = []
                allwords = []
                h2List = []
                h3List = []
                imgList = []
                bgcolor1 = '#eff7f6'
                bgcolor2 = '#f6fff8'
                space = '[div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]'
                ca = 1
                allitems = [str(ele).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\n', u'') for ele in allParts]
                while all(x in allitems[0] for x in allitems[1:10]):
                    del allitems[0]
                    del allParts[0]

                for item in allParts:
                    if len(str(item))<15:
                        if '<h3' not in str(item) and '<h2' not in str(item):
                            continue
                    if '<tbody' in str(item)[0:8]:
                        continue
                    if '<td' in str(item)[0:5]:
                        continue
                    if '<tr' in str(item)[0:5]:
                        continue
                    if '<ul' in str(item)[0:5]:
                        continue
                    if '<li' in str(item)[0:5]:
                        continue
                    if 'group>' in str(item)[0:12]:
                        continue
                    if '<col' in str(item)[0:5]:
                        continue
                    if '<span' in str(item)[0:5]:
                        continue
                    if '<p' in str(item)[0:5]:
                        continue
                    if item.text.strip() == '' and not 'img' in str(item):
                        continue
                    if 'gamecard' in str(item):
                        continue
                    if '<a' in str(item)[0:3] and not 'img' in str(item):
                        continue
                    if '<table' in str(item) and '<div' in str(item)[0:5]:
                        continue
                    if len(item.find_all('div'))>1 and not 'td' in str(item):
                        continue
                    words = item.text.strip()
                    if '　　' in str(item):
                        allwords += [(space + '[div align=left]\u3000\u3000' + words + '[/div]' + space)]
                        continue
                    if '<h2' in str(item)[0:3] and '<div' not in str(item)[0:5]:
                        h2List += [(words)]
                        allwords += [(space + '\n[div align=left][size=5][b][color=#145292]' + words + '[/color][/b][/size][/div][hr]')]
                        continue
                    if '<h3' in str(item)[0:3] and '<div' not in str(item)[0:5]:
                        h3List += [(words)]
                        allwords += [(space + '\n[div align=left][size=4][b][color=#145292]- ' + words + ' -[/color][/b][/size][/div]' + space)]
                        continue
                    if '<img' in str(item):
                        try:
                            if 'gnnPIC' in str(item):
                                image = re.search(r'<img.*name="gnnPIC".*?/>', str(item)).group()
                                link = re.search(r'.*data-src="(.*?)"', image).group(1)
                                # pPhoto = item['data-src']
                                s = quote(link, safe=string.printable)
                                if not s in imgList:
                                    tn = '[div align=center width=100%][img='+s+' width=999][/div]'
                                    allwords += [(tn)]
                                    imgList += [(s)]
                                continue
                        except TypeError:
                            continue
                    if 'pic-desc' in str(item) and '<div' not in str(item)[0:5]:
                        if not '<li' in str(item):
                            allwords += [('[div align=center][size=2][color=#343a40]'+words+'[/color][/size][/div]' + space)]
                            continue
                        if '<li' in str(item):
                            continue
                    # if ('<div' in str(item) or '<center' in str(item)) and '<table' in str(item):
                    #     tb = item.find('td')
                    #     if len(tb.find_all('div'))==0 or len(item.find_all('table'))==0:
                    #         continue
                    if '<table' in str(item) and '<div' not in str(item)[0:5] and '<center' not in str(item)[0:8]:
                        # allwords += ['table']
                        tbody = item.find('tbody')
                        rows = tbody.find_all('tr')
                        at = '[div][table width=100% cellspacing=1 cellpadding=1 border=1]'
                        for row in rows:
                            c = 1
                            at += '[tr]'
                            cols = row.find_all('td')
                            for col in cols:
                                if 'colspan=' in str(col):
                                    x = str(col).index('colspan=')
                                    tar = str(col)[x+8:x+12]
                                    cspan = re.findall(r'\d+', str(col)[x+8:x+12])[0]
                                    if 'text-align: center;' in str(col):
                                        at += '[td colspan=' + cspan + ' bgcolor=' + (bgcolor1 if ca%2==0 else bgcolor2) + '][div align=center][size=3]' + col.text.strip() + '[/size][/div][/td]'
                                    else:
                                        at += '[td colspan=' + cspan + ' bgcolor=' + (bgcolor1 if ca%2==0 else bgcolor2) + '][size=3]' + col.text.strip() + '[/size][/td]'
                                    c+=int(cspan)-1
                                if 'rowspan=' in str(col):
                                    x = str(col).index('rowspan=')
                                    tar = str(col)[x + 8 : x + 12]
                                    rspan = re.findall(r'\d+', str(col)[x + 8 : x + 12])[0]
                                    if 'text-align: center;' in str(col):
                                        at += '[td rowspan=' + rspan + ' bgcolor=' + (bgcolor1 if ca%2==0 else bgcolor2) + '][div align=center][size=3]' + col.text.strip() + '[/size][/div][/td]'
                                    else:
                                        at += '[td rowspan=' + rspan + ' bgcolor=' + (bgcolor1 if ca%2==0 else bgcolor2) + '][size=3]' + col.text.strip() + '[/size][/td]'
                                else:
                                    if c<=len(cols):
                                        if 'text-align: center;' in str(col):
                                            at += '[td bgcolor=' + (bgcolor1 if ca%2==0 else bgcolor2) + '][div align=center][size=3]' + col.text.strip() + '[/div][/size][/td]'
                                        else:
                                            at += '[td bgcolor=' + (bgcolor1 if ca%2==0 else bgcolor2) + '][size=3]' + col.text.strip() + '[/size][/td]'
                                at = at.replace('\n\n', '\n').replace('\n\n\n', '\n').replace('\n\n\n\n', '\n')
                                c += 1
                            at += '[/tr]'
                        at += '[/table][/div][div]'
                        ca += 1
                        allwords += [(space + at + space)]
                        continue
                        
                    if 'quote-box' in str(item) and '<div' in str(item):
                        words = '[div][table width=100% cellspacing=1 cellpadding=1 border=1][tr][td]' + words + '[/td][/tr][/table][div]'
                        allwords += [(space + words + space)]
                        continue
                        
                    if words != '':
                        if '</li>' in str(item):
                            if not '</ul>' in str(item):
                                words = '[li]' + words + '[/li]' 
                                allwords += [(space + '[div align=left]' + words + '[/div]' + space)]
                            else:
                                words = ''
                            continue
                        if str(item).find('span style="color:') != -1:
                            if str(item).find('style="font-size:') != -1:
                                if str(item).find('</div>') != -1:
                                    words = '[size=2][b][color=#4d4d4d]' + words + '[/b][/color][/size]'
                                    allwords += [(space + '[div align=left]' + words + '[/div]' + space)]
                                    continue
                            if str(item).find('</div>') == -1:
                                words = ''
                                item = ''
                                continue
                
                text = '[div align=left][size=1][color=#343a40]發布時間: ' + author + '[/color][/size][/div][hr]'
                if test:
                    text = '[div align=left][b]測試[b][/div]\n[div align=left][size=1][color=#343a40]發布時間: ' + author + '[/color][/size][/div][hr]'
                for i in np.arange(len(allwords)):
                    text += allwords[i]
                text += '[div][/div]\n[div align=left]' + '[hr][url='
                text +=  myLink
                text += ']來源[/url][/div]\n[div align=left]標題整理:\n'
                for h2 in h2List:
                    text += '[color=#145292]● ' + h2 + '[/color]\n'
                text += '[/div][div align=left]' + review + '[/div]'

                tf = time.time()
                dt = round(tf - ts, 4)
                print(str(dt) + 's')
                if result:
                    article = text
                    post(test, title, article)
                    webbrowser.open(myLink,1)

                if not test:
                    with open(latest, 'w') as fi:
                        data['gnn'] = id
                        json.dump(data, fi)
                        fi.close()
                break
        time.sleep(0.5)
    except NameError:
        pass

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
# year=int(time.strftime('%y',t))
# month=int(time.strftime('%m',t))

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
test=True

##result 發布文章
result=False
result=True

##timer 設定發文時間
timer=False
# timer=True

##LinkSet 指定連結
LinkSet=False
LinkSet=True

##reviewInput 心得
reviewInput=False
# reviewInput=True

review=''
# review='施工中...\n格式可能會亂掉\n'
if reviewInput:
    review=review+input("心得: ")
print("心得: "+review)

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
    
    

    url='https://gnn.gamer.com.tw/index.php?k=4'

    # url='https://gnn.gamer.com.tw/?yy=20'+year+'&mm='+month
    if test:
        # url = 'https://gnn.gamer.com.tw/index.php?yy=2023&mm=2&k=4'
        url='https://gnn.gamer.com.tw/index.php?k=4'

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
                if LinkSet:
                    myLink='https://gnn.gamer.com.tw/detail.php?sn=246391/'
                response = requests.get(url=myLink, headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                pArticle = soup.find("div", {"class": "BH-lbox GN-lbox3 gnn-detail-cont"})
                h1 = pArticle.find('h1').text.strip()
    print(' '+animation[round(ix*1) % len(animation)]+'Waiting...', end="\r")
    ix+=1
    try:
        # break
        if target in h1:
            ts = time.time()
            newResponse = requests.get(url = myLink, headers = headers)
            newSoup = BeautifulSoup(newResponse.text, 'lxml')
            idDiv = newSoup.find("div", {"id": "BH-master"})
            id = str(int(re.search(r'\d+', myLink).group()))
            author = newSoup.find("span", {"class": "GN-lbox3C"}).text.strip()
            author = author[author.index('）')+2:]
            month = int(author[author.index('-')+1:author.index('-')+3])
            day = (author[author.index('-')+4:author.index('-')+6])
            latest = cd + '\\DL.txt'
            if not Path(latest).is_file():
                fi = open(latest, 'w')
                fi.close()
            fi = open(latest, 'r')
            rec = fi.read()
            if test:
                rec = ''
            if id in rec:
                fi.close()
                pass
            else:
                
                nod=[]
                print("New GNN Found")
                pTitle = newSoup.find("div", {"class": "BH-lbox GN-lbox3 gnn-detail-cont"})
                title = pTitle.find('h1').text.strip()
                pArticle = newSoup.find("div", {"class": "GN-lbox3B"})
                figAll = newSoup.find("div", {"class": "GN-lbox3B"})
                ptable = pArticle
                allParts = pArticle.find_all()
                alldivs = []
                allitems = []
                allwords = []
                h2List = []
                h3List = []
                imgList = []
                bgcolor1='#eff7f6'
                bgcolor2='#f6fff8'
                ca=1
                for i in allParts:
                    allitems.append(str(i).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\n', u''))
                while all(x in allitems[0] for x in allitems[1:10]):
                    del allitems[0]
                    del allParts[0]
                    pArticle = pArticle.find('div')

                for item in allParts:
                    
                    words = item.text.strip()
                    if '　　' in str(item):
                        index = allParts.index(item)
                        words = '\u3000\u3000' + words
                        if index > 2:
                            if '　　' in str(allParts[index - 2]):
                                words =  '\n' + words
                    if 'h2' in str(item):
                        h2List.append(words)
                        allwords.append('[div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]\n[div align=left][size=5][b][color=#145292]' + words + '[/color][/b][/size][/div][hr]')
                        words = ''
                    if 'h3' in str(item):
                        h3List.append(words)
                        allwords.append('[div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]\n[div align=left][size=4][b][color=#145292]' + words + '[/color][/b][/size][/div]')
                        words = ''
                    if 'img' in str(item):
                        try:
                            ele = item.find('img')
                            pPhoto = ele['data-src']
                            s = quote(pPhoto, safe=string.printable)
                            if not s in imgList:
                                tn = '[div align=center width=100%][img='+s+'][/div]\n'
                                allwords.append(tn)
                                imgList.append(s)
                                words = ''
                        except TypeError:
                            pPhoto=''
                            tn=''
                            pass
                    if 'pic-desc' in str(item):
                        if not '<li' in str(item):
                            allwords.append('[div align=center][size=2][color=#343a40]'+words+'[/color][/size][/div][div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]')
                            words = ''
                        if '<li' in str(item):
                            words = ''
                    
                    if ('div' in str(item) or 'center' in str(item)) and 'table' in str(item):
                        item = ''
                        words = ''
                    if 'table' in str(item):
                        tbody = item.find('tbody')
                        rows = tbody.find_all('tr')
                        at = '[div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div][div][table width=100% cellspacing=1 cellpadding=1 border=1]'
                        for row in rows:
                            c = 1
                            at = at + '[tr]'
                            cols = row.find_all('td')
                            for col in cols:
                                if 'colspan=' in str(col):
                                    x=str(col).index('colspan=')
                                    tar=str(col)[x+8:x+12]
                                    cspan=re.findall(r'\d+', str(col)[x+8:x+12])[0]
                                    if 'text-align: center;' in str(col):
                                        at=at+'[td colspan='+cspan+' bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][div align=center][size=3]'+col.text.strip()+'[/size][/div][/td]'
                                    else:
                                        at=at+'[td colspan='+cspan+' bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][size=3]'+col.text.strip()+'[/size][/td]'
                                    c+=int(cspan)-1
                                if 'rowspan=' in str(col):
                                    x=str(col).index('rowspan=')
                                    tar=str(col)[x+8:x+12]
                                    rspan=re.findall(r'\d+', str(col)[x+8:x+12])[0]
                                    if 'text-align: center;' in str(col):
                                        at=at+'[td rowspan='+rspan+' bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][div align=center][size=3]'+col.text.strip()+'[/size][/div][/td]'
                                    else:
                                        at=at+'[td rowspan='+rspan+' bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][size=3]'+col.text.strip()+'[/size][/td]'
                                else:
                                    if c<=len(cols):
                                        if 'text-align: center;' in str(col):
                                            at=at+'[td bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][div align=center][size=3]'+col.text.strip()+'[/div][/size][/td]'
                                        else:
                                            at=at+'[td bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][size=3]'+col.text.strip()+'[/size][/td]'
                                at = at.replace('\n\n', '\n').replace('\n\n\n', '\n').replace('\n\n\n\n', '\n')
                                c+=1
                            at = at+'[/tr]'
                        at = at+'[/table][/div][div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]'
                        ca+=1
                        allwords.append(at)
                    


                    if not words == '' and str(item).find('gamecard') == -1 and str(item).find('span') == -1 :
                        if str(item).find('acglink')!=-1 and str(item).find('<div')==-1:
                            words = ''
                        allwords.append('[div align=left]' + words + '[/div]')
                    alldivs.append(str(item))


                # break
                
                res = [ele for ele in allwords if ele != '']
                text = '[div align=left][size=1][color=#343a40]發布時間: ' + author + '[/color][/size][/div][hr]'
                for i in range(len(res)):
                    text = text + res[i]
                text = text + '[div][/div]\n[div align=left]' + '[hr][url='
                text = text + myLink
                text = text + '/]來源[/url] [/div]\n[div align=left]標題整理:\n'
                for h2 in h2List:
                    text = text + '[li][color=#145292]' + h2 + '[/color][/li]'
                text = text + '[/div][div align=left]' + review + '[/div]'


                if result:
                    article = text
                    post(test, title, article)

                    tf=time.time()
                    dt=round(tf-ts,2)
                    print('Totoal Time: '+str(dt)+'s')
                    webbrowser.open(myLink,1)

                if not test:
                    fi = open(latest, 'w')
                    fi.write(id+'\n'+rec)
                    fi.close()
                break
        delay_choices = [0.5, 0.2, 0.4]  # 延遲的秒數
        delay = random.choice(delay_choices)  # 隨機選取秒數
        time.sleep(delay)
    except NameError:
        pass
##先將發布文章放在左螢幕的右半邊
import requests
from bs4 import BeautifulSoup
import datetime
from pathlib import Path
from urllib.parse import quote
import string
import os
import time
import pyperclip
import random
import webbrowser
import numpy as np
from autoPost import post, initial
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

space = '[div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]'
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
            ts=time.time()
            newResponse = requests.get(url=myLink, headers=headers)
            newSoup = BeautifulSoup(newResponse.text, 'lxml')
            idDiv=newSoup.find("div", {"id": "BH-master"})
            id = str(int(re.search(r'\d+', myLink).group()))
            author=newSoup.find("span", {"class": "GN-lbox3C"}).text.strip()
            author=author[author.index('）')+2:]
            month = int(author[author.index('-')+1:author.index('-')+3])
            day = (author[author.index('-')+4:author.index('-')+6])
            latest = cd+'\\DL.txt'
            if not Path(latest).is_file():
                fi = open(latest, 'w')
                fi.close()
            fi = open(latest, 'r')
            rec = fi.read()
            if test:
                rec=''
            if id in rec:
                fi.close()
                pass
            else:
                
                nod=[]
                print("New GNN Found")
                pTitle = newSoup.find("div", {"class": "BH-lbox GN-lbox3 gnn-detail-cont"})
                title = pTitle.find('h1').text.strip()
                pArticle=newSoup.find("div", {"class": "GN-lbox3B"})
                figAll=newSoup.find("div", {"class": "GN-lbox3B"})
                ptable=pArticle
                allParts=pArticle.find_all()
                alldivs=[]
                allwords=[]
                for i in allParts:
                    alldivs.append(str(i).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\n', u''))
                # txt(alldivs)
                
                while all(x in alldivs[0] for x in alldivs[1:10] ):
                    del alldivs[0]
                    del allParts[0]
                    pArticle=pArticle.find('div')
                for i in allParts:
                    if str(i).find('td')==-1 and str(i).find('gamecard')==-1:
                        tx=i.text.strip()
                        allwords.append(tx)
                    else:
                        allwords.append('')
                # txt(allwords)

                ytList=[]
                ytVideos=pArticle.find_all('iframe')
                for v in ytVideos:
                    ytLink=v['data-src']
                    ix=allParts.index(v)
                    alldivs[ix]='[div][movie='+ytLink+' width=640 height=360][/div]'
                    ytList.append(ytLink)


                
                article=[]
                wordArt=[]
                wordList=[]
                divWords=pArticle.find_all('div')
                for item in divWords:
                    if not item.find('table') and not item.find('figure') and not item.find('h2') and not item.find('h3'):
                        # if not item.find('figure'):
                            tstring=str(item)
                            word=item.text.strip()
                            st=item.text.strip()
                            if '　　' in tstring:
                                word='\u3000\u3000'+word
                            if tstring.find('<span style="font-size:16px;">')==-1:
                                if word!='':
                                    if tstring.find('<span class="slider-count-span">')==-1 and not word in nod:
                                        if tstring.find('<span style="font-size:')!=-1:
                                            if tstring.find('13px;')!=-1 or tstring.find('12px;')!=-1:
                                                article.append('[div align=left][size=2][color=#343a40]'+word+'[/color][/size][/div]')
                                        else:
                                            article.append('[div align=left]'+word+'[/div]\n')
                                        wordList.append(st)
                                        wordArt.append(st)
                                        nod.append(word)
                # txt(divWords)
                for word in wordArt:
                    i=allwords.index(word)
                    alldivs[i]='words'
                
                h2s=pArticle.find_all('h2')
                h2List=[]
                for ele in h2s:
                    h2=ele.text.strip()
                    # .replace(u'\u3000', u' ').replace(u'\xa0', u' ')
                    # if not h2 in wordList:
                    i2=allParts.index(ele)
                    allParts[i2]='hash'
                    alldivs[i2]='h2'
                    h2List.append(h2)
                        # wordList.append(h2)
                
                h3s=pArticle.find_all('h3')
                h3List=[]
                for ele in h3s:
                    h3=ele.text.strip()
                    # .replace(u'\u3000', u' ').replace(u'\xa0', u' ')
                    # if not h3 in wordList:
                    i3=allParts.index(ele)
                    allParts[i3]='hash'
                    alldivs[i3]='h3'
                    h3List.append(h3)
                    # wordList.append(h3)
                # txt(alldivs)
                
                

                lis=figAll.find_all('img',{'name':'gnnPIC'})
                liList=[]
                for ele in lis:
                    try:
                        # fig = ele.find('img')
                        pPhoto = ele['data-src']
                        s = quote(pPhoto, safe=string.printable)
                        tn='[div align=center width=100%][img='+s+'][/div]'

                    except TypeError:
                        pPhoto=''
                        tn=''
                        pass
                    liList.append(tn)

                figd=figAll.find_all('figure',{'class':'pic-desc'})
                figdList=[]
                for ele in figd:
                    text=ele.text.strip()
                    i=len(allwords)-allwords[::-1].index(text)
                    alldivs[i-1]='[div align=center][size=2][color=#343a40]'+text+'[/color][/size][/div][div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]\n'
                    figdList.append(text)
                # txt(alldivs)
                # txt(figdList)
                



                tables=ptable.find_all('tbody')
                taList=[]
                bgcolor1='#eff7f6'
                bgcolor2='#f6fff8'
                ca=1
                # txt(tables)
                for a in np.arange(len(tables)):
                    at = '[div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div][div][table width=100% cellspacing=1 cellpadding=1 border=1]'
                    rows = tables[a].find_all('tr')
                    for row in rows:
                        c=1
                        at += '[tr]'
                        cols = row.find_all('td')
                        for col in cols:
                            if 'colspan=' in str(col):
                                x=str(col).index('colspan=')
                                tar=str(col)[x+8:x+12]
                                cspan=re.findall(r'\d+', str(col)[x+8:x+12])[0]
                                if 'text-align: center;' in str(col):
                                    at += '[td colspan='+cspan+' bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][div align=center][size=3]'+col.text.strip()+'[/size][/div][/td]'
                                else:
                                    at += '[td colspan='+cspan+' bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][size=3]'+col.text.strip()+'[/size][/td]'
                                c+=int(cspan)-1
                            if 'rowspan=' in str(col):
                                x=str(col).index('rowspan=')
                                tar=str(col)[x+8:x+12]
                                rspan=re.findall(r'\d+', str(col)[x+8:x+12])[0]
                                if 'text-align: center;' in str(col):
                                    at += '[td rowspan='+rspan+' bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][div align=center][size=3]'+col.text.strip()+'[/size][/div][/td]'
                                else:
                                    at += '[td rowspan='+rspan+' bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][size=3]'+col.text.strip()+'[/size][/td]'
                            else:
                                if c<=len(cols):
                                    if 'text-align: center;' in str(col):
                                        at += '[td bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][div align=center][size=3]'+col.text.strip()+'[/div][/size][/td]'
                                    else:
                                        at += '[td bgcolor='+(bgcolor1 if ca%2==0 else bgcolor2)+'][size=3]'+col.text.strip()+'[/size][/td]'
                            at = at.replace('\n\n', '\n').replace('\n\n\n', '\n').replace('\n\n\n\n', '\n')
                            c+=1
                        at += '[/tr]'
                    at += '[/table][/div][div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]'
                    taList.append(at)
                    ca+=1
                
                liIndex=[]
                ulIndex=[]
                idx=0
                for item in allParts:
                    num2=item.find('img')
                    if num2!=None:
                        if num2!=-1:
                            
                            ulIndex.append(idx)
                            # alldivs[idx]='empty2'
                            alldivs[idx+1]='figure'
                            if 'name="gnnPIC"' in str(num2) and not str(num2) in nod:
                                nod.append(str(num2))
                                
                            if not str(num2) in nod:
                                alldivs[idx+1]='out'

                            alldivs[idx]='out'
                        
                        
                    idx+=1

                
                taIndex=[]
                for ele in tables:
                    taIndex.append(allParts.index(ele))
                    alldivs[allParts.index(ele)]='table'
                # txt(alldivs)

                for i in np.arange(len(alldivs)):
                    if alldivs[i].find('<span style="font-size:16px;">')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<div class="gamecard__background">')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<div class="article_gamercard lazyload" data-fanspage-id="488" data-from="web_gnn">')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<div></div>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<div> </div>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<div>  </div>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<div style="clear:both;"> </div>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<col')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<p> </p>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<iframe')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('</td>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<br/>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<p>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<div><span style="font-size:16px;">')!=-1:
                        if alldivs[i].find('table')==-1:
                            alldivs[i]='out'
                    if alldivs[i].find('<span')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('</figure>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<script')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<div class="bh-grids-img-box"')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('</a>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<div>')!=-1:
                        alldivs[i]='out'
                    if alldivs[i].find('<p style="text-align: center;">')!=-1:
                        alldivs[i]='out'
                
                # txt(alldivs)
                
                numW=0
                numT=0
                numh2=0
                numh3=0
                numF=0
                for i in np.arange(len(alldivs)):
                    if alldivs[i]=='words':
                        alldivs[i]=article[numW]
                        numW+=1
                    if alldivs[i]=='table':
                        alldivs[i]=taList[numT]
                        numT+=1
                    if alldivs[i]=='h2':
                        alldivs[i]='\xa0\n[div align=left][size=5][b][color=#145292]'+h2List[numh2]+'[/b][/color][/size][/div][hr]'
                        numh2+=1
                    if alldivs[i]=='h3':
                        alldivs[i]='\xa0\n'+'[div align=left][size=4][b][color=#145292]- '+h3List[numh3]+' -[/b][/color][/size][/div]'
                        numh3+=1
                    if alldivs[i]=='figure':
                        try:
                            alldivs[i]=liList[numF]+'\n'
                            numF+=1
                        except IndexError:
                            alldivs[i]='out'
                
                for i in np.arange(len(alldivs)):
                    if alldivs[i]=='out':
                        alldivs[i]=''
                    if alldivs[i]=='empty':
                        alldivs[i]=''
                    if alldivs[i]=='empty2':
                        alldivs[i]=''
                    if alldivs[i]=='empty3':
                        alldivs[i]=''
                    if alldivs[i]=='empty4':
                        alldivs[i]=''
                    alldivs[i]=alldivs[i].replace('<p style="font-size: 12px; padding: 10px 0;">','[div align=left][size=2][color=#343a40]').replace('</p>','[/color][/size][/div]\n').replace('&gt;', '>').replace('<li>', '[div align=left]．').replace('<li>', '[/div]').replace('<p style="margin-bottom: 0cm">','').replace('<p class="pic-desc">', '')
                
                res = [ele for ele in alldivs if ele != '']
                text = '[div align=left][size=1][color=#343a40]發布時間: '+author+'[/color][/size][/div][hr]'
                for i in np.arange(len(res)):
                    text += res[i]
                text += '[div][/div]\n[div align=left]'+'[hr][url='
                text += myLink
                text += '/]來源[/url] [/div]\n[div align=left]標題整理:\n'
                for h2 in h2List:
                    text += '[li][color=#145292]'+h2+'[/color][/li]'
                text += '[/div][div align=left]'+review+'[/div]'
                # text = text+'\n[div align=left]Totoal Time: '+str(dt)+'(+1.7) s[/div]'

                if result:
                    article = text
                    tf = time.time()
                    dt = round(tf - ts, 2)
                    print('Total Time: ' + str(dt) + 's')
                    post(test, title, article)
                    
                
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
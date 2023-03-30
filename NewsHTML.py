import requests
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
from urllib.parse import quote
import string
import os
import time
import webbrowser
import pyperclip
import random
import pyimgur
from tqdm import tqdm
from autoPost import post, initial
import json
import re

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

def formatTime(time):
    if time<10:
        return '0'+str(time)
    else:
        return str(time)

kt='\'\\x16\''
def show(key):
  
    # print('\nYou Entered {0}'.format( key))
    # print(format( key))
    if format( key) == kt:
        # Stop listener
        return False

tStart=time.time()
t = time.localtime()

result = time.strftime("%Y/%m/%d %H:%M:%S", t)
print("Start Time: "+result)

##imgur
CLIENT_ID = "886c33830062f60"
idx = 0

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
target = '慶祝活動'
cd = os.getcwd()
user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)","Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
                   ]

##test 場外測試
test=False
test=True

##result 發布文章
result=False
result=True

##LinkSet 指定連結
LinkSet=False
LinkSet=True

##reviewInput 心得
reviewInput=False
# reviewInput=True

##Alarm 發布確認
Alarm=False
# Alarm=True

review=''
# review='施工中...\n格式可能會亂掉'
if reviewInput:
    review=input("心得:")
print("心得:" + review)

initial(test)

while True:
    
    url = 'https://towerofsaviors.com/category/%e5%85%ac%e5%91%8a/'
    
    headers = {'User-Agent': random.choice(user_agent_list)}
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    pArticle = soup.find_all('article')
    for i in range(10):
        h2 = pArticle[i].find('h2').text.strip()
        if target in h2:
            pA = pArticle[i].find('a')
            tPost=pArticle[i].find('time').get('datetime')
            try:
                timePost=tPost[tPost.index('T')+1:tPost.index('+')]
            except IndexError:
                timePost=tPost
            break
        
    if target in h2:
        try:
            myLink = pA.get('href')
            if LinkSet:
                myLink = 'https://towerofsaviors.com/2023/03/24/%e3%80%90%e9%87%91%e5%ad%97%e5%a1%94%e7%9a%84%e5%95%9f%e5%8b%95%e2%80%a7-%e5%a7%8b%e7%a5%96%e5%85%83%e7%b4%a0%e7%9a%84%e5%8a%9b%e9%87%8f%e7%88%86%e7%99%bc%e3%80%91%e6%85%b6%e7%a5%9d%e6%b4%bb%e5%8b%95/'

            newResponse = requests.get(url=myLink)
            newSoup = BeautifulSoup(newResponse.text, 'lxml')
            pArticle = newSoup.find('article')
            id = re.findall(r'\d+', str(pArticle.get('id')))[0]
            folder = cd+'\\'+id
            latest = cd + '\\DL.json'
            if not Path(latest).is_file():
                fi = open(latest, 'w')
                data = { "gnn": "",  "announcement": ""}
                json.dump(data, fi)
                fi.write(id+'\n'+rec)
                fi.close()
            with open(latest, 'r') as fi:
                data = json.load(fi)
                rec = data['announcement']
                fi.close()
            if test or int(id) > int(rec):
                ts = time.time()
                list = []
                print("New Announcement Found")
                Path(folder).mkdir(parents=True, exist_ok=True)

                # pThumbnail = pArticle.find_all('img')
                # img = []
                # uploaded_image = []
                # for item in tqdm(range(len(pThumbnail))):
                #     pPhoto = pThumbnail[item]['src']
                #     if not pPhoto in img:
                #         img.append(pPhoto)
                #         s = quote(pPhoto, safe=string.printable)
                #         urllib.request.urlretrieve(s, folder + f"\\cover{item}.jpg")
                #         PATH = folder + f"\\cover{item}.jpg"
                #         im = pyimgur.Imgur(CLIENT_ID)
                #         uploaded_image = im.upload_image(PATH, title=id)
                #         if item == 0:
                #             tn='[div][img='+uploaded_image.link+' thumbnail=yes width=999][/div]'
                #         else:
                #             tn='[div][img='+uploaded_image.link+'  width=999][/div]'
                #         list.append(tn)
                
                titleList = []
                pContent = pArticle.find('figure', {"class": "wp-block-table"})
                pNews = pContent.find('tbody')
                timeP = pContent.find_all('figcaption')
                # txt(pNews)
                # break
                if len(timeP) > 0:
                    text = timeP[0].text.strip()
                    timePost = text[text.index('：')+1:]
                td = pNews.find_all('td')
                titles = pNews.find_all('mark')
                for title in titles:
                    text = title.text.strip()
                    if text != '':
                        titleList += ['[b][color=#790000]' + text+ '[/color][/b]']

                linkList = []
                textList = []
                link = pNews.find_all('a')
                for links in link:
                    ax = links['href']
                    linkList.append(ax)
                    textList.append(links.text.strip())
                uIndex=0
                for part in pNews:
                    af = str(part)
                    af = re.sub('<br/>', '\n', af)
                    af = re.sub('<tr>', '[hr]', af)
                    af = re.sub('</tr>', '', af)
                    af = re.sub('<td>', '[div]', af)
                    af = re.sub('</td>', '[/div]', af)
                    af = re.sub('<mark.*?>', '[color=#790000]', af)
                    af = re.sub('</mark>', '[/color]', af)
                    af = re.sub('<strong.*?>', '[b]', af)
                    af = re.sub('</strong>', '[/b]', af)
                    af = re.sub('<s>', '[s]', af)
                    af = re.sub('</s>', '[/s]', af)
                    while '</a>' in af:
                        alltext = re.search(r'<a .*?href=".*?".*?>.*?</a>', af).group()
                        link = re.search(r'<a .*?href="(.*?)".*?>.*?</a>', af).group(1)
                        text = re.search(r'<a .*?>(.*?)</a>', af).group(1)
                        af = re.sub(alltext, '[url=' + link + ']' + text + '[/url]', af)
                    list.append(af)
                text = ''
                for i in range(len(list)):
                    text = text + list[i]
                text += '[hr][div]' + '[url=' + myLink + '/]來源[/url] [/div]'
                text += '[div]更新時間: '+timePost+'[/div]'
                text += '[div]'+review+'[/div]'
                text += '懶人包:\n'
                for x in titleList:
                    if '★' in x:
                        text += x + '\n'
                if result:
                    article = text
                    title = h2
                    if Alarm:
                        webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=0s',1)
                        os.startfile(folder+"\\cover.jpg")
                        input('Press Enter')
                    tf = time.time()
                    dt = round(tf - ts, 4)
                    print('Total Time: '+str(dt)+'s')
                    post(test, title, article)

                if not test:
                    with open(latest, 'w') as fi:
                        data['announcement'] = id
                        json.dump(data, fi)
                        fi.close()
                break
            tCurrent=time.time()
            tLapsed=round(tCurrent-tStart)
            m, s = divmod(tLapsed, 60)
            h, m = divmod(m, 60)
            h=formatTime(h)
            m=formatTime(m)
            s=formatTime(s)
            print('Time Lapsed: '+h+':'+m+':'+s+', Loops: '+str(idx), end="\r")
            delay_choices = [8, 5, 10, 6, 11, 9, 13, 15, 12, 7]  # 延遲的秒數
            delay = random.choice(delay_choices)  # 隨機選取秒數
            time.sleep(delay)
            idx += 1
        except NameError:
            pass

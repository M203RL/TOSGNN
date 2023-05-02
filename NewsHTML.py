##GNN發布後執行
import requests
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
from urllib.parse import quote
import string
import os
import time
import pyperclip
import random
import pyimgur
from tqdm import tqdm
from autoPost import post, initial
import json
import re
from NewsUpdate import update
import pathlib
from fake_useragent import UserAgent
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pkg_resources
from subprocess import call

packages = [dist.project_name for dist in pkg_resources.working_set]
call("pip install --upgrade " + ' '.join(packages), shell=True)

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
    if int(time)<10:
        return '0'+str(int(time))
    else:
        return str(int(time))
    
    
tStart=time.time()
t = time.localtime()
year=str(time.strftime('%Y',t))
month=str(time.strftime('%m',t))
day=str(time.strftime('%d',t))

result = time.strftime("%Y/%m/%d %H:%M:%S", t)
print("Start Time: "+result)

##imgur
CLIENT_ID = "886c33830062f60"
idx = 1

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
target = '慶祝活動'
cd = str(pathlib.Path(__file__).parent.resolve())
user_agent = UserAgent()


##test 場外測試
test=False
test=True

##autoUpdate 監視官網更新
autoUpdate=False
# autoUpdate=True

##result 發布文章
result=False
result=True

##LinkSet 指定連結
LinkSet=False
# LinkSet=True

##autoReply 發文後自動回覆文章
autoReply=False
# autoReply=True

##reviewInput 心得
reviewInput=False
# reviewInput=True


testLink = 'https://towerofsaviors.com/2023/03/31/%e3%80%90%e6%8e%83%e8%95%a9%e9%99%b0%e9%9c%be%e7%9a%84%e9%bb%84%e6%98%8f%e4%b9%8b%e8%8a%92-%e2%80%a7-%e5%9f%8b%e8%91%ac%e5%8d%83%e5%b9%b4%e7%9a%84%e6%9c%a8%e4%b9%83%e4%bc%8a%e3%80%91%e6%85%b6%e7%a5%9d/'

review=''
# review='施工中...\n格式可能會亂掉'
if reviewInput:
    review=input("心得:")
print("心得:" + review)

driver = initial(test)

userList = []
while True:
    url = 'https://towerofsaviors.com/category/%e5%85%ac%e5%91%8a/'
    try:
        
        # response = requests.get(url=url, headers=headers, timeout=5, verify=False)
        response = requests.get(url=url, headers={ 'user-agent': user_agent.random }, verify=False)
    
        soup = BeautifulSoup(response.text, 'lxml')
        pArticle = soup.find_all('article')
        for i in range(5):
            h2 = pArticle[i].find('h2').text.strip()
            if target in h2:
                pA = pArticle[i].find('a')
                tPost = pArticle[i].find('time').get('datetime')
                tyear = formatTime(re.search(r'(.*?)-(.*?)-(.*?)T(.*?):(.+?)', tPost).group(1))
                tmonth = formatTime(re.search(r'(.*?)-(.*?)-(.*?)T(.*?):(.+?)', tPost).group(2))
                tday = formatTime(re.search(r'(.*?)-(.*?)-(.*?)T(.*?):(.+?)', tPost).group(3))
                thour = formatTime(re.search(r'(.*?)-(.*?)-(.*?)T(.*?):(.+?)', tPost).group(4))
                tminute = formatTime(re.search(r'(.*?)-(.*?)-(.*?)T(.*?):(.+?)', tPost).group(5))
                try:
                    timePost = f'{tyear}-{tmonth}-{tday} {thour}:{tminute}'
                except IndexError:
                    timePost = tPost
                break
            
        if target in h2:
            try:
                t = time.localtime()
                year=str(time.strftime('%Y',t))
                month=str(time.strftime('%m',t))
                day=str(time.strftime('%d',t))
                myLink = pA.get('href')
                if LinkSet:
                    myLink = testLink
                newResponse = requests.get(url=myLink)
                newSoup = BeautifulSoup(newResponse.text, 'lxml')
                pArticle = newSoup.find('article')
                id = re.findall(r'\d+', str(pArticle.get('id')))[0]
                folder = cd+'\\'+id
                latest = cd + '\\DL.json'
                if not Path(latest).is_file():
                    fi = open(latest, 'w')
                    data = { "gnn": "0",  "announcement": "0"}
                    json.dump(data, fi)
                with open(latest, 'r') as fi:
                    data = json.load(fi)
                    rec = data['announcement']
                    fi.close()
                if test or (int(id) > int(rec) and (year == tyear and month == tmonth and day == tday)):
                # if int(id) > int(rec):
                    ts = time.time()
                    list = []
                    print("New Announcement Found")
                    Path(folder).mkdir(parents=True, exist_ok=True)
                    if int(id) > int(rec):
                        with open(latest, 'w') as fi:
                            data['announcement'] = id
                            json.dump(data, fi)
                            fi.close()
                    
                    imgList = []
                    if not test:
                        pThumbnail = pArticle.find_all('img')
                        img = []
                        uploaded_image = []
                        for item in tqdm(range(len(pThumbnail))):
                            pPhoto = pThumbnail[item]['src']
                            if not pPhoto in img:
                                img.append(pPhoto)
                                s = quote(pPhoto, safe=string.printable)
                                urllib.request.urlretrieve(s, f"{folder}\\cover{item}.jpg")
                                PATH = f"{folder}\\cover{item}.jpg"
                                im = pyimgur.Imgur(CLIENT_ID)
                                uploaded_image = im.upload_image(PATH, title=id)
                                if item == 0:
                                    tn = f'[div][img={uploaded_image.link} thumbnail=yes width=999][/div]'
                                else:
                                    tn = f'[div][img={uploaded_image.link} width=999][/div]'
                                list.append(tn)
                                imgList.append(tn)
                    
                    titleList = []
                    pContent = pArticle.find('figure', {"class": "wp-block-table"})
                    pNews = pContent.find('tbody')
                    td = pNews.find_all('td')
                    titles = pNews.find_all('mark')
                    for title in titles:
                        text = title.text.strip()
                        if text != '':
                            titleList .append(f'[b][color=#790000]{text}[/color][/b]')

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
                            af = re.sub(alltext, f'[url={link}]{text}[/url]', af)
                        list.append(af)
                    text = ''
                    for i in range(len(list)):
                        text += list[i]
                    text += f'[hr][div][url={myLink}]來源[/url][/div]'
                    text += f'[div]更新時間: {timePost}[/div]'
                    text += f'[div]{review}[/div]'
                    text += '懶人包:\n'
                    for x in titleList:
                        if '★' in x:
                            text += x + '\n'
                    if result:
                        article = text
                        title = h2
                        tf = time.time()
                        dt = round(tf - ts, 4)
                        print('Total Time: '+str(dt)+'s')
                        newlink = post(driver, test, autoUpdate, autoReply, title, article)

                    break
                # if year != tyear or month != tmonth or day != tday and int(id) <= int(rec):
                #     break
                tCurrent = time.time()
                tLapsed = round(tCurrent - tStart)
                m, s = divmod(tLapsed, 60)
                h, m = divmod(m, 60)
                h = formatTime(h)
                m = formatTime(m)
                s = formatTime(s)
                avg = round(tLapsed/idx, 2)
                print(f'Time Lapsed: {h}:{m}:{s}, Loops: {idx}, Average: {avg} s/loop', end="\r")
                delay_choices = [8, 15, 10, 16, 11, 6, 13, 15, 12, 14]  # 延遲的秒數
                delay = random.choice(delay_choices)  # 隨機選取秒數
                time.sleep(delay)
                idx += 1
            except NameError:
                pass
    except requests.exceptions.ConnectionError:
        time.sleep(15)
        continue
    except IndexError:
        pass

if autoUpdate:
    time.sleep(10)
    trecord = (tyear, tmonth, tday, thour, tminute)
    update(test, trecord, myLink, newlink, title, article, review, imgList)

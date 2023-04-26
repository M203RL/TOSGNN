import time
import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import random
from tqdm import tqdm
from urllib.parse import quote
import string
import pyimgur
from autoPost import upt
import datetime

def formatTime(time):
    if int(time)<10:
        return '0'+str(int(time))
    else:
        return str(int(time))

cd = os.getcwd()
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
CLIENT_ID = "886c33830062f60"


def update(test, trecord, myLink, newlink, h2, review, imgList):
    (tyear, tmonth, tday, thour, tminute) = trecord
    rUpdate = f'{tyear}-{tmonth}-{tday} {thour}:{tminute}'
    while True:
        list = []
        headers = {'User-Agent': random.choice(user_agent_list)}
        try:
            Response = requests.get(url=myLink, headers=headers, timeout=5, verify=False)
            Soup = BeautifulSoup(Response.text, 'lxml')
            pArticle = Soup.find('article')
            id = re.findall(r'\d+', str(pArticle.get('id')))[0]
            folder = cd+'\\'+id
            if '最後更新時間' in str(pArticle):
                tUpdate = re.search(r'最後更新時間：([0-9][0-9][0-9][0-9])-([0-1][0-9])-([0-3][0-9]) ([0-2][0-9]):([0-5][0-9])', str(pArticle))
                uyear = formatTime(tUpdate.group(1))
                umonth = formatTime(tUpdate.group(2))
                uday = formatTime(tUpdate.group(3))
                uhour = formatTime(tUpdate.group(4))
                uminute = formatTime(tUpdate.group(5))
                if tyear != uyear or tmonth != umonth or tday != uday or thour != uhour or tminute != uminute:
                    tyear = uyear
                    tmonth = umonth
                    tday = uday
                    thour = uhour
                    tminute = uminute
                    rUpdate = f'{uyear}-{umonth}-{uday} {uhour}:{uminute}'
                    for img in imgList:
                        list.append(img)
                
                    titleList = []
                    pContent = pArticle.find('figure', {"class": "wp-block-table"})
                    pNews = pContent.find('tbody')
                    timeP = pContent.find_all('figcaption')
                    # txt(pNews)
                    # break
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
                    text += f'[hr][div][url={myLink}]來源[/url] [/div]'
                    text += f'[div]更新時間: {rUpdate}[/div]'
                    text += f'[div]{review}[/div]'
                    text += '懶人包:\n'
                    for x in titleList:
                        if '★' in x:
                            text += x + '\n'
                    article = text
                    title = h2
                    
                    upt(test, title, article, newlink)
                    day = datetime.datetime.today().weekday()
                    if day == 2:
                        break

        except requests.exceptions.ConnectionError:
            time.sleep(5)
            continue
        time.sleep(300)

if __name__ == '__main__':
    pass
import time
import requests
from bs4 import BeautifulSoup
import re
from autoPost import upt
import datetime
import pathlib
from fake_useragent import UserAgent
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import difflib

def formatTime(time):
    if int(time)<10:
        return '0'+str(int(time))
    else:
        return str(int(time))
    
def compare(before, after, rUpdate):
    result = ''
    diff = difflib.unified_diff(
    before, after, lineterm='', n=1000000)

    lines = list(diff)[2:]
    for line in lines:
        if line[0] != '@' and line[0] != '+' and line[0] != '-':
            result += f"{line[1:]}"
        if line[0] == '-' and line[1:5] != '更新時間':
            result += f"[s]{line[1:]}[/s]"
        if line[0] == '+' and line[1:5] != '更新時間':
            result += f"[u]{line[1:]}[/u] (更新於: {rUpdate})"
        if line[0] == '+' and line[1:5] == '更新時間':
            result += f"{line[1:]}"
        result += '\n'
    return result

cd = str(pathlib.Path(__file__).parent.resolve())
user_agent = UserAgent()
CLIENT_ID = "886c33830062f60"


def update(test, trecord, myLink, newlink, title, article_before, review, imgList):
    (tyear, tmonth, tday, thour, tminute) = trecord
    rUpdate = f'{tyear}-{tmonth}-{tday} {thour}:{tminute}'
    while True:
        list = []
        try:
            Response = requests.get(url=myLink, headers={ 'user-agent': user_agent.random }, timeout=5, verify=False)
            Soup = BeautifulSoup(Response.text, 'lxml')
            pArticle = Soup.find('article')
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
                    article = compare(article_before, text, rUpdate)
                    
                    upt(test, title, article, newlink)
                    day = datetime.datetime.today().weekday()
                    if day == 2:
                        break

        except requests.exceptions.ConnectionError:
            time.sleep(15)
            continue
        time.sleep(300)

if __name__ == '__main__':
    pass
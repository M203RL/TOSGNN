import numpy as np
import re
from urllib.parse import quote
import string
import pyperclip
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

def html2bbcode0(pArticle, author):
    bgcolor1 = '#eff7f6'
    bgcolor2 = '#f6fff8'
    space = '[div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]'
    wordList = []
    tables = pArticle.find_all('tbody')
    taList = []
    ca = 0
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
        at += '[/table][/div][div]'
        taList += [(space + at + space)]
        ca+=1
    ta = 0
    for item in pArticle:
        word = str(item)
        word = re.sub(r'<.*?acglink.*?>', '', word)
        word = re.sub(r'<.*?javascript.*?>', '', word)
        while '<table' in word:
            table = re.search(re.compile(r'<table.+?</table>', re.DOTALL), word).group()
            word = word.replace(table, 'table')
            
        while 'gnnPIC' in word:
            image = re.search(re.compile(r'<img .*?>', re.DOTALL), word).group()
            if 'gnnPIC' in image:
                link = re.search(r'data-src="(.*?)"', image).group(1)
                word = word.replace(image, '[div align=center width=100%][img='+link+' width=999][/div]')
            else:
                word = word.replace(image, '')
        word = word.replace('<h2>\n', space + space + space + space + '[div align=left][size=5][b][color=#145292]')
        word = word.replace('</h2>', '[/color][/b][/size][/div][hr]')
        word = word.replace('<h3>\n', space + space + space + space + '[div align=left][size=4][b][color=#145292]- ')
        word = word.replace('</h3>', ' -[/color][/b][/size][/div]')
        word = re.sub(r'<span style.*"><span style.*">', '[size=2][b][color=#4d4d4d]', word)
        word = re.sub(r'</span></span>', '[/b][/color][/size]', word)
        while '<figure class="pic-desc">' in word:
            des = re.search(re.compile(r'<figure class="pic-desc">\n(.*?)</figure>', re.DOTALL), word).group()
            text = re.search(re.compile(r'<figure class="pic-desc">\n(.*?)</figure>', re.DOTALL), word).group(1)
            word = word.replace(des, '[div align=center][size=2][color=#343a40]' + text + '[/color][/size][/div]')
        word = re.sub(r'<.*? class.*?">.*?</span>', '', word)
        word = re.sub(r'<.*? class.*?">', '', word)
        word = re.sub(r'</ul>', '', word)
        word = re.sub(r'</a>', '', word)
        word = re.sub(r'</li>', '', word)
        word = re.sub(r'<.*?figcaption.*?>', '', word)
        word = re.sub(r'<p style=".*">', '[size=2][b][color=#4d4d4d]', word)
        word = re.sub(r'</p>', '[/b][/color][/size]', word)
        word = re.sub(re.compile(r'<script.+?</script>', re.DOTALL),'',  word)
        word = re.sub(r'<p>', '', word)
        word = re.sub(r' 新聞內容 ', '', word)
        word = re.sub(r' 新聞內容結束 ', '', word)
        wordList += re.split('<div>|</div>|\n', word)
    text = '[div align=left][size=1][color=#343a40]發布時間: ' + author + '[/color][/size][/div][hr]'
    print(len(wordList))
    # txt(wordList)
    for i in wordList:
        if i == 'table':
            i = taList[ta]
            ta += 1
        if i != '':
            text += i + space
        #     tt = i.replace('<div> </div>', '')
        #     text += tt.replace('<div>', space).replace('</div>', space)
    return text

def html2bbcode1(pArticle, author):

    bgcolor1 = '#eff7f6'
    bgcolor2 = '#f6fff8'
    space = '[div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]'
    wordList = []
    tables = pArticle.find_all('tbody')
    taList = []
    ca = 0
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
        at += '[/table][/div][div]'
        taList += [(space + at + space)]
        ca+=1
    ta = 0
    for item in pArticle:
        word = str(item)
        word = word.replace('\n', '')
        while '<a class="acglink"' in word:
            ws = word.index('<a class="acglink"')
            wm = word.index('_blank">') + 8
            wf = word.index('</a>') + 4
            word = word.replace(word[ws : wf], word[wm  : wf - 4])
        word = word.replace('<h2>', space + '\n[div align=left][size=5][b][color=#145292]')
        word = word.replace('</h2>', '[/color][/b][/size][/div][hr]')
        word = word.replace('<h3>', space + '\n[div align=left][size=4][b][color=#145292]- ')
        word = word.replace('</h3>', ' -[/color][/b][/size][/div]')
        word = word.replace('<ul class="bh-grids-img">', '')
        word = word.replace('</ul>', '')
        word = word.replace('<li class="bh-grids-img-box" style="width: 99.87%;">', '')
        word = word.replace('<li class="bh-grids-img-box" style="width: 100.00%;">', '')
        word = word.replace('</li>', '')
        word = word.replace('<p> </p>', '')
        # word = word.replace('<div>', '')
        # word = word.replace('</div>', '')
        # while 'gnnPIC' in word:
        #     ws = word.index('<img')
        #     wm = word.index('data-src="') + 10
        #     wm2 = word.index('" data-srcset')
        #     wf = word.index('"/>') + 13
        #     link = word[wm  : wm2]
        #     word = word.replace(word[ws : wf], '[div align=center width=100%][img='+link+' width=999][/div]')
        while 'gnnPIC' in word:
            image = re.search(r'<img.*name="gnnPIC".*/>', word).group()
            link = re.search(r'.*data-src="(.*)" data-srcset="', image).group(1)
            print(image)
            word = word.replace(image, '[div align=center width=100%][img='+link+' width=999][/div]')
        while '<table' in word:
            ws = word.index('<table')
            wf = word.index('</table>') + 8
            word = word.replace(word[ws : wf], taList[ta])
            ta += 1
        while '<figure class="pic-desc">' in word:
            ws = word.index('<figure class="pic-desc">')
            wm = word.index('pic-desc">') + 10
            wf = word.index('</figure>') + 9
            text = '[div align=center][size=2][color=#343a40]'+word[wm : wf - 9]+'[/color][/size][/div]'
            word = word.replace(word[ws : wf], text)
        # while '<span style="color:' in word:
        #     ws = word.index('<span style="color:')
        #     wm = word.index('color:#808080;">') + 16
        #     wf = word.index('</span></span>') + 14
        #     text = '[size=2][b][color=#4d4d4d]' + word[wm : wf - 14] + '[/b][/color][/size]'
        #     word = word.replace(word[ws : wf], text)
        word = re.sub(r'<span style.*"><span style.*">', '[size=2][b][color=#4d4d4d]', word)
        word = re.sub(r'</span></span>', '[/b][/color][/size]', word)
        # while 'href="javascript' in word:
        #     ws = word.index('<a href="javascript')
        #     wf = word.index('></a>') + 5
        #     word = word.replace(word[ws : wf], '')
        
        word = word.replace('<div class="article_gamercard lazyload" data-fanspage-id="488" data-from="web_gnn"></div>', '')
        word = word.replace('<script id="wallFanspageCardTemplate" type="text/template">', '')
        word = word.replace('<div class="gamecard-name">', '')
        word = word.replace('<div class="gamecard__game">', '')
        word = word.replace('<div class="gamecard__background"></div>', '')
        word = word.replace('<div class="gamecard-img"></div>', '')
        word = word.replace('<p class="gamecard-label-name"></p>', '')
        word = word.replace('<p class="gamecard-label-people"><span></span> 人已追蹤，快追蹤取得最新情報！</p>', '')
        word = word.replace('<div class="gamecard-img"><a href="javascript:;"></a></div>', '')
        word = word.replace('<div class="gamecard__data">', '')
        word = word.replace('<div class="gamecard__info">', '')
        word = word.replace('<a href="javascript:;" class="gamecard__follow" data-want2playsn="[59899,59910]"></a>', '')
        word = word.replace('</script>', '')
        word = word.replace(' 新聞內容 ', '')
        word = word.replace(' 新聞內容結束', '')
        word = word.replace('<br/>', '\n')
        word = re.sub(r'<p style=".*">', '\n[size=2][b][color=#4d4d4d]', word)
        word = re.sub(r'</p>', '[/b][/color][/size]', word)
        wordList += [word]
    text = '[div align=left][size=1][color=#343a40]發布時間: ' + author + '[/color][/size][/div][hr]'
    for i in wordList:
        if i != '':
            tt = i.replace('<div> </div>', space)
            text += tt.replace('<div>', '').replace('</div>', '')
    return text

def html2bbcode2(pArticle, author):
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
        if '<table' in str(item) and '<div' not in str(item)[0:5] and '<center' not in str(item)[0:8]:
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
    for i in np.arange(len(allwords)):
        text += allwords[i]
    return text

def html2bbcode3(pArticle, figAll, author):
    nod = []
    space = '[div][table width=100% cellspacing=1 cellpadding=1 border=0][tr][td][/td][/tr][/table][/div]'
    ptable=pArticle
    allParts=pArticle.find_all()
    alldivs=[]
    allwords=[]
    for i in allParts:
        alldivs += [(str(i).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\n', u''))]
    # txt(alldivs)
    
    while all(x in alldivs[0] for x in alldivs[1:10]):
        del alldivs[0]
        del allParts[0]
        pArticle=pArticle.find('div')
    for i in allParts:
        if str(i).find('td')==-1 and str(i).find('gamecard')==-1:
            tx = i.text.strip()
            allwords += [(tx)]
        else:
            allwords += [('')]
        
    # txt(allwords)

    ytList = []
    ytVideos = pArticle.find_all('iframe')
    for v in ytVideos:
        ytLink = v['data-src']
        ix = allParts.index(v)
        alldivs[ix] = '[div][movie='+ytLink+' width=640 height=360][/div]'
        ytList += [(ytLink)]


    
    article = []
    wordArt = []
    wordList = []
    divWords = pArticle.find_all('div')
    for item in divWords:
        if 'quote-box' in str(item) and '<div' in str(item):
            word = item.text.strip()
            word = '[div][table width=100% cellspacing=1 cellpadding=1 border=1][tr][td]' + word + '[/td][/tr][/table][div]'
            article += [word]
            wordList += [(st)]
            wordArt += [(st)]
            nod += [(word)]
            continue 
        if not item.find('table') and not item.find('figure') and not item.find('h2') and not item.find('h3'):
            # if not item.find('figure'):
            tstring = str(item)
            word = item.text.strip()
            st = item.text.strip()
            if '　　' in tstring:
                article += [(space + '[div align=left]\u3000\u3000' + word + '[/div]' + space)]
                wordList += [(st)]
                wordArt += [(st)]
                nod += [(word)]
                continue
            if word!='':
                if str(item).find('span style="font-size:') !=- 1:
                    if str(item).find('span style="color:') == -1:
                        words = ''
                        item = ''
                        continue
                if str(item).find('style="font-size:') != -1:
                    word = '[size=2][b][color=#4d4d4d]' + word + '[/b][/color][/size]'
                    article += [(space + '[div align=left]' + word + '[/div]' + space)]
                    wordList += [(st)]
                    wordArt += [(st)]
                    nod += [(word)]
                    continue
            
        

    # txt(divWords)
    for word in wordArt:
        i=allwords.index(word)
        alldivs[i]='words'
        
    

    h2s=pArticle.find_all('h2')
    h2List=[]
    for ele in h2s:
        h2 = ele.text.strip()
        # .replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        # if not h2 in wordList:
        i2 = allParts.index(ele)
        allParts[i2] = 'hash'
        alldivs[i2] = 'h2'
        h2List += [(h2)]
            # wordList += [(h2)
        
    
    h3s=pArticle.find_all('h3')
    h3List=[]
    for ele in h3s:
        h3 = ele.text.strip()
        # .replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        # if not h3 in wordList:
        i3 = allParts.index(ele)
        allParts[i3] = 'hash'
        alldivs[i3] = 'h3'
        h3List += [(h3)]
        # wordList += [(h3)
        
    # txt(alldivs)
    
    

    lis = figAll.find_all('img',{'name':'gnnPIC'})
    liList = []
    for ele in lis:
        try:
            # fig = ele.find('img')
            pPhoto = ele['data-src']
            s = quote(pPhoto, safe=string.printable)
            tn='[div align=center][img='+s+' width=999][/div]'

        except TypeError:
            pPhoto=''
            tn=''
            pass
        liList += [(tn)]
        

    figd = figAll.find_all('figure',{'class':'pic-desc'})
    figdList = []
    for ele in figd:
        text = ele.text.strip()
        i = len(allwords)-allwords[::-1].index(text)
        alldivs[i-1] = '[div align=center][size=2][color=#343a40]' + text + '[/color][/size][/div]' + space
        figdList += [(text)]
        
    # txt(alldivs)
    # txt(figdList)
    



    tables = ptable.find_all('tbody')
    taList = []
    bgcolor1 = '#eff7f6'
    bgcolor2 = '#f6fff8'
    ca = 1
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
        at += '[/table][/div][div]'
        taList += [(space + at + space)]
        ca+=1
        
    
    liIndex = []
    ulIndex = []
    idx = 0
    for item in allParts:
        num2 = item.find('img')
        if num2 != None:
            if num2 != -1:
                ulIndex += [(idx)]
                # alldivs[idx]='empty2'
                alldivs[idx+1]='figure'
                if 'name="gnnPIC"' in str(num2) and not str(num2) in nod:
                    nod += [(str(num2))]
                if not str(num2) in nod:
                    alldivs[idx+1]='out'
                alldivs[idx]='out'
            
            
        idx+=1
        

    
    taIndex = []
    for ele in tables:
        taIndex += [(allParts.index(ele))]
        alldivs[allParts.index(ele)]='table'
        
    # txt(alldivs)
    for i in np.arange(len(alldivs)):
        if '</li>' in alldivs[i]:
            if not '</ul>' in alldivs[i]:
                if not 'pic-desc' in alldivs[i]:
                    word = space + '[div align=left][li]' + allParts[i].text.strip() + '[/li][/div]' + space 
                    alldivs[i] = word
                    continue
            else:
                alldivs[i] = 'out'
                continue
        if '</' in alldivs[i]:
            alldivs[i]='out'
            continue
        if '/>' in alldivs[i]:
            alldivs[i]='out'
            continue
        
    
    numW=0
    numT=0
    numh2=0
    numh3=0
    numF=0
    for i in np.arange(len(alldivs)):
        if alldivs[i]=='words':
            alldivs[i] = article[numW]
            numW+=1
            continue
        if alldivs[i]=='table':
            alldivs[i]=taList[numT]
            numT+=1
            continue
        if alldivs[i]=='h2':
            alldivs[i]=space + '\n[div align=left][size=5][b][color=#145292]' + h2List[numh2]+ '[/color][/b][/size][/div][hr]'
            numh2+=1
            continue
        if alldivs[i]=='h3':
            alldivs[i]=space + '\n[div align=left][size=4][b][color=#145292]- ' + h3List[numh3] + ' -[/color][/b][/size][/div]' + space
            numh3+=1
            continue
        if alldivs[i]=='figure':
            try:
                alldivs[i]=liList[numF]
                numF+=1
            except IndexError:
                alldivs[i]='out'
            continue
    
    alldivs = [ele for ele in alldivs if ele != 'out']
    
    res = [ele for ele in alldivs if ele != '']
    text = '[div align=left][size=1][color=#343a40]發布時間: ' + author + '[/color][/size][/div][hr]'
    for i in np.arange(len(res)):
        text += res[i]
    return text
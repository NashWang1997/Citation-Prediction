import os
import json
from bs4 import BeautifulSoup
import re

def getpaperinfo(content, id):
    path = 'detail'
    title = ''
    year = ''
    dic = {}
    soup = BeautifulSoup(content, 'html.parser')
    for i in soup.findAll('div'):
        if i.get('class') == ['result']:
            for j in i.find('h3'):
                title = j.string
            for k in i.findAll('div'):
                if k.get('class') == ['res_info']:
                    author = []
                    journal = []
                    refpape = []
                    year = k.find('span').string
                    for j in k.findAll('a'):
                        hreflist = re.findall(r"wd=.*", j.get('href'))
                        if hreflist[0][3:10] == 'author%':
                            author.append(j.string)
                        if hreflist[0][3:10] == 'journal':
                            journal.append(j.string)
                        if hreflist[0][3:10] == 'refpape':
                            refpape.append(j.string)
            # print(title)
            # print(year)
            # print(author)
            # print(journal)
            # print(refpape)
            dic['title'] = title
            dic['pubyear'] = year
            dic['coauthor'] = author
            if not len(journal) == 0:
                dic['pubjournal'] = journal[0]
            else:
                dic['pubjournal'] = ''
            if not len(refpape) == 0:
                dic['citation'] = refpape[0]
            else:
                dic['citation'] = '0'
            f = open(path+'/'+id+'.txt', 'a', encoding='utf-8')
            f.write(json.dumps(dic) + '\n')
            f.close()
def main():
    path = 'authors'
    #subpath = 'CN-BN74POSJ'
    #filename = 'http___xueshu.baidu.com_scholarID_CN-BN74POSJ2'
    for subpath in os.listdir(path):
        for filename in os.listdir(path+'/'+subpath):
            content = open(path+'/'+subpath+'/'+filename, 'r', encoding='utf-8')
            getpaperinfo(content, subpath)
main()
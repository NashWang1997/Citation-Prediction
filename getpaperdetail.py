import os
from bs4 import BeautifulSoup
import urllib.request
import time
import random
import re
import json

def getpaperlinks(content):
    paperlink = {}
    year = {}
    journal = {}
    citation = {}
    soup = BeautifulSoup(content, 'html.parser')
    for i in soup.findAll('div'):
        if i.get('class') == ['res_con']:
            j = i.find('h3')
            paperlink[j.find('a').string] = 'http:' + j.find('a').get('href')
            for k in i.findAll('div'):
                if k.get('class') == ['res_info']:
                    year[j.find('a').string] = k.find('span').string
                    for m in k.findAll('a'):
                        hreflist = re.findall(r"wd=.*", m.get('href'))
                        if hreflist == []:
                            journal[j.find('a').string] = ''
                            citation[j.find('a').string] = 0
                        elif hreflist[0][3:10] == 'refpape':
                            citation[j.find('a').string] = m.string
                        elif hreflist[0][3:10] == 'journal':
                            journal[j.find('a').string] = m.string
            if not j.find('a').string in year:
                year[j.find('a').string] = ''
            if not j.find('a').string in journal:
                journal[j.find('a').string] = ''
            if not j.find('a').string in citation:
                citation[j.find('a').string] = 0
    return paperlink, year, journal, citation
def getdetail(links):
    citabyear = {}
    for key in links:
        url = links[key]
        #time.sleep(random.randint(0, 1))
        content = urllib.request.urlopen(url).read().decode()
        print(url)
        soup = BeautifulSoup(content, "html.parser")
        for i in soup.findAll('script'):
            if not i.string == None:
                for k in re.findall(r"lineMapCitedData\s=\s\[.*]", i.string):
                    if not k == []:
                        citamap = {}
                        line = re.split('{|}', k)
                        for element in line:
                            if element[0:8] == '"cited":':
                                list = re.split(':|,', element)
                                citamap[list[-1]] = list[3]
                        citabyear[key] = citamap
                    else:
                        pass
            else:
                pass
        if not key in citabyear:
            citabyear[key] = {}
    return citabyear
def dealwith(citbyear, year, journal, citation):
    dic = {}
    tmp = [-1, -1, -1, -1, -1]
    if year == '':
        return dic
    try:
        startyear = int(year)
    except:
        return dic
    if startyear > 2015:
        return dic
    if citbyear == {}:
        for i in range(2011, 2016):
            if i > startyear:
                tmp[i-2011] = 0
        dic['pubyear'] = year
        dic['citby'] = tmp
        dic['journal'] = journal
        dic['citall'] = citation
        return dic
    for key in citbyear:
        if int(key)>=2011 and int(key)<=2015:
            tmp[int(key)-2011] = int(citbyear[key])
    dic['pubyear'] = year
    dic['citby'] = tmp
    dic['journal'] = journal
    dic['citall'] = citation
    return dic
def main():
    path = 'authors'
    pathnew = 'data2'
    #subpath = 'CN-BN74POSJ'
    #filename = 'http___xueshu.baidu.com_scholarID_CN-BN74POSJ2'
    for subpath in os.listdir(path):
        print(subpath)
        f = open(pathnew + '/' + subpath + '.json', 'w', encoding='utf-8')
        for filename in os.listdir(path + '/' + subpath):
            print(filename)
            content = open(path + '/' + subpath + '/' + filename, 'r', encoding='utf-8')
            links, year, journal,citation = getpaperlinks(content)
            citbyear = getdetail(links)
            #print(citbyear)
            for key in citbyear:
                if key in year and key in journal and key in citation:
                    dic = dealwith(citbyear[key], year[key], journal[key], citation[key])
                else:
                    dic = {}
                if not dic == {}:
                    f.write(json.dumps(dic)+'\n')
        f.close()
if __name__ == '__main__':
    main()
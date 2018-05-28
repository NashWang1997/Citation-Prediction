from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
import random
from queue import Queue
import re
import os
import requests
import json

def getauthorinfo(content):
    soup = BeautifulSoup(content, 'html.parser')
    dic = {}
    journal = {}
    coauthors = {}
    coaffname = []
    coaffnum = []
    co_affiliate_list = {}
    for i in soup.findAll('div'):
        if i.get('class') == ['p_name']:
            dic['name'] = i.string
        if i.get('class') == ['p_volume']:
            dic['volume'] = i.string[0:-3]
        if i.get('class') == ['p_affiliate']:
            dic['affiliate'] = i.string
        if i.get('class') == ['pieBox', 'journalBox']:
            for j in i.findAll('p'):
                plist = re.split('>|<', str(j))
                journalname = plist[2]
                for k in j.findAll('span'):
                    if k.get('class') == ['boxnum']:
                        publishnum = k.string
                journal[journalname] = publishnum
            dic['journal'] = journal
    for i in soup.findAll('li'):
        if i.get('class') == ['p_ach_item']:
            tmp = []
            for j in i.findAll('p'):
                tmp.append(j.string)
            if tmp[0] == '被引频次':
                dic['citation'] = tmp[1]
            if tmp[0] == '成果数':
                dic['papers'] = tmp[1]
            if tmp[0] == 'H指数':
                dic['Hindex'] = tmp[1]
            if tmp[0] == 'G指数':
                dic['Gindex'] = tmp[1]
    for i in soup.findAll('span'):
        if i.get('class') == ['p_scholarID_id']:
            dic['id'] = i.string
        if i.get('class') == ['au_info']:
            tmp = []
            for j in i.findAll('p'):
                if j.find('a'):
                    tmp.append(j.find('a').string)
                if j.find('span'):
                    tmp.append(j.find('span').string)
            try:
                coauthors[tmp[0]] = tmp[1]
            except:
                pass
        if i.get('class') == ['co_paper_name']:
            coaffname.append(i.get('title'))
        if i.get('class') == ['co_paper_count']:
            coaffnum.append(i.string)
    dic['coauthors'] = coauthors
    for i in range(len(coaffname)):
        co_affiliate_list[coaffname[i]] = coaffnum[i]
    dic['coaffiliate'] = co_affiliate_list
    for i in soup.findAll('script'):
        if not i.string == None:
            for k in re.findall(r"lineMapCitedData\s=\s\[.*]", i.string):
                if not k == []:
                    citamap = {}
                    line1 = re.split('{|}', k)
                    for element in line1:
                        if element[0:6] == '"year"':
                            list1 = re.split(':|,', element)
                            citamap[list1[1]] = list1[3]
                    dic['citamap'] = citamap
            for k in re.findall(r"lineMapAchData\s=\s\[.*]", i.string):
                if not k == []:
                    arhmap = {}
                    line1 = re.split('{|}', k)
                    for element in line1:
                        if element[0:6] == '"year"':
                            list1 = re.split(':|,', element)
                            arhmap[list1[1]] = list1[3]
                    dic['arhmap'] = arhmap
    for i in dic:
        print(i)
        print(dic[i])
    # f = open('info.json', 'a', encoding='utf-8')
    # f.write(json.dumps(dic) + '\n')
    # f.close()
def main():
    path = 'author'
    cnt = 0
    for filename in os.listdir(path):
        cnt += 1
        if cnt >= 2:
            continue
    #filename = 'http___xueshu.baidu.com_homepage_u_741a90c2a4b2a73d6bc7b8d94578fd42'
        content = open(path+'/'+filename, 'r', encoding='utf-8')
        print(filename+'\t'+str(cnt))
        getauthorinfo(content)
        content.close()
main()
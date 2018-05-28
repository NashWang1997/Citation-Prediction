from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
import random
from queue import Queue
import re
import os
import requests

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
def getinfo(text):
    soup = BeautifulSoup(text, 'html.parser')
    ScholarID = ''
    entity_id = ''
    Pages = ['1']
    for i in soup.findAll('a'):
        if i.get('class') == ['person_authen', 'p_auth_btn']:
            href = i.get('href')
            entity_id = re.split('=', href)[-1]
            break
    for i in soup.findAll('span'):
        if i.get('class') == ['p_scholarID_id']:
            ScholarID = i.string
        if i.get('class') == ['res-page-number', 'pagenumber']:
            Pages.append(i.string)
    return ScholarID, entity_id, Pages[-1]
def savepapers(ScholarID, entity_id, pages):
    url = 'http://xueshu.baidu.com/scholarID/' + ScholarID
    path = 'authors'
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh; q=0.9, en-US; q=0.8, en; q=0.7',
        'Content-Length': '131',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Host': 'xueshu.baidu.com',
        'Origin': 'http://xueshu.baidu.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': url,
        'X-Requested-With': 'XMLHttpRequest'
    }
    for page in range(1, int(pages)+1):
        from_data = {
            'cmd': 'academic_paper',
            'entity_id': entity_id,
            'bsToken': '5242892358eaf2dfdb9aeaa0a65d33f0',
            'sc_sort': 'sc_time',
            'curPageNum': str(page)
        }
        time.sleep(random.randint(0, 3))
        result = requests.post('http://xueshu.baidu.com/usercenter/data/author', data=from_data, headers=headers)
        content = result.content.decode()
        name = validateTitle(url) + str(page)
        if not os.path.exists(path + '/' +ScholarID):
            os.makedirs(path + '/' + ScholarID)
        f = open(path+'/'+ScholarID+'/'+name, 'w', encoding='utf-8')
        print(ScholarID+'\t'+name)
        f.write(content)
        f.close()
def main():
    path = 'author'
    for filename in os.listdir(path):
        #filename = 'http___xueshu.baidu.com_homepage_u_31c97b67f493a3f59f6b81694cf1df0d'
        text = open(path+'/'+filename, 'r', encoding='utf-8')
        ID, entity_id, pages = getinfo(text)
        savepapers(ID, entity_id, pages)
        text.close()
if __name__ == '__main__':
    main()
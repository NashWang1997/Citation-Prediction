from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
import random
from queue import Queue
import re

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
def writefile(url, content):
    path = 'author/'
    filename = validateTitle(url)
    f = open(path+filename, 'w', encoding='utf-8')
    print(url)
    f.write(content)
    f.close()
def getalllinks(url):
    time.sleep(random.randint(0, 3))
    content = urllib.request.urlopen(url).read().decode()
    soup = BeautifulSoup(content, "html.parser")
    writefile(url, content)
    links = []
    presite = 'http://xueshu.baidu.com'
    for i in soup.findAll('a'):
        if i.get('class') == ['au_name']:
            newurl = presite + i.get('href')
            links.append(newurl)
    return links
def crawl(url):
    tocrawl = Queue()
    crawled = []
    tocrawl.put(url)
    while not tocrawl.empty():
        url = tocrawl.get()
        if url not in crawled:
            links = getalllinks(url)
            for link in links:
                if not link in crawled:
                    tocrawl.put(link)
            crawled.append(url)
        if len(crawled) >= 1000:
            break
def main():
    url = 'http://xueshu.baidu.com/scholarID/CN-B874NFBJ'
    crawl(url)

if __name__ == '__main__':
    main()
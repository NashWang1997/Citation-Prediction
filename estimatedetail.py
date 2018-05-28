import os
import json
from bs4 import BeautifulSoup
import re

def main():
    path = 'detail'
    pathnew = 'data1.1'
    endyear = 2018
    years = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
    cnt = 0
    for filename in os.listdir(path):
        cnt += 1
        print(filename+'\t'+str(cnt))
        f = open(path+'/'+filename, 'r', encoding='utf-8')
        fw = open(pathnew+'/'+filename, 'w', encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            dic = json.loads(line)
            dicw = {}
            citbetw = []
            if dic['pubyear']==None or dic['citation']==None:
                continue
            try:
                startyear = int(dic['pubyear'])
                citall = int(dic['citation'])
            except:
                continue
            if startyear <= 2016:
                tmp = []
                diff = endyear - startyear + 1
                ave = citall // diff
                rest = citall - ave * diff
                for i in range(startyear, endyear+1):
                    if rest > 0:
                        tmp.append(ave+1)
                        rest -= 1
                    else:
                        tmp.append(ave)
                for i in range(1, len(tmp)):
                    tmp[i] += tmp[i-1]
                for year in years:
                    if year < startyear:
                        citbetw.append(-1)
                    else:
                        citbetw.append(tmp[year-startyear])
                dicw['pubyear'] = dic['pubyear']
                dicw['citation'] = dic['citation']
                dicw['citbyyear'] = citbetw
                dicw['pubjournal'] = dic['pubjournal']
                fw.write(json.dumps(dicw) + '\n')
            else:
                pass
        fw.close()
        f.close()
if __name__ == '__main__':
    main()
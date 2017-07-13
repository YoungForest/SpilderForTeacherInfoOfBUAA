# -*- coding: utf-8 -*-
"""
A spider to crawl the teachers' basic information at School of Computer Science
and Engineering(SCSE) of Beihang University.
"""

import requests
from bs4 import BeautifulSoup
import traceback
import re
import sys
import csv

def getHTMLText(url, param=None):
    """Get HTML text from url/param
    
    Return:
        String: a html text
    """
    try:
        r = requests.get(url, params=param)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return re.sub(r'\s+', ' ', r.text)
    except:
        return "raise a exception %s" %(r.status_code)

def killNewlineInList(contents):
    """remove all '\n' items from a list
    
    because beautifulsoup.contents alwasys generate annoying '\n'
    """
    try:
        # because we replace the '\n' with ' ' when get HTML text
#        while '\n' in contents:
#            contents.remove('\n')
        while ' ' in contents:
            contents.remove(' ')
        return contents
    except:
        traceback.print_exc()
        

def getATeacherInfo(card_div):
    """Get a teacher's expand information from tag div card_div
    
    Parameters:
        a soup
    
    Return:
        List: a teacher's info [name, job title, title, phone_number, email, 
        homepage, zip code, office, introduce]
    """
    try:
        card_divl = card_div.div    # only one div here because the topest isnot docment
        info = {}
        divs = killNewlineInList(killNewlineInList(card_divl.contents)[1].div.contents)
        # deal with 1st div
        spans1 = killNewlineInList(divs[0].contents)
        onclick = spans1[0].attrs['onclick'].split('\'')[1] # get the numbers series"toCardDetailAction('652c28c1-8cb2-44cf-92e2-fa841a9e2c1e');"
        name = spans1[0].string
        jobtitle = spans1[1].string
        #deal with 2nd div
        if divs[1].span:    # many teachers donot have a specific title
            title = divs[1].span.spring
        else:
            title = ''
        # 3rd div
        phone_number = killNewlineInList(divs[2].contents)[1].string
        # 4th div
        email = killNewlineInList(divs[3].contents)[1].string
        # 5th div
        homepage = killNewlineInList(divs[4].contents)[1].string
        info['name'] = name
        info['job_title'] = jobtitle
        info['title'] = title
        info['phone_number'] = phone_number
        info['email'] = email
        info['homepage'] = homepage
        url = "http://scse.buaa.edu.cn/buaa-css-web/toCardDetailAction.action?firstSelId=CARD_TMPL_OF_FIRST_NAVI_CN&secondSelId=CARD_TMPL_OF_ALL_TEACHER_CN&thirdSelId=&cardId=%s&language=0&curSelectNavId=CARD_TMPL_OF_ALL_TEACHER_CN" %(onclick)
        homepage = getHTMLText(url)
        soup = BeautifulSoup(homepage, "html.parser")
        details = soup.find_all('div', attrs={'class': 'card_detail'})
        zip_code = details[3].find('span', attrs={'class': 'card_detail_span'}).string
        office = details[4].find('span', attrs={'class': 'card_detail_span'}).string
        introduceP2 = soup.find('p', id='introduceP2')
        # Some teacher do not have a introduce even.
        if introduceP2:
            introduce = introduceP2.string
        else:
            introduce = 'nothing'
        info['zip_code'] = zip_code
        info['office'] = office
        info['introduce'] = introduce
        # print(info)
        # sys.exit()
    except:
        traceback.print_exc()
        # sys.exit()
    
    return info
    
def getTeachersInfo(url, infoList):
    """Get all teachers' information
    
    Parameters:
        url: the website where information put
        infoList: store the information
    """
    try:
        html = getHTMLText(url)
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find_all('div', attrs={'class': 'card_div'})
        for i in  div:
            infoList.append(getATeacherInfo(i))

    except:
        traceback.print_exc()

def saveToCSV(infoList):
    """Save the information list to csv file
    """
    head = ['name', 'job_title', 'title', 'phone_number', 'email', 
              'homepage', 'zip_code', 'office', 'introduce']
    ofile = open('teachers-info.csv', "w")
    writer = csv.DictWriter(ofile, fieldnames=head, dialect='unix')
    writer.writeheader()
    
    for row in infoList:
        try:
            writer.writerow(row)
        except:
            print(row)
            traceback.print_exc()
    ofile.close()
    # print(infoList)

if __name__ == "__main__":
    url = "http://scse.buaa.edu.cn/buaa-css-web/navigationTemplateListAction.action?firstSelId=CARD_TMPL_OF_FIRST_NAVI_CN&updateSelFirstNav=true&language=0"
    info = []
    getTeachersInfo(url, info)
    saveToCSV(info)

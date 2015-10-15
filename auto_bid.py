#!/usr/bin/env python
# -*-coding: utf-8 -*-
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import os
import re
import unicodedata
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup


"""
need put chromedriver.exe path into PATH
1. PySide for UI
2. selenium for website operation
3. BeautifulSoup for parse html
"""

global login_url, tender_url, username, password, paypasswd, browser, balance, total_interest, total_assets

def init_global():
    global login_url, tender_url, username, password, paypasswd, browser, balance, total_interest, total_assets
    login_url = "https://passport.eloancn.com/login?service=http%3A%2F%2Fwww.eloancn.com%2Fpage%2FuserMgr%2FmyHome.jsp%3Furl%3Dfresh%2FuserDefaultMessage.action%26menuid%3D1%26timestamp%3D14447502342114579"
    tender_url = "http://www.eloancn.com/new/loadAllTender.action"
    username = "15251611350"
    password = "xuyihua3590321"
    paypasswd = "xuyihua3590321"
    balance = 0
    total_interest = 0
    total_assets = 0


def open_chrome():
    global browser
    browser = webdriver.Chrome()
    browser.maximize_window()


def login_eloance():
    global browser, login_url, username, password

    # auto login
    try:
        browser.set_page_load_timeout(10)
        browser.get(login_url)
        browser.execute_script('window.stop()')
    except:
        # TODO : check if enter successful
        pass

    print("login website!")

    browser.find_element_by_id("loginName").send_keys([username, Keys.TAB, password, Keys.ENTER])
    sleep(5)
    print("Enter username and password")

    try:
        browser.set_page_load_timeout(5)        
        browser.execute_script('window.stop()')
        print("stop load this website")
    except:
        # TODO : check if login successful
        pass

    print("login successful!!!")


def unicode_to_int(u_data):
    temp1 = u_data.split('.')
    temp2 = temp1[0]    #just keep integer
    temp3 = unicodedata.normalize('NFKD', temp2).encode('ascii','ignore')
    temp4 = temp3.replace(',', '')
    return int(temp4)

def get_balance():
    global balance, browser
    webdata = browser.find_element_by_id("statField2").text
    balance = unicode_to_int(webdata)
    print("userful balance is %d¥" %balance)

def get_total_interest():
    global total_interest, browser
    webdata = browser.find_element_by_id("accumulative").text
    total_interest = unicode_to_int(webdata)
    print("total interest is %d¥" %total_interest)    

def get_total_assets():
    global total_interest, browser
    webdata = browser.find_element_by_id("total_assets").text
    total_assets = unicode_to_int(webdata)
    print("total assets is %d¥" %total_assets)

def get_money():
    get_balance()
    get_total_interest()
    get_total_assets()

def parse_lend_time(tag):
    time_tag = str(tag.contents[1].contents[0])
    time = (time_tag.split('>')[1]).split('<')[0]
    return int(time)

def parse_lend_schedule(tag):
    schedult_tag = str(tag.contents[1].contents[0].contents[0])
    schedult = (schedult_tag.split('%')[1]).split('>')[1]
    return int(schedult)

def parse_other(tag):
    return 60000


"""
1. get >=18% bid
2. sort bid money
3. check if balance > max bid money
4. get avaliable id to invest

## condiction:class="lendtable"/tenderid/
## each bid have 6 items
need return a list:{[tenderid, time, rate, remainder], [...]}
"""

def parse_target():
    global tender_url
    type_NavigableString = "<class 'BeautifulSoup.NavigableString'>"
    type_Tag = "<class 'BeautifulSoup.Tag'>"
    type_unicode = "<type 'unicode'>"
    lend_page = urllib2.urlopen(tender_url).read()
    soup = BeautifulSoup(''.join(lend_page))
    lendtable = soup.findAll(attrs={'class' : re.compile("lendtable")})  # get all lendtable, type:BeautifulSoup.ResultSet
    c1_child = lendtable[0]         # 1
    c2_child = c1_child.contents[1] # 2

    # TODO: if 100%, break
    # begin dividing:
    i = 0
    j = 0
    data = []         # new array
    for c3_child in c2_child:
        if i % 12 == 0:
            i = 0;
            dic = {}    # new dictionary
            # TODO: don't append this dic if schedule == 100
            data.append(dic)
            j = j + 1
            print("round : %d" %j)

        i = i + 1

        """
        i == 2:  lender pic, useless
        i == 4:  title and lender name, useless
        i == 6:  lend money, tender_id and interest rate(very useful) *****
        i == 8:  lend time, useful   **
        i == 10: schedule, useful(first check)    ***
        i == 12: count, useless
        """
        if i == 8:
            time = parse_lend_time(c3_child)
            dic['time'] = time
            print("month: %d" %time)
        elif i == 10:
            schedule = parse_lend_schedule(c3_child)
            dic['schedule'] = schedule
            print("schedule : %d%s" %(schedule, "%"))
        elif i == 6:
            list_other = parse_other(c3_child)
            dic['other'] = list_other

    return data

def main():
    init_global()
    #open_chrome()
    #login_eloance()
    #get_money()

    parse_target()
    print("End")

    #browser.get(tender_url)
    #browser.quit()

# main function
if __name__ == '__main__':
    main()


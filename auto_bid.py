#!/usr/bin/env python
# -*-coding: utf-8 -*-
from selenium import webdriver
from time import sleep, time, strftime
from selenium.webdriver.common.keys import Keys
import os, sys, re
import unicodedata
import urllib, urllib2
from PIL import Image
from pytesseract import image_to_string
from BeautifulSoup import BeautifulSoup

import datetime

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

def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def open_chrome():
    global browser
    browser = webdriver.Chrome()
    browser.maximize_window()


def login_eloance():
    global browser, login_url, username, password

    # auto login
    try:
        browser.set_page_load_timeout(5)
        browser.get(login_url)
        browser.execute_script('window.stop()')
    except:
        # TODO : check if enter successful
        pass

    print("login website!")
    elem = browser.find_element_by_id("loginName")
    #screen_shot(elem)
    browser.find_element_by_id("loginName").send_keys([username, Keys.TAB, password, Keys.ENTER])
    sleep(5)
    print("Enter username and password")

    #cookie= browser.get_cookies()
    #print cookie

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
    print("userful balance is %d元" %balance)

def get_total_interest():
    global total_interest, browser
    webdata = browser.find_element_by_id("accumulative").text
    total_interest = unicode_to_int(webdata)
    print("total interest is %d元" %total_interest) 

def get_total_assets():
    global total_interest, browser
    webdata = browser.find_element_by_id("total_assets").text
    total_assets = unicode_to_int(webdata)
    print("total assets is %d元" %total_assets)

def get_money():
    get_balance()
    get_total_interest()
    get_total_assets()

def load_tend_web():
    global tender_url, browser
    # load tender website
    try:
        browser.set_page_load_timeout(2)
        browser.get(tender_url)
        browser.execute_script('window.stop()')
    except:
        # TODO : check if enter successful
        #print("load_tend_web except")
        pass

def crop_verify_code(code_name):
    global browser
    pay_name = "pay.png"
    browser.save_screenshot(pay_name)
    #crop the verify code image
    im = Image.open(pay_name)
    box = (500, 300, 800, 600)
    region = im.crop(box)
    region.save(code_name)

def get_verify_code():
    threshold = 140
    code_name = "code.png"
    table = []

    # get verify code picture
    crop_verify_code(code_name)

    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    rep = {'O':'0',
           'I':'1','L':'1',
           'Z':'2',
           'S':'8'
           };
    im = Image.open(code_name)
    imgry = im.convert('L')
    imgry.save('g'+code_name)

    out = imgry.point(table, '1')
    out.save('b' + code_name)

    text = image_to_string(out)

    text = text.strip()
    text = text.upper()

    for r in rep:
        text = text.replace(r, rep[r])
    print(text)
    return text

def auto_bid(lendtable):
    global browser, paypasswd
    load_tend_web()
    max_rest_no = lendtable[0]['no']
    xpath_id = 5 * max_rest_no
    xpath = "/html/body/div[8]/div[2]/div[4]/dl/dd[" + str(xpath_id) + "]/a"
    browser.save_screenshot("before.png")
    browser.find_element_by_xpath(xpath).click()
    #sleep(1)
    browser.save_screenshot("click.png")
    # maybe need input money
    # input pay password
    browser.find_element_by_xpath("//*[@id=\"paypassowrd\"]").send_keys(paypasswd)
    browser.save_screenshot("enter_paypass.png")
    # get and input verify code
    verify_code = get_verify_code()
    browser.find_element_by_xpath("//*[@id=\"tenderRecordRandCode\"]").send_keys(verify_code)
    # make sure bid
    #browser.find_element_by_xpath("//*[@id=\"fastLender_1\"]/div[2]/div/p[6]/input[2]").click()

def parse_lend_time(tag):
    time_str = str(tag.contents[1].contents[0])
    time = (time_str.split('>')[1]).split('<')[0]
    return int(time)

def parse_lend_schedule(tag):
    schedul2_str = str(tag.contents[1].contents[0].contents[0])
    schedule = (schedule_str.split('%')[1]).split('>')[1]
    # just get integer
    schedule = schedule.split('.')[0]
    return int(schedule)

def parse_other(tag):
    money_str = str(tag.contents[1].contents[0])
    tender_id_tag = tag.contents[3].contents[1]
    rate_str = str(tender_id_tag.contents[0])
    tender_id = (str(tender_id_tag)).split('_')[1]
    #tender_id = int(tender_id_str.split('_')[1])
    money = int(money_str[3:].replace(',', ''))
    rate = int(rate_str[0:2])
    other = [money, rate, tender_id]
    return other


"""
1. get >=18% bid
2. sort bid money
3. check if balance > max bid money
4. get avaliable id to invest

## condiction:class="lendtable"/tenderid/
## each bid have 4 items
## id: needAmount_189691
need return a list:{[tenderid, time, rate, schedule], [...]}
"""

def parse_lendtable():
    global tender_url
    table = [] # new array

    try:
        lend_page = urllib2.urlopen(tender_url).read()
    except:
        lend_page = ""
        print("Internal Server Error")
        pass

    if lend_page != "":
        soup = BeautifulSoup(''.join(lend_page))
        lendtable = soup.findAll(attrs={'class' : re.compile("lendtable")})  # get all lendtable, type:BeautifulSoup.ResultSet
        c1_child = lendtable[0]         # 1
        c2_child = c1_child.contents[1] # 2

        # TODO: if 100%, break
        # begin dividing:
        i = 0
        j = 0       
        dic = {}
        for c3_child in c2_child:
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
                # now time is useless, ignore it.
                #time = parse_lend_time(c3_child)
                #dic['time'] = time
                pass
            elif i == 10:
                schedule = parse_lend_schedule(c3_child)
                dic['schedule'] = schedule
                # in case schedule is noninteger, so -1
                dic['rest'] = dic['money']/100*(100-dic['schedule']-1)
            elif i == 6:
                other = parse_other(c3_child)
                dic['tender_id'] = other.pop()
                dic['rate'] = other.pop()
                dic['money'] = other.pop()

            if i % 12 == 0:
                i = 0;
                j = j + 1
                dic['no'] = j
                # filter table
                if dic['rest'] <= 0 or dic['rate'] < 18:
                    #print("Drop this bid, schedule=%d, rate=%d." %(dic['schedule'], dic['rate']))
                    pass
                else:
                    print dic
                    table.append(dic)
                dic = {}    # new dictionary

    return table

def sort_lendtable(table):
    #table.sort(lambda x, y:cmp(x['rest'], y['rest']))
    table = sorted(table, key=lambda x:x['rest'], reverse=True)
    return table

def main():
    global browser
    init_global()
    open_chrome()
    login_eloance()
    #get_money()


    times = 1
    while True:
        lendtable = parse_lendtable()
        lendtable = sort_lendtable(lendtable)

        if lendtable == []:
            #print("%s --- check %d times." %(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), times))
            times = times + 1
            if times % 400 == 0:
                load_tend_web()
        else:
            #for dic in lendtable:
            #    print dic
            break

    auto_bid(lendtable)   

    print("End")

    #browser.get(tender_url)
    #browser.quit()


# main function
if __name__ == '__main__':
    main()


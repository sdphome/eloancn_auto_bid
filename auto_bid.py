#!/usr/bin/env python
# -*-coding: utf-8 -*-
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys #需要引入 keys 包
import os
import unicodedata

""" need put chromedriver.exe path into PATH
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
    browser.maximize_window()  #将浏览器最大化


def login_eloance():
    global browser, login_url, username, password

    # auto login
    try:
        browser.set_page_load_timeout(10)
        browser.get(login_url)
        browser.execute_script('window.stop()')
    except:
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
        pass

    # TODO: need check if login successful
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

def main():
    init_global()
    open_chrome()
    login_eloance()
    get_money()
    print("End")
    #browser.get(tender_url)
    #browser.quit()

# main function
if __name__ == '__main__':
    main()

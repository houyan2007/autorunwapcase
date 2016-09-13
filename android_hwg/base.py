#coding=utf-8
from selenium.common.exceptions import NoSuchElementException

def swipeToUp(browser,element,during):
    if element=='':
        width = browser.get_window_size()['width']
        height = browser.get_window_size()['height']
        browser.swipe(width / 2, height * 3 / 4, width / 2, height * 2 / 4, during)
        return True
    else:        
        try:exec(element)
        except NoSuchElementException,e:
            width = browser.get_window_size()['width']
            height = browser.get_window_size()['height']
            browser.swipe(width / 2, height * 3 / 4, width / 2, height * 2 / 4, during)
            swipeToUp(browser,element,during)
        else:
        	return True



def buy_login(browser):
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/et_username')
    except NoSuchElementException,e:
        return 'logined'
    browser.find_element_by_id('com.hnmall.haiwaigou:id/et_username').send_keys('18942519969')
    browser.find_element_by_id('com.hnmall.haiwaigou:id/et_password').send_keys('111111')
    browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_login').click()
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/expandListView')
    except NoSuchElementException,e:
        try:browser.find_element_by_id('com.hnmall.haiwaigou:id/bt_go_home')
        except NoSuchElementException,e:
            return False
    return True


def home_back(browser):    #找到搜索按钮的界面
    #从分类、购物车、爆款、个人中心页面->首页
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/index_home').click()
    except NoSuchElementException,e:
        pass
    else:return
        #从提交订单->商品详情页->首页、从支付完成界面放弃退款到首页
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/commit_order_button')
    except NoSuchElementException,e:
        pass
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/title_back').click()
    except NoSuchElementException,e:
        pass 
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/detail_cannel').click()
    except NoSuchElementException,e:
        pass
    browser.implicitly_wait(5)
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/bt_go_home').click()
    except NoSuchElementException,e:
        pass
    else:
        return   
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/positiveButton').click()
    except NoSuchElementException,e:
        pass
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_pay')
    except NoSuchElementException,e:
        pass
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/title_back').click()
    except NoSuchElementException,e:
        pass        
    try:browser.find_element_by_id('com.hnmall.haiwaigou:id/index_home').click()
    except NoSuchElementException,e:
        pass
    else:return



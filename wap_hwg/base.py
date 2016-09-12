#coding:utf-8
from selenium.common.exceptions import NoSuchElementException
import time

#商品详情链接
SHOP_URL='http://wap.hwg.youayun.cn/shop/sp-'
HWG_HRL='http://wap.hwg.youayun.cn/'
CENTER_URL='http://wap.hwg.youayun.cn/shop/membercenter.html'


def scroll(browser,element):
	browser.execute_script("arguments[0].scrollIntoViewIfNeeded(true);",element)

def is_element_present(browser,how, what):
    try: browser.find_element(by=how, value=what)
    except NoSuchElementException, e: return False
    return True

def buy_login(browser): 
    try:browser.find_element_by_name('loginname')
    except NoSuchElementException,e:
        return True
    else:
    	browser.find_element_by_name('loginname').send_keys('18942519969')#此处用户未作配置
    	browser.find_element_by_name('password').send_keys('111111')
        #browser.implicitly_wait(5)
        time.sleep(1)
        browser.find_element_by_css_selector('#loginform > div.org-qdModify.__login').click()
        try: browser.find_element_by_id('msg_confirm')   #用户名或者密码错误，弹窗提示
        except NoSuchElementException, e: 
            return True
        else:
            return False
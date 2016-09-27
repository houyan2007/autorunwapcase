#coding:utf-8
from selenium.common.exceptions import NoSuchElementException
import time

class BaseHWG(object):
    #静态变量
    SHOP_URL='http://wap.hwg.youayun.cn/shop/sp-'
    HWG_HRL='http://wap.hwg.youayun.cn/'
    CENTER_URL='http://wap.hwg.youayun.cn/shop/membercenter.html'
    CATEGORY_URL='http://wap.hwg.youayun.cn/shop/category/findShowCategories.html'

    def __init__(self,browser):
        self.browser=browser

    def scroll(self,element):
        self.browser.execute_script("arguments[0].scrollIntoViewIfNeeded(true);",element)

    def buy_login(self): 
        try:self.browser.find_element_by_name('loginname')
        except NoSuchElementException,e:
            return True
        else:
            self.browser.find_element_by_name('loginname').send_keys('18942519969')#此处用户未作配置
            self.browser.find_element_by_name('password').send_keys('111111')
            #browser.implicitly_wait(5)
            time.sleep(1)
            self.browser.find_element_by_css_selector('#loginform > div.org-qdModify.__login').click()
            try: self.browser.find_element_by_id('msg_confirm')   #用户名或者密码错误，弹窗提示
            except NoSuchElementException, e: 
                return True
            else:
                return False
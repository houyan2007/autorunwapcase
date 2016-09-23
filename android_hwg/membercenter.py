#coding=utf-8
from selenium.common.exceptions import NoSuchElementException
from base import BaseHWG

class Membercenter(BaseHWG):
    def __init__(self,browser):
        super(Membercenter,self).__init__(browser)
        self.browser=browser
        self.center_page()

    def __dir__(self):
        return ['register','login','nopay','addr_delete']

    def center_page(self):
        self.browser.implicitly_wait(5)
        self.home_back(BaseHWG.PageFlag)
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/index_personal').click()
        BaseHWG.PageFlag='membercenter'

    def islogin(self):
        try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_login')
        except NoSuchElementException,e:
            return True
        else:
            return False

    def loginout(self):
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_search').click()
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/ll_exist_login').click()
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/positiveButton').click()


    def login(self,mobileNumber,password):
        if self.islogin():
            self.loginout()
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_login').click()
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/et_username').send_keys(mobileNumber)
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/et_password').send_keys(password)
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_login').click()
        try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_username')
        except NoSuchElementException,e:
            BaseHWG.PageFlag='login'   #在登录界面
            return False
        else:
            return True

    def addr_delete(self,num=''):  #删除地址，默认只删除列表中的第1条记录，返回个人中心页面
        if num=='0' or num==0:
            return True
        if num!='':
            num=int(num)
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/ll_address').click()
        flag=0
        while True:
            try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/iv_delete_address')
            except NoSuchElementException,e:
                break   #地址列表为空,无需再删除
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/iv_delete_address').click()
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/positiveButton').click()
            flag=flag+1
            if num!='' and flag==num:
                break
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_back').click()
        return True

    def nopay(self):
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_pay').click()
        try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_pay_money').click()
        except NoSuchElementException,e:
            BaseHWG.PageFlag='nopay'
            return False   #待付款列表为空
        title=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_name').text
        if title==u'支付方式':
            BaseHWG.PageFlag='paytype_'+BaseHWG.PageFlag
            return True
        else:
            return False
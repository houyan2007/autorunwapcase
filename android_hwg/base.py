#coding=utf-8
from selenium.common.exceptions import NoSuchElementException

class BaseHWG(object):
    PageFlag='index'
    def __init__(self,browser):
        self.browser=browser

    def swipeToUp(self,element,during):
        if element=='':
            width = self.browser.get_window_size()['width']
            height = self.browser.get_window_size()['height']
            self.browser.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4, during)
            return True
        else:        
            try:exec(element)
            except NoSuchElementException,e:
                width = self.browser.get_window_size()['width']
                height = self.browser.get_window_size()['height']
                self.browser.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4, during)
                self.swipeToUp(element,during)
            else:
            	return True

    def pos_tap(self,element,t):  #t:点击要素的持续时间
        pos=element.location_in_view
        pos_x=pos[u'x']
        pos_y=pos[u'y']
        self.browser.tap([(pos_x,pos_y)],t)

    def is_pagebottom(self,element_str):
        goods_old=exec(element_str)
        self.swipeToUp('',1000)
        try:goods_new=exec(element_str)
        except NoSuchElementException,e:
            self.swipeToUp('',1000)
            goods_new=exec(element_str)
        if goods_old==goods_new:   #滑动到页面底部
            return True
        else:
            return False

    def is_elemadownelemb(self,elema,elemb):
        a_pos=elema.location_in_view
        a_y=a_pos[u'y']
        a_x=a_pos[u'x']
        try:
            b_pos=elemb.location_in_view
            b_y=b_pos[u'y']
        except NoSuchElementException,e:
            return a_x,a_y
        if a_y>b_y:
            return a_x,a_y
        else:
            return False

    def buy_login(self):
        try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/et_username')
        except NoSuchElementException,e:
            return 'logined'
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/et_username').send_keys('18942519969')
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/et_password').send_keys('111111')
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_login').click()
        try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/expandListView')
        except NoSuchElementException,e:
            try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/bt_go_home')
            except NoSuchElementException,e:
                return False
        return True


    def home_back(self,PageFlag):    #找到搜索按钮的界面
        print PageFlag
        if PageFlag=='index':
            return
        elif PageFlag in ['cart','membercenter','cart2order','nopay','paytype_cart2order','paytype_membercenter']:
            if PageFlag in ['cart2order','nopay','paytype_cart2order','paytype_membercenter']:
                self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_back').click()
                if PageFlag in ['paytype_cart2order','paytype_membercenter']:
                    self.browser.find_element_by_id('com.hnmall.haiwaigou:id/positiveButton').click() 
                    self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_back').click()
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/index_home').click()
            return
        elif PageFlag=='searchresult':
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_back').click()
            try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/search_edittext').send_keys('')
            except NoSuchElementException,e:
                pass
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/search_cannel').click()
            return
        elif PageFlag in ['shop','shopspec','shop2order','spec2order','paytype_shop2order','paytype_spec2order']:
            if PageFlag in ['shop2order','spec2order','paytype_shop2order','paytype_spec2order']:
                self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_back').click()
                if PageFlag in ['paytype_shop2order','paytype_spec2order']:
                    self.browser.find_element_by_id('com.hnmall.haiwaigou:id/positiveButton').click()  
                    self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_back').click()            
            if PageFlag in ['shopspec','spec2order','paytype_spec2order']:
                self.browser.find_element_by_id('com.hnmall.haiwaigou:id/detail_cannel').click()
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/bt_go_home').click()
            return
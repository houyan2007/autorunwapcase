#coding=utf-8
from selenium.common.exceptions import NoSuchElementException
from base import BaseHWG

class Index(BaseHWG):
	def __init__(self,browser):
		self.browser=browser
		self.index_page()

	def index_page(self):
		self.home_back(BaseHWG.PageFlag)
		PageFlag='index'

	def search(self,name):
        if name=='':
            return False
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_search').click()
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/search_edittext').send_keys(name)
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/search_cannel').click()
        try:gridview=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/default_textbutton')
        except NoSuchElementException,e:
            BaseHWG.PageFlag='searchresult'
            return False   #没有搜索到对应的商品
        else:   #点击搜索结果的第1条记录
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/act_session_item_img').click()
            try:title=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_name').text
            except NoSuchElementException,e:
                return False  #未跳转到商品详情页
            else:
                if title==u'商品详情':
                    return True
                else:
                    return False


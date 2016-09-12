#coding=utf-8
from selenium.common.exceptions import NoSuchElementException

class Membercenter(object):
	def __init__(self,browser):
		self.browser=browser
		self.init_result()

	def __dir__(self):
		return ['caculate_add']

	def init_result(self):
		edit_text=self.browser.find_element_by_id('com.meizu.flyme.calculator:id/edit_text').text
		if edit_text!='':
			self.browser.find_element_by_id('com.meizu.flyme.calculator:id/clear_simple').click()
		try:result_text=self.browser.find_element_by_id('com.meizu.flyme.calculator:id/result_text')
		except NoSuchElementException,e:
			pass
		else:
			self.browser.find_element_by_id('com.meizu.flyme.calculator:id/clear_simple').click()

	def caculate_add(self,num1,num2):
		self.browser.find_element_by_id('com.meizu.flyme.calculator:id/digit%s' % num1).click()
		self.browser.find_element_by_id('com.meizu.flyme.calculator:id/plus').click()
		self.browser.find_element_by_id('com.meizu.flyme.calculator:id/digit%s' % num2).click()
		self.browser.find_element_by_id('com.meizu.flyme.calculator:id/clear').click()
		result=self.browser.find_element_by_id('com.meizu.flyme.calculator:id/edit_text').text
		return result


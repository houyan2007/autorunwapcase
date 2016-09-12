#coding:utf-8
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest

capabilities ={'device':'android',
'platformName': 'Android',
'platformVersion': '5.0.1',
'deviceName': 'MEIZU MX4',
'browserName':  'Chrome'  #'Safari’ for iOS and 'Chrome’, 'Chromium’, or 'Browser’ for Android
}

class WapTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Remote('http://localhost:4723/wd/hub', capabilities)
 
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
    """
    def setUp(self):
        self.browser=Browser('chrome')

    def tearDown(self):
        self.browser.quit()
    """
    def is_element_present(self, how, what):
        try: self.browser.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
 
    def getTest(self,file_name, sheetname,caseid,content,condition,case_steps,expects):      
        u"""%(file_name)s-%(sheetname)s-%(caseid)d-%(content)s"""
        browser=self.browser
        browser.get(condition)
        step_list=case_steps.split('\n')
        for i in step_list:
            exec(i.strip())

        if expects:
            expect_list=expects.split('\n')
            for j in expect_list:
                exec(j.strip())

    @staticmethod  
    def getTestFunc(file_name, sheetname,caseid,content,condition,case_steps,expects):
        def func(self):
            self.getTest(file_name, sheetname,caseid,content,condition,case_steps,expects)
        return func

if __name__=='__main__':
    print 'No main file'
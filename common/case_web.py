#coding:utf-8
import unittest
from splinter import Browser

class WebTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser=Browser('chrome',fullscreen=True)
 
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
    """
    def setUp(self):
        self.browser=Browser('chrome')

    def tearDown(self):
        self.browser.quit()
    """
 
    def getTest(self,file_name, sheetname,caseid,content,condition,case_steps,expects):      
        u"""%(file_name)s-%(sheetname)s-%(caseid)d-%(content)s"""
        browser=self.browser
        browser.visit(condition)
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
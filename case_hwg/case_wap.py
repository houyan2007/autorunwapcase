#coding:utf-8
import sys
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest
import mobile_flag

SRC_FLAG=''
MOBIL_FLAG=''
cap_dict={}
input_para=sys.argv
if len(input_para)!=1 and len(input_para)!=3:
    print '输入参数错误'
if len(input_para)==3:
    SRC_FLAG=input_para[1].lower()
    MOBIL_FLAG=input_para[2].lower()
    cap_dict=eval(mobile_flag.'capabilities_'+MOBIL_FLAG+'_'+SRC_FLAG)
if len(input_para)==1:
    SRC_FLAG='wap'
    cap_dict=capabilities_wap_mx

if SRC_FLAG=='wap':
    from wap_hwg import membercenter,shop,cart,order
elif SRC_FLAG=='android':
    from android_hwg import membercenter,shop,cart,order
else:
    print '参数错误'


class WapTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Remote('http://localhost:4723/wd/hub', cap_dict)
 
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
    """
    def setUp(self):
        self.browser=webdriver.Remote('http://localhost:4723/wd/hub', capabilities_mx_app)

    def tearDown(self):
        self.browser.quit()
    """

    def case_step(self,case_cmd):
        funcsplitl=case_cmd.find('(')
        if funcsplitl==-1:
            pass
        funcname=case_cmd[:funcsplitl].strip()
        funcsplitr=case_cmd[funcsplitl+1:].strip()
        if funcsplitr==')':
            case_cmd_str=funcname+'()'
        else:
            funcargs=case_cmd[funcsplitl+1:-1].strip().split(',')
            case_cmd_str=funcname+'('
            for i,funcarg in enumerate(funcargs):#funcargs
                funcargs[i]=unicode(funcarg.strip())
                case_cmd_str=case_cmd_str+"u'"+funcargs[i]+"'"+','
            case_cmd_str=case_cmd_str[:-1]+')'
        hwgobj=None
        classlist=[membercenter.Membercenter,shop.Shop,cart.Cart,order.Order]
        for i in classlist:
            if funcname in dir(i):
                hwgobj=i(self.browser) 
            else:
                pass 
        print 'hwgobj.%s'% case_cmd_str
        return eval('hwgobj.%s'% case_cmd_str)

    def case_expect(self,step_list,expect):
        step_results=[]
        for case_cmd in step_list:
            step_result=self.case_step(case_cmd.strip())
            step_results.append(step_result)
        print step_results
        if expect.find('find')>-1:  #该判断不可用
            lfind=expect.find('(')
            llfind=expect[lfind+1:-1].strip()
            htmltext=htmlparse.HtmlParse(self.browser.current_url)
            result=htmltext.find(llfind)
            self.assertTrue(result)
        elif expect.lower()=='true':
            if False in step_results:
                self.assertTrue(False)
            elif True not in step_results:
                self.assertTrue(False)
            else:
                self.assertTrue(True)
        elif expect.lower()=='false':
            if step_results[-1]==False:
                self.assertFalse(False)
            else:
                self.assertFalse(True)
        else:  #直接比对结果
            self.assertEqual(expect.lower(),step_results[-1].lower())
            
 
    def getTest(self,file_name, sheetname,caseid,content,condition,case_steps,expects):      
        u"""%(file_name)s-%(sheetname)s-%(caseid)d-%(content)s"""
        if condition!=None:
            self.browser.get(condition)
        else:
            pass #在上一个用例基础上不跳转新界面
        step_list=case_steps.split('\n')
        expects=str(expects)
        self.case_expect(step_list,expects)

    @staticmethod  
    def getTestFunc(file_name, sheetname,caseid,content,condition,case_steps,expects):
        def func(self):
            self.getTest(file_name, sheetname,caseid,content,condition,case_steps,expects)
        return func

if __name__=='__main__':
    print 'No main file'
#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#BASE_DIR=os.path.dirname(os.path.abspath(__file__)) #路径为当前文件所在目录
BASE_DIR=os.path.abspath(os.path.dirname(__file__) + '/' + '..')  #路径为当前文件所在的父目录 
BASE_DIR=BASE_DIR.decode("GBK")
CASE_DIR=os.path.join(BASE_DIR,u'testcase')
REPORT_DIR=os.path.join(BASE_DIR,u'report')
EXCEL_DIR=os.path.join(BASE_DIR,u'测试用例')

if __name__=='__main__':
    print 'No main file'

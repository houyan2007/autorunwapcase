#coding:utf-8
import os,time,sys
import unittest,HTMLTestRunner
from common import config,case_excel
from case_hwg import case_wap

def files_list(parentpath):
    file_list=os.listdir(parentpath)
    excel_list=[os.path.join(parentpath,f) for f in file_list if f.endswith('.xlsx') and not f.startswith('~')]
    return excel_list

def excels_read(excel_list):
    test_case=[]
    for excel_file in excel_list:
        excel_case=case_excel.ExcelCase(excel_file)
        excel_rows=excel_case.excel_read()
        case_dic=excel_case.casedic
        file_name=excel_file.split("\\")[-1][:-5]
        for sheet_name,rows in excel_rows:
            for row_i in rows:
                test_case.append((file_name,sheet_name,case_dic,row_i))
    return test_case

'''       
def __generateTestCases():
    excel_list=files_list(config.EXCEL_DIR)
    arglists=excels_read(excel_list)
    for args in arglists:
        setattr(case_web.WebTestCase, 'test_func_%s_%s_%s_%s'%(args[0], args[1],args[3][0],args[3][1]),
            case_web.WebTestCase.getTestFunc(args[0], args[1],args[3][0],args[3][1],args[3][3],args[3][4],args[3][5]))
        #通过setattr自动为TestCase类添加成员方法,方法以"test_func_"开头

def suite():
    __generateTestCases()
    return unittest.makeSuite(MyTestCase, "test")'''

def main():
    syslen=len(sys.argv)
    if syslen>=2 and sys.argv[1].lower() not in ['wap','web']:
        print '参数错误，第2个参数，应该是wap或者web'
        return False
    suite=''
    excel_list=files_list(config.EXCEL_DIR)
    arglists=excels_read(excel_list)
    if syslen==1 or (syslen==2 and sys.argv[1].lower()=='wap'):#默认是wap端
        for args in arglists:
            steps=args[3][4].decode('utf-8')
            setattr(case_wap.WapTestCase, 'test_func_%s_%s_%s_%s_%s'%(args[0], args[1],args[3][0],args[3][1],args[3][2]),
                case_wap.WapTestCase.getTestFunc(args[0], args[1],args[3][0],args[3][1],args[3][3],steps,args[3][5]))
            #通过setattr自动为TestCase类添加成员方法,方法以"test_func_"开头
        suite=unittest.makeSuite(case_wap.WapTestCase, "test")  
    elif syslen==2 and sys.argv[1].lower()=='web':
        for args in arglists:
            setattr(case_web.WebTestCase, 'test_func_%s_%s_%s_%s'%(args[0], args[1],args[3][0],args[3][1]),
                case_web.WebTestCase.getTestFunc(args[0], args[1],args[3][0],args[3][1],args[3][3],args[3][4],args[3][5]))
            #通过setattr自动为TestCase类添加成员方法,方法以"test_func_"开头
        suite=unittest.makeSuite(case_web.WebTestCase, "test")
    else:  
        return False
    now=time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime(time.time()))
    htmlreport=os.path.join(config.REPORT_DIR,now+'_result.html')
    htmlfile=file(htmlreport,'wb')
    runner=HTMLTestRunner.HTMLTestRunner(stream=htmlfile,title=u'测试报告',description=u'用例执行情况')
    runner.run(suite)

if __name__=='__main__':
    print 'Begin'
    main()
    print 'End'

    """
    待完成工作表：
    1、错误用例的识别判断
    2、执行失败定位用例信息
    3、多线程
    4、浏览器可以选择后台启动
    """
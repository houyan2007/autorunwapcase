#coding:utf-8
import os,time
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
        self.browser.get(BaseHWG.CENTER_URL)

    def isLogin(self):
        try: self.browser.find_element_by_class_name('userInfo')
        except NoSuchElementException, e: 
            return False
        return True

    def logout(self):
        if not self.isLogin():
            return False
        js="window.scrollTo(0, document.body.scrollHeight)"
        self.browser.execute_script(js)
        self.browser.find_element_by_link_text(u'退出登录').click() #此时会跳转到首页
        self.browser.find_element_by_link_text(u'我的').click()
        return True

    def register(self,mobileNumber,verifyCode,password):
        dologout=self.logout()
        #点击注册按钮，跳转到注册界面
        self.browser.find_element_by_class_name('userBtns').find_element_by_css_selector('a:nth-child(1)').click() 
        self.browser.find_element_by_name('mobileNumber').send_keys(mobileNumber)
        self.browser.find_element_by_name('verifyCode').send_keys(verifyCode)
        try: self.browser.find_element_by_id('mobileNumber-error')   #注册号码错误,界面有提示信息
        except NoSuchElementException, e: 
            return False
        self.browser.find_element_by_css_selector('#registerform > div.org-qdModify.__register').click()
        try: self.browser.find_element_by_id('msg_confirm')   
        except NoSuchElementException, e: 
            return False
        self.browser.find_element_by_id('password').send_keys(password)
        self.browser.find_element_by_name('rpassword').send_keys(password)
        try: self.browser.find_element_by_id('password-error')   #密码不符合要求
        except NoSuchElementException, e: 
            return False
        try: self.browser.find_element_by_id('rpassword-error')   #重复密码不符合要求
        except NoSuchElementException, e: 
            return False
        self.browser.find_element_by_css_selector('#registerConfirmform > div.org-qdModify.__registerConfirm').click()
        return True
            
    def login(self,mobileNumber,password):
        dologout=self.logout()
        #点击登陆按钮，跳转到登陆界面
        self.browser.find_element_by_class_name('userBtns').find_element_by_css_selector('a:nth-child(2)').click()
        self.browser.find_element_by_name('loginname').send_keys(mobileNumber)
        self.browser.find_element_by_name('password').send_keys(password)
        #self.browser.implicitly_wait(5)
        time.sleep(1)
        self.browser.find_element_by_css_selector('#loginform > div.org-qdModify.__login').click()
        try: self.browser.find_element_by_id('msg_confirm')   #用户名或者密码错误，弹窗提示
        except NoSuchElementException, e: 
            try:self.browser.find_element_by_class_name('userInfo')  #判断出现了用户信息，即认为正确
            except NoSuchElementException, e: 
                return False
            else:
                return True
        else:
            return False

    def nopay(self):#只查最新待付款记录,点击去支付按钮
        self.browser.find_element_by_class_name('userGoods_1').click()  #点击待付款按钮
        try:first_order=self.browser.find_element_by_class_name('order-box ')
        except NoSuchElementException,e:
            return False   #该页面记录为空
        else:
            try:first_order.find_element_by_name('countdown1')
            except NoSuchElementException,e:
                return False  #没有找到倒计时
            try:first_order.find_element_by_link_text(u'去支付').click()
            except NoSuchElementException,e:
                return False   #没有找到去支付按钮
            if self.browser.find_element_by_class_name('title').text==u'选择支付方式':
                return True
            else:
                return False


    def idcard(self,name,number,fileA,fileB):
        self.browser.find_element_by_link_text(u'身份证认证').click()
        self.browser.implicitly_wait(5)
        try: self.browser.find_element_by_class_name('empty_btn')
        except NoSuchElementException, e:  
            dels=self.browser.find_elements_by_class_name('del')
            for dela in dels:
                dela.click()
                self.browser.find_element_by_id('SD_confirm').click()  
        finally:
            self.browser.find_element_by_class_name('empty_btn').click()
            self.browser.find_element_by_id('name').send_keys(name)
            self.browser.find_element_by_id('number').send_keys(number)
            self.browser.find_element_by_id('fileA').send_keys(os.path.abspath(fileA))
            self.browser.find_element_by_id('fileB').send_keys(os.path.abspath(fileB))
            self.browser.find_element_by_class_name('screening').click()
        if self.browser.find_element_by_id('SD_window'):
            return False
        else:
            return True

    def addr_delete(self,num=''):  #删除地址，默认只删除列表中的第1条记录
        if num=='0' or num==0:
            return True
        if num!='':
            num=int(num)
        self.browser.find_element_by_link_text(u'我的地址').click()
        try:elements=self.browser.find_elements_by_class_name('order-time')
        except NoSuchElementException,e:
            return True  #地址列表为空,无需再删除
        else:
            flag=0
            for element in elements:
                if num=='':
                    element.find_element_by_class_name('del').click()
                else:
                    element.find_element_by_class_name('del').click()
                    flag=flag+1
                self.browser.implicitly_wait(5)
                self.browser.find_element_by_id('SD_confirm').click()
                if flag==num:
                    break
            return True
                


if __name__=='__main__':
    print dir(Membercenter)

    """
    //移动到元素element对象的“顶端”与当前窗口的“顶部”对齐  
((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView();", element);  
((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView(true);", element);  
  
//移动到元素element对象的“底端”与当前窗口的“底部”对齐  
((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView(false);", element);  
  
//移动到页面最底部  
((JavascriptExecutor) driver).executeScript("window.scrollTo(0, document.body.scrollHeight)");  
  
//移动到指定的坐标(相对当前的坐标移动)  
((JavascriptExecutor) driver).executeScript("window.scrollBy(0, 700)");  
Thread.sleep(3000);  
//结合上面的scrollBy语句，相当于移动到700+800=1600像素位置  
((JavascriptExecutor) driver).executeScript("window.scrollBy(0, 800)");  
  
//移动到窗口绝对位置坐标，如下移动到纵坐标1600像素位置  
((JavascriptExecutor) driver).executeScript("window.scrollTo(0, 1600)");  
Thread.sleep(3000);  
//结合上面的scrollTo语句，仍然移动到纵坐标1200像素位置  
((JavascriptExecutor) driver).executeScript("window.scrollTo(0, 1200)");  
"""
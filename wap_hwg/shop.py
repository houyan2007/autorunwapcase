#coding:utf-8
from base import SHOP_URL,buy_login,scroll
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import time

class Shop(object): #基于登录后
    def __init__(self,browser):
        self.browser=browser

    def __dir__(self):
        return ['goods_max','goods_min','goods_change','goods_buyadd']

    def goods_page(self,sp):
        goods_url='%s%s.html' % (SHOP_URL,sp)
        self.browser.get(goods_url)
        try:self.browser.find_element_by_id('banner')
        except NoSuchElementException,e:
            return False
        return True

    def buy_click(self,mb):
        if mb==False:  #在商品详情页点击立即购买
            try:self.browser.find_element_by_class_name('icon-close').click()
            except WebDriverException,e:
                pass
            self.browser.implicitly_wait(5)
            self.browser.find_element_by_class_name('goodsBtns').find_element_by_link_text(u'立即购买').click()
        else: #在规格面板点击立即购买
            self.browser.find_element_by_class_name('goodsSureBtn').find_element_by_link_text(u'立即购买').click()

    def add_click(self,mb):            
        if mb==False: #在商品详情页点击加入购物车
            try:self.browser.find_element_by_class_name('goods_close').click()
            except WebDriverException,e:
                pass
            self.browser.implicitly_wait(5)
            self.browser.find_element_by_class_name('goodsBtns').find_element_by_link_text(u'加入购物车').click()
        else:  #在规格面板点击加入购物车
            self.browser.find_element_by_class_name('goodsSureBtn').find_element_by_link_text(u'加入购物车').click()

    def goods_buyadd(self,sp='',goodsbuy=False,goodsadd=False,mb=False):
        if str(goodsbuy).lower()=='false':goodsbuy=False
        if str(goodsbuy).lower()=='true':goodsbuy=True
        if str(goodsadd).lower()=='false':goodsadd=False
        if str(goodsadd).lower()=='true':goodsadd=True    
        if str(mb).lower()=='false':mb=False
        if str(mb).lower()=='true':mb=True
        if sp!='':
            if not self.goods_page(sp): 
                return False #打开商品详情页失败，直接退出  
            if mb==True:
                self.selected_show()
        if goodsbuy==False and goodsadd==False:  #不点击立即购买、加入购物车按钮
            try:self.browser.find_element_by_id('banner')
            except NoSuchElementException,e:
                return False
            else:
                return True
        if goodsbuy==True:
            self.buy_click(mb)
            if not buy_login(self.browser):
                return False
            if self.browser.find_element_by_class_name('title').text==u'提交订单':
                return True
            else:
                return False
        elif goodsadd==True:
            self.add_click(mb)
            try:self.browser.find_element_by_css_selector('#SD_window > div > div > em')
            except NoSuchElementException,e:
                return False
            else:
                if self.browser.find_element_by_css_selector('#SD_window > div > div > em').text=='已成功加入购物车':
                    return True
                else:
                    return False           
        else:
            return False


    def selected_show(self):
        element=self.browser.find_element_by_css_selector(
            'body > div.box > div.goods > div.goods_top > div.selectedShow.clearfix')
        scroll(self.browser,element) 
        element.click()

    def goods_numvalue(self):
        js_="window.scrollTo(0, document.body.scrollHeight)"
        self.browser.execute_script(js_)
        js_value='return document.getElementById("number").value'
        num=self.browser.execute_script(js_value)
        return int(num)


    def inver_unable(self):
        try:
            self.browser.find_element_by_id('SD_window')
        except NoSuchElementException as e:
            try:self.browser.find_element_by_class_name('inve').find_element_by_css_selector('span.inver.unable')
            except NoSuchElementException as e:
                return False
            else:
                return True
        else:
            return True


    def goods_inver(self,number):
        if number!='max':
            number=int(number)
        while not self.inver_unable():
            self.browser.find_element_by_class_name('inver').click()
            num=self.goods_numvalue()
            if number!='max' and num>=number:
                return num
        return self.goods_numvalue()

    def invel_unable(self):
        if self.goods_numvalue()==1:
            return True
        try: self.browser.find_element_by_class_name('inve').find_element_by_css_selector('span.invel.unable')
        except NoSuchElementException as e:
            return False
        else:
            return True

    def goods_invel(self,number):
        if number!='min':
            number=int(number)
        while not self.invel_unable():
            self.browser.find_element_by_class_name('invel').click()
            num=self.goods_numvalue()
            if number!='min' and num<=number:
                return num
        return self.goods_numvalue()
       

    def goods_max(self,sp,num,goodsbuy=False,goodsadd=False,mb=False):
        if not self.goods_page(sp): 
            return False #打开商品详情页失败，直接退出
        self.selected_show()
        js_="window.scrollTo(0, document.body.scrollHeight)"
        self.browser.execute_script(js_)
        number=self.goods_inver('max')
        num=int(num)
        if number!=num:
            return False  #购买的最大数量与用例要求不一致
        else:
            return self.goods_buyadd('',goodsbuy,goodsadd,mb)



    def goods_min(self,sp,num,goodsbuy=False,goodsadd=False,mb=False): 
        if not self.goods_page(sp): 
            return False #打开商品详情页失败，直接退出
        self.selected_show()
        js_="window.scrollTo(0, document.body.scrollHeight)"
        self.browser.execute_script(js_)
        number=self.goods_invel('min')
        num=int(num)
        if number!=num:
            return False #购买的最小数量与用例要求不一致
        else:
            return self.goods_buyadd('',goodsbuy,goodsadd,mb)


    def goods_change(self,sp,spec,num,goodsbuy=False,goodsadd=False,mb=False):
        if not self.goods_page(sp): 
            return False #打开商品详情页失败，直接退出
        self.selected_show()
        if spec!='':  #更新为其他规格，若spec=='',表不更新规格
            parent=self.browser.find_element_by_css_selector(
                'body > div.box > div.goodsDialog > div > div.dialog_scroll > div.size-select.select.clearfix')
            children=parent.find_elements_by_class_name('able')
            for able in children:
                if able.text.lower()==spec.lower():
                    scroll(self.browser,able)
                    able.click()
                    break
        number=self.goods_numvalue()
        num=int(num)  
        if number<num:  #购买数量大于默认数量，点击加处理
            self.goods_inver(num)
            numberadd=self.goods_numvalue()
            if numberadd!=num:
                return False  #无法切换到指定数量
        if number>num:  #购买数量小于默认数量
            return False #无法切换到小于起购数
        return self.goods_buyadd('',goodsbuy,goodsadd,mb)
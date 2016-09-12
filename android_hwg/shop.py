#coding=utf-8
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from base import buy_login,swipeToUp,home_back

class Shop(object):
    def __init__(self,browser):
        self.browser=browser

    def __dir__(self):
        return ['goods_max','goods_min','goods_change','goods_buyadd']

    def goods_page(self,name):#android通过商品名称搜索定位
        if name=='':
            return False
        self.browser.implicitly_wait(30)
        try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/detail_cannel').click()
        except NoSuchElementException,e:
            pass
        self.browser.implicitly_wait(5)
        try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/bt_go_home').click()
        except NoSuchElementException,e:
            home_back(self.browser)
        else:pass
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_search').click()
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/search_edittext').send_keys(name)
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/search_cannel').click()
        try:gridview=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/default_textbutton')
        except NoSuchElementException,e:
            return False   #没有搜索到对应的商品
        else:
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/act_session_item_img').click()
            try:title=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_name').text
            except NoSuchElementException,e:
                return False  #未跳转到商品详情页
            else:
                if title==u'商品详情':
                    return True
                else:
                    return False


    def selected_show(self):
        element="browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_rule_name').click()"
        swipeToUp(self.browser,element,1000)


    def buy_click(self,mb):
        if mb==True:  #在规格面板点击立即购买
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/buy_now').click()
        else:   #在商品详情页点击立即购买
            try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/detail_cannel').click()
            except WebDriverException,e:
                pass
            self.browser.implicitly_wait(5)
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/buy_now').click()

    def add_click(self,mb):
        if mb==True:  #在规格面板点击加入购物车
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/shop_dedail_addcar').click()
            try: self.browser.find_element_by_id('com.hnmall.haiwaigou:id/shop_dedail_carnum')
            except NoSuchElementException.e:
                return False
            else:
                return True
        else:   #在商品详情页点击加入购物车
            try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/bottom_layout')
            except NoSuchElementException,e:
                try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/detail_cannel').click()
                except WebDriverException,e:
                    pass
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/shop_dedail_addcar').click()
            return  True

    def goods_buyadd(self,name='',goodsbuy=False,goodsadd=False,mb=False):
        if str(goodsbuy).lower()=='false':goodsbuy=False
        if str(goodsbuy).lower()=='true':goodsbuy=True
        if str(goodsadd).lower()=='false':goodsadd=False
        if str(goodsadd).lower()=='true':goodsadd=True    
        if str(mb).lower()=='false':mb=False
        if str(mb).lower()=='true':mb=True
        if name!='':
            if not self.goods_page(name): 
                return False #打开商品详情页失败，直接退出  
            if mb==True:
                self.selected_show()
        if goodsbuy==False and goodsadd==False:  #不点击立即购买、加入购物车按钮
            try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/detail_cannel')
            except NoSuchElementException,e:
                return False
            else:
                return True
        if goodsbuy==True:
            self.buy_click(mb)
            if not buy_login(self.browser):
                return False
            if self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_name').text==u'提交订单':
                return True
            else:
                return False
        elif goodsadd==True:
            if not self.add_click(mb):
                return False
            else:
                return True
        else:
            return False       


    def goods_inver(self,number,diradd):
        num_old=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/edittext_num').text
        num_old=int(num_old)
        while True:
            if diradd=='add':
                if number!='max' and num_old>=number:
                    return num_old
                self.browser.find_element_by_id('com.hnmall.haiwaigou:id/text_num_add').click()
            elif diradd=='reduce':
                if number!='min' and num_old<=number:
                    return num_old
                self.browser.find_element_by_id('com.hnmall.haiwaigou:id/text_num_subtract').click()
            else:
                pass  
            num_new=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/edittext_num').text
            num_new=int(num_new)
            if num_old==num_new:
                return num_old   #通过比对前后2次点击的商品数量是否一致，判断按钮是否可以继续点击
            num_old=num_new

    def change_spec(self,spec):
        flag=0
        spec_list=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/tag')
        for spec_i in spec_list:
            if spec_i.text==spec:
                spec_i.click()
                flag=1
                break
        if flag==0:
            swipeToUp(self.browser,'',1000)
            self.change_spec(spec)


    def goods_change(self,name,spec,num,goodsbuy=False,goodsadd=False,mb=False):
        if not self.goods_page(name): 
            return False #打开商品详情页失败，直接退出
        self.selected_show()
        if spec!='':  #更新为其他规格，一定是其他规格，否则会出错，若spec=='',表示不更新规格
            self.change_spec(spec)
        element="browser.find_element_by_id('com.hnmall.haiwaigou:id/text_num_add')"
        swipeToUp(self.browser,element,1000)
        number=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/edittext_num').text
        number=int(number)
        num=int(num)  
        if number<num:  #购买数量大于默认数量，点击加处理
            numberadd=self.goods_inver(num,'add')
            if numberadd!=num:
                return False  #无法切换到指定数量
        if number>num:  #购买数量小于默认数量
            return False #无法切换到小于起购数
        return self.goods_buyadd('',goodsbuy,goodsadd,mb)

    def goods_max_min(self,name,num,typemn='',goodsbuy=False,goodsadd=False,mb=False):
        if not self.goods_page(name):
            return False
        self.selected_show()
        element="browser.find_element_by_id('com.hnmall.haiwaigou:id/text_num_add')"
        swipeToUp(self.browser,element,1000)
        num=int(num)
        diradd=''
        if typemn=='max':
            diradd='add'
        else: #typemn='min'
            diradd='reduce'
        number=self.goods_inver(typemn,diradd)
        if number!=num:
            return False  #购买的数量与用例要求不一致
        else:
            return self.goods_buyadd('',goodsbuy,goodsadd,mb)

    def goods_max(self,name,num,goodsbuy=False,goodsadd=False,mb=False):
        return self.goods_max_min(name,num,'max',goodsbuy,goodsadd,mb)

    def goods_min(self,name,num,goodsbuy=False,goodsadd=False,mb=False):
        return self.goods_max_min(name,num,'min',goodsbuy,goodsadd,mb)







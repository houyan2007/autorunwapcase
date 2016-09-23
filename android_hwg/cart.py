#coding=utf-8
from selenium.common.exceptions import NoSuchElementException
from base import BaseHWG
from android_hwg import shop

class Cart(BaseHWG):
    def __init__(self,browser):
        super(Cart,self).__init__(browser)
        self.browser=browser
        self.cart_page()

    def __dir__(self):
        return ['cart_delete','cart_numchange','cart_submit']

    def cart_page(self):
        self.browser.implicitly_wait(30)
        self.home_back(BaseHWG.PageFlag)
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/index_production').click()
        BaseHWG.PageFlag='cart'

    def cart_delete(self,*names):
        names=list(names)
        names_len=len(names)
        if names_len==0:
            self.cart_delete_all()
            return True
        else:
            self.cart_delete_by_name(names)
            return True

    def cart_delete_all(self):
        while True:
            try:goods=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_product_name')
            except NoSuchElementException,e:
                break
            goods_pos=goods.location_in_view   #eg:{u'y': 506, u'x': 406}
            x_pos=goods_pos[u'x']
            y_pos=goods_pos[u'y']
            self.browser.tap([(x_pos,y_pos)],1000)
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/positiveButton').click()        


    def cart_delete_by_name(self,*name):
        names=name[0]
        while True:
            goods=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/tv_product_name')
            if len(goods)==0:
                break
            del_flag=0
            name_len=len(names)
            goods.reverse()
            for good in goods:
                if name_len>0 and good.text not in names:
                    continue
                else:
                    good_pos=good.location_in_view   #eg:{u'y': 506, u'x': 406}
                    x_pos=good_pos[u'x']
                    y_pos=good_pos[u'y']
                    self.browser.tap([(x_pos,y_pos)],1000)
                    self.browser.find_element_by_id('com.hnmall.haiwaigou:id/positiveButton').click()
                    del_flag=del_flag+1
            if del_flag==0:
                goods_old=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/tv_product_name')[-1].text
                self.swipeToUp('',1000)
                self.swipeToUp('',1000)
                try:goods_new=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/tv_product_name')[-1].text
                except NoSuchElementException,e:
                    self.swipeToUp('',1000)
                    goods_new=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/tv_product_name')[-1].text
                if goods_old==goods_new:   #滑动到页面底部
                    break

    def cart_findgoods(self,name):
        try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/el_shop_car')
        except NoSuchElementException,e:
            return False   #购物车列表为空
        while True:
            goods_all=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/ll_child_all')
            goods=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/tv_product_name')
            if len(goods)==0:
                return False
            for i,good in enumerate(goods):
                if name in good.text:
                    return goods_all[i]
                else:
                    continue
            goods_old=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/tv_product_name')[-1].text
            self.swipeToUp('',1000)
            self.swipeToUp('',1000)
            self.browser.implicitly_wait(5)
            try:
                goods_new=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/tv_product_name')[-1].text
            except NoSuchElementException,e:
                self.swipeToUp('',1000)
                goods_new=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/tv_product_name')[-1].text
            if goods_old==goods_new:   #滑动到页面底部
                return False    


    def cart_shop(self,name):
        goods=self.cart_findgoods(name)
        if not goods:#购物车列表无该商品，则新增该商品到购物车
            goods_object=shop.Shop(self.browser)
            if not goods_object.goods_buyadd(name,False,True,False):
                return False   #商品添加到购物车失败，直接退出
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/bottom_layout').click()
            BaseHWG.PageFlag='cart'
            return self.cart_findgoods(name)
        else:
            BaseHWG.PageFlag='cart'
            return goods


    def  cart_numclick(self,goods,num,ntype=''):
        if ntype.lower() not in ['max','min','']:
            return False
        goods_qty=goods.find_element_by_id('com.hnmall.haiwaigou:id/edittext_num').text
        goods_qty=int(goods_qty)
        if goods_qty==num:
            return True
        if ntype.lower()=='max' or goods_qty<num:  #购物车设置为最大数量，或增加购物车到指定数量
            goods.find_element_by_id('com.hnmall.haiwaigou:id/text_num_add').click()
            num_new=goods.find_element_by_id('com.hnmall.haiwaigou:id/edittext_num').text
            if int(num_new)==goods_qty:
                return False
            else:
                self.cart_numclick(goods,num,ntype)
        elif ntype.lower()=='min' or goods_qty>num:  #购物车设置为最小数量，或减少购物车到指定数量
            goods.find_element_by_id('com.hnmall.haiwaigou:id/text_num_subtract').click()
            num_new=goods.find_element_by_id('com.hnmall.haiwaigou:id/edittext_num').text
            if int(num_new)==goods_qty:
                return False
            else: 
                self.cart_numclick(goods,num,ntype)


    def cart_numchange(self,name,num,ntype=''):  #购物车可以设置商品到最大、最小、指定数量   
        num=int(num)
        if num==0:
            return False   #用例错误
        goods=self.cart_shop(name)   
        if goods==False:
            return False
        self.cart_numclick(goods,num,ntype)  
        goods_qty=goods.find_element_by_id('com.hnmall.haiwaigou:id/edittext_num').text  
        goods_qty=int(goods_qty)
        if goods_qty==num:

            return True
        else:
            return False 

    def goods_pay(self,goods):
        while True:
            try:
                pay_btn=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_pay')
            except NoSuchElementException,e:
                element="self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_pay')"
                self.swipeToUp(element,1000)
            else:
                pay_pos=pay_btn.location_in_view
                pay_y=pay_pos[u'y']
                pay_x=pay_pos[u'x']
                try:
                    goods_pos=goods.location_in_view
                    goods_y=goods_pos[u'y']
                except NoSuchElementException,e:
                    return pay_x,pay_y
                if pay_y>goods_y:   #结算按钮在商品名称下面
                    return pay_x,pay_y
                else:
                    element="self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_pay')"
                    self.swipeToUp(element,1000)

    def cart_submit(self,name):#点击包含某商品对应的结算按钮
        goods=self.cart_shop(name)
        if goods==False:
            return False
        '''if not self.cart_numchange(self,name,num):
            return False'''
        pay_x,pay_y=self.goods_pay(goods)    #商品对应的结算按钮左上角坐标
        self.browser.tap([(pay_x,pay_y)],0)
        try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/et_username')
        except NoSuchElementException,e:
            pass
        else:
            login_result=self.buy_login()
            if login_result==False:#判断是否进入登录界面
                return False
            else:
                pay_x,pay_y=self.goods_pay(goods)
                self.browser.tap([(pay_x,pay_y)],0)                
        self.browser.implicitly_wait(5)
        if self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_name').text==u'提交订单':
            BaseHWG.PageFlag='cart2order'
            return True
        else:
            return False

    def cart_samesubmit(self,*names):
        goods_first=names[0]
        pos_first=self.goods_pay(goods_first)
        for i in names[1:]:
            pos_i=self.goods_pay(i)
            if pos_i!=pos_first:
                return False
        return True
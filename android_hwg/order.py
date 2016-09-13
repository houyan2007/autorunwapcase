#coding=utf-8
from selenium.common.exceptions import NoSuchElementException
from android_hwg import shop,cart
from base import swipeToUp
import time

class Order(object):
    def __init__(self,browser):
        self.browser=browser

    def order_one(self,name,num):  #跳转到提交订单页面
        num=int(num)
        if num<=0:
            return False 
        goods=shop.Shop(self.browser)
        if num==1:
            return goods.goods_buyadd(name,goodsbuy=True,goodsadd=False,mb=False)
        else:
            return goods.goods_change(name,'',num,goodsbuy=True,goodsadd=False,mb=False)

    def order_more(self,*namenum):# eg *sps=[S644000000223,3],[S644000000223,3] #通过购物车结算按钮进入提交订单页面
        goodsnum=len(namenum)
        if goodsnum==0:
            return False
        elif goodsnum==1:
            return self.order_one(namenum[0],namenum[1])
        else:
            goods=cart.Cart(self.browser)
            for goods_name,goods_num in namenum:
                if not cart_numchange(goods_name,goods_num):
                    return False   #若出现加入购物车失败时
            goods_names=[names[0] for names in namenum]
            if not goods.cart_samesubmit(goods_names):
                return False    #不在同一个结算模块
            return goods.cart_submit(goods_names[0])

    def order_add_addr(self,name,idcard,mobile,province,city,district,addr):
        try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/ll_select_address').click()
        except NoSuchElementException,e:
            try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/ll_add_new_address').click()  #判断若账号下无地址时
            except NoSuchElementException,e:
                return False
        else:
            try:self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_add_new_address').click()
            except NoSuchElementException,e:
                return False
        try:
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/et_address_name').send_keys(name)
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/et_address_card').send_keys(idcard)
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/et_address_number').send_keys(mobile)
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_add_address').send_keys('')
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/province').send_keys(province)
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/city').send_keys(city)
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/couny').send_keys(district)
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/citypicker_confirm').click()
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/et_address_detail_address').send_keys(addr)
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_search').click()
            title=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_name').text
        except NoSuchElementException,e:
            return False
        if title!=u'选择收货地址':
            return False
        return self.order_change_addr('max')


    def order_change_addr(self,num):#目前只支持切换到最后那个地址
        if num!='max':
            num=int(num)
        if num==0:
            return False
        try:element=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/iv_address_selected')
        except NoSuchElementException,e:
            return False   #地址列表为空
        while True:
            sel_old=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/iv_address_selected')[-1]
            sel_old_pos=sel_old.location_in_view
            swipeToUp(self.browser,'',1000)
            time.sleep(1)
            sel_new=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/iv_address_selected')[-1]
            sel_new_pos=sel_new.location_in_view
            if sel_old_pos==sel_new_pos:
                sel_new.click()
                return True

    def order_coupon_has(self):
        element='browser.find_element_by_id("com.hnmall.haiwaigou:id/tv_discount_name")'
        swipeToUp(self.browser,element,1000)
        elem_discount=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_discount_name')
        if elem_discount.text==u'可用优惠券0张':
            elem_discount.click()
            elem_coupon=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_coupon_text')
            if u'没有'in elem_coupon.text:     # ==u'你目前没有可用的优惠券哟~':
                self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_back').click()
                return False
        else:
            return True

    def order_coupon_change(self,num):#目前支持第1屏幕的优惠券直接的切换
        num=int(num)
        if num==0:
            return False
        if not self.order_coupon_has():
            return False
        if num==1:
            return True
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/tv_discount_name').click()
        elem_bgs=self.browser.find_elements_by_id('com.hnmall.haiwaigou:id/tv_discount_plant')
        flag=0
        if num>len(elem_bgs):
            return False  #待切换的优惠券不在第1屏幕或者大于优惠券总数
        for elem_bg in elem_bgs:
            flag=flag+1
            if flag==num:
                elem_bg.click()
                title=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_name').text
                if title==u'提交订单':
                    return True
                else:
                    return False                
        if flag<num:   #优惠券数量小于Num
            self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_back').click()
            return False   

    def order_confirm(self):
        self.browser.find_element_by_id('com.hnmall.haiwaigou:id/commit_order_button').click()
        title=self.browser.find_element_by_id('com.hnmall.haiwaigou:id/title_name').text
        if title==u'支付方式':
            return True
        else:
            return False







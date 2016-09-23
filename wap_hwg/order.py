#coding:utf-8
from selenium.common.exceptions import NoSuchElementException
from wap_hwg import shop,cart
from base import BaseHWG

class Order(BaseHWG):
    def __init__(self,browser):
        super(Order,self).__init__(browser)
        self.browser=browser

    def __dir__(self):
        return ['order_one','order_more','order_add_addr','order_change_addr','order_coupon_change','order_confirm']

    def order_one(self,sp,num):  #只针对从商品详情页点击立即购买到提交订单页面
        shopobj=shop.Shop(self.browser)
        num=int(num)
        if num<=0:
            return False 
        return shopobj.goods_change(sp,'',num,True,False,True)  #已经进入了提交订单页面


    def order_more(self,*spsnum): # eg *sps=[S644000000223,3],[S644000000223,3] #通过购物车结算按钮进入提交订单页面
        goodsnum=len(spsnum)
        if goodsnum==0:
            return False
        elif goodsnum==1:
            return self.order_one(spsnum[0][0],spsnum[0][1])
        else:
            sps=[sp[0] for sp in spsnum]
            nums=[int(sp[1]) for sp in spsnum]
            cartobj=cart.Cart(self.browser)
            for i in range(goodsnum):
                if not cartobj.cart_numchange(sps[i],nums[i]):
                    return False  #加入购物车失败
            if not cartobj.cart_samesubmit(sps):
                return False
            cartobj.cart_submit(sps[-1])  #点击结算按钮，进入提交订单页面
            return True

    def order_add_addr(self,name,idcard,mobile,province,city,district,addr):#添加新地址,最后切换到地址列表
        noreceive='body > div.box > div.order_left > div > div.order-time.noReceive > span'
        try:self.browser.find_element_by_css_selector(noreceive).click()
        except NoSuchElementException,e:
            try:self.browser.find_element_by_class_name('order-icpe').click()
            except NoSuchElementException,e:
                return False
            else:
                self.browser.find_element_by_link_text(u'添加新地址').click()
                try:self.browser.find_element_by_id('SD_window')
                except NoSuchElementException,e:
                    pass  
                else:
                    return False  #已经有10个地址了，无法新增地址
        self.browser.find_element_by_id('recvLinkman').send_keys(name)
        self.browser.find_element_by_id('idCard').send_keys(idcard)
        self.browser.find_element_by_id('recvMobile').send_keys(mobile)
        self.browser.find_element_by_id('provinceCode').send_keys(province)
        self.browser.find_element_by_id('cityCode').send_keys(city)
        self.browser.find_element_by_id('districtCode').send_keys(district)
        self.browser.find_element_by_id('address').send_keys(addr)
        self.browser.find_element_by_link_text(u'保存').click()
        try:tip=self.browser.find_element_by_css_selector('#SD_window > div > div > em')       
        except NoSuchElementException,e:
            return False   
        else:
            if u'成功' in tip.text:
                return self.order_change_addr('max')   #切换地址为新增地址
            else:
                return False


    def order_change_addr(self,num):  #切换到指定顺序的地址，从1开始指定，最后切换回提交订单页面
        self.browser.implicitly_wait(5)
        try:self.browser.find_element_by_class_name('orderConfirm')
        except NoSuchElementException,e:
            pass
        else:
            return True  #提交订单页面无默认地址时，点击保存直接返回提交订单页面
        try:addr_list=self.browser.find_elements_by_class_name('order-time')
        except NoSuchElementException,e:
            return False   
        addr_len=len(addr_list)
        element=None
        if num=='max':
            element=addr_list[addr_len-1]
        else:
            num=int(num)
            if num>addr_len:
                return False  #地址列表小于指定数字的地址
            element=addr_list[num-1]
        addr_value=element.find_element_by_name('sel_cartgoods_1[]').get_attribute('value')
        element.find_element_by_class_name('checkboxRed').click()
        addr_select=self.browser.find_element_by_css_selector(
            'body > div.box > div.order_left > div > div.order-time > span > i').get_attribute('onclick')
        addr_int=addr_select.find('(')
        addr_select=addr_select[addr_int+1:-2]
        if addr_value!=addr_select:  
            return False
        return True

    def order_coupon_has(self): #判断是否有可用优惠券
        try:self.browser.find_element_by_id('_show_coupon_name')
        except NoSuchElementException,e:
            return False
        else:
            return True

    def order_coupon_back(self):
        titles=self.browser.find_elements_by_class_name('title')
        for coupon_title in titles:
            if coupon_title.text==u'选择优惠券':
                header=coupon_title.find_element_by_xpath('..')
                header.find_element_by_class_name('backArrow').click()
                break

    def order_coupon_change(self,num):  #切换优惠券选择,最后切换回提交订单列表
        '''
        num=0:表述不选择优惠券，取消默认优惠券使用
        num>0:表述选择排序为num的优惠券
        '''
        if not self.order_coupon_has():
            return False  #没有优惠券可切换
        self.browser.find_element_by_id('_show_coupon_name').click()  #进入优惠券列表
        num=int(num)
        parent=self.browser.find_element_by_class_name('list_youa')
        if num==0:
            coupon_hover=parent.find_element_by_css_selector('div.coupon.haitao.hover')
            coupon_hover.find_element_by_class_name('selected').click()
            self.order_coupon_back()
            return True
        elif num==1:
            self.order_coupon_back()
            return True           
        else:
            try:
                coupon_nohover=parent.find_elements_by_css_selector('div.coupon.haitao')
            except NoSuchElementException,e:
                pass
            else:
                coupon_len=len(coupon_nohover)
                if num>coupon_len:
                    self.order_coupon_back()
                    return False  #要求的优惠券排序不存在
                else:
                    #parent=self.browser.find_element_by_class_name('list_youa')
                    #child=parent.find_element_by_css_selector('div:nth-child(%d)' % num)
                    child=coupon_nohover[num-1]
                    if child.get_attribute('class')=='coupon haitao hover':
                        self.order_coupon_back()
                        return True  #默认选中的优惠券与指定的优惠券一致
                    else:
                        child.click()
                        self.order_coupon_back()
                        return True

    def order_confirm(self):
        self.browser.find_element_by_class_name('confirm_btn').click()  #点击提交订单按钮
        self.browser.implicitly_wait(5)
        try:self.browser.find_element_by_class_name('pay_amount')
        except NoSuchElementException,e:
            return False
        else:
            return True

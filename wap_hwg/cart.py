#coding:utf-8
from selenium.common.exceptions import NoSuchElementException
from wap_hwg import shop
from base import BaseHWG


class Cart(BaseHWG):#基于登录后
    def __init__(self,browser):
        super(Cart,self).__init__(browser)
        self.browser=browser
        self.cart_page()

    def __dir__(self):
        return ['cart_delete','cart_numchange','cart_submit']

    def cart_page(self):
        try:self.browser.find_element_by_id('a_cart').click()
        except NoSuchElementException,e:
            try:self.browser.find_element_by_link_text(u'购物车').click()
            except NoSuchElementException,e:
                self.browser.get(BaseHWG.HWG_HRL)
                self.cart_page()

    def cart_findgoods(self,sp):  #找到商品所在位置
        goods=self.browser.find_elements_by_class_name('J_moveRight') 
        if len(goods)==0:
            return False   
        for good in goods:
            if good.get_attribute('ccode').lower()==sp.lower():
                return good
        return False

    def cart_delete(self,*sp):
        try: self.browser.find_element_by_class_name('empty_btn')
        except NoSuchElementException,e:
            goods=self.browser.find_elements_by_class_name('shanchu') #找到所有的删除按钮
            goodslen=len(goods) 
            splen=len(sp)
            if splen==0:
                while goodslen:
                    try:
                        good=self.browser.find_element_by_class_name('shanchu')
                    except NoSuchElementException,e:
                        return True
                    good.click()
                    self.browser.find_element_by_id('SD_confirm').click()  
                    goodslen=goodslen-1             
                return True
            else:
                spflag=splen
                sp=[i.lower() for i in sp]
                while spflag>0:
                    goods=self.browser.find_elements_by_class_name('shanchu') 
                    goodslen=len(goods)
                    goodsflag=0
                    for good in goods:            
                        if good.get_attribute('ccode').lower() in sp:
                            spflag=spflag-1
                            good.click()
                            self.browser.find_element_by_id('SD_confirm').click() 
                            break
                        goodsflag=goodsflag+1
                    if goodsflag==goodslen:
                        break
                return True
        return True


    def cart_numclick(self,goods,num,ntype=''): 
        if ntype.lower() not in ['max','min','']:
            return False
        goods_qty=goods.find_element_by_id('prod_qty').get_attribute('value')
        goods_qty=int(goods_qty)
        if goods_qty==num:
            return True
        if ntype.lower()=='max' or goods_qty<num:  #购物车设置为最大数量，或增加购物车到指定数量
            try: goods.find_element_by_css_selector(
                'div:nth-child(2) > div.gd_info > div > a.J_add.add.y_hover.reduce.J_ytag.btn_disabled')
            except NoSuchElementException,e:
                goods.find_element_by_css_selector(
                    'div:nth-child(2) > div.gd_info > div > a.J_add.add.y_hover.reduce.J_ytag').click()
                self.cart_numclick(goods,num,ntype)
        elif ntype.lower()=='min' or goods_qty>num:  #购物车设置为最小数量，或减少购物车到指定数量
            try: goods.find_element_by_css_selector(
                'div:nth-child(2) > div.gd_info > div > a.J_reduce.add.y_hover.J_ytag.btn_disabled')
            except NoSuchElementException,e:
                goods.find_element_by_css_selector(
                    'div:nth-child(2) > div.gd_info > div > a.J_reduce.add.y_hover.J_ytag').click()
                self.cart_numclick(goods,num,ntype)
          

    
    def cart_shop(self,sp):  #添加某商品到购物车列表
        if not self.cart_findgoods(sp):  #购物车列表无该商品，则新增该商品到购物车
            goods_object=shop.Shop(self.browser)
            if not goods_object.goods_buyadd(sp,False,True,False):
                return False   #商品添加到购物车失败，直接退出
            self.browser.find_element_by_id('productCount').click()
        return self.cart_findgoods(sp)       


    def cart_numchange(self,sp,num,ntype=''):  #购物车可以设置商品到最大、最小、指定数量
        num=int(num)
        if num==0:
            return False  #用例错误
        goods=self.cart_shop(sp)
        if goods==False:
            return False
        self.cart_numclick(goods,num,ntype)
        self.browser.find_element_by_id('a_cart').click()
        goods_new=self.cart_findgoods(sp)
        goods_qty=goods_new.find_element_by_id('prod_qty').get_attribute('value')
        goods_qty=int(goods_qty)
        if goods_qty==num:
            return True
        else:
            return False 

    def cart_submit(self,sp):#点击包含某商品对应的结算按钮
        goods=self.cart_shop(sp)
        if goods==False:
            return False
        '''if not self.cart_numchange(self,sp,num):
            return False'''
        submit_parent=goods.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
        submit_btn=submit_parent.find_element_by_id('selcart_submit_1')
        if submit_btn.get_attribute('class')=='btn_buy unable_buy':
            return False  #结算按钮是灰色的，直接退出
        else:
            self.scroll(submit_btn)
            submit_btn.click()
        login_result=self.buy_login()
        if login_result==False:#判断是否进入登录界面
            return False
        elif login_result==2:
            self.cart_submit(sp)
        else:
            pass
        self.browser.implicitly_wait(5)
        try:self.browser.find_element_by_class_name('orderConfirm')
        except NoSuchElementException,e:
            return False
        return True


    def cart_samesubmit(self,*sps):#判断给出的商品是否属于同一个结算单元，前提：商品都已经在购物车列表中了
        if len(sps)==0:
            return False
        if len(sps)==1:
            return True
        list_id=[]
        for sp in sps:       
            goods=self.cart_findgoods(sp)
            parent_id=goods.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').get_attribute('id')
            pos_id=parent_id.find('-')
            parent_id=parent_id[pos_id+1:]
            list_id.append(parent_id)
        first_id=list_id[0]
        for i in list_id[1:]:
            if i!=first_id:
                return False
        return True
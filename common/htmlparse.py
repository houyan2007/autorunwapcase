
#-*- coding:utf-8 -*-
import requests

class HtmlParse(object):
    def __init__(self,url):
        self.url=url

    def htmlread(self):
        r = requests.get(self.url)
        codetype=r.encoding
        return r.text.encode(codetype)

    def find(self,text):
        htmltext=self.htmlread()
        if htmltext.find(text)>-1:
            return True
        else:
            return False


#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
def send_mail(file_new):
	mail_from='houyan2007@sina.com'
	mail_to='houyan@youayun.cn'
	f = open(file_new, 'rb')
	mail_body = f.read()
	f.close()
	msg=MIMEText(mail_body,_subtype='html',_charset='utf-8')
	msg['Subject']=u"WEB端用例测试报告"
	msg['date']=time.strftime("%a,%d %b %Y %H:%M:%S %z")
	smtp=smtplib.SMTP()
	smtp.connect('smtp.sina.com')
	smtp.login('houyan2007@sina.com','VinceyHY0916')#vpkliwatxxfgbihh
	smtp.sendmail(mail_from,mail_to,msg.as_string())
	smtp.quit()

def sendreport():
	lists=os.listdir(REPORT_DIR)
	lists.sort(key=lambda fn: os.path.getmtime(REPORT_DIR+"\\"+fn) if not os.path.isdir(REPORT_DIR+"\\"+fn) else 0)
	file_new = os.path.join(REPORT_DIR,lists[-1])
	send_mail(file_new)

if __name__=='__main__':
    print 'No main file'
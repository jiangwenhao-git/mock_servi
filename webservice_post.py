# -*- coding: utf-8 -*-
import httplib2

#本模块是模拟发送soap报文的功能



def mdsmssend():
  #定义发送报文
   file_content = open('./request/UsLmtChg_req.xml')
   try:
    SoapMessage = file_content.read()
   finally:
    file_content.close()

   webservice = httplib2.Http('.cache')
   #连接到服务器后的第一个调用。它发送由request字符串到到服务器
   response,content = webservice.request("http://127.0.0.1:9001/services/" , "POST",SoapMessage, headers={'Content-Type': 'application/x-www-form-urlencoded'})
   print("content :",content.decode('utf-8'))
   print("res ：",response)

if __name__ == '__main__':
 mdsmssend()
import xmltodict

# 根据tagfile文件递归生成字典
def fun(list_tmp,n,i=0,dict1={}):
    if i == n-1:
        dict1[list_tmp[i]] = list_tmp[i+1:]
    if i < n -1:
        dict1[list_tmp[i]] = fun(n,i+1,dict1={})
    return dict1

# 处理返回报文的函数
filepath = './UsLmtChg.xml'
# recod = []
# def file_handler(mockfile):
#     with open(filepath,'r',encoding='utf8') as f:
#         if not f:
#             recod['Error_msg'] = '文件读取异常'
#         else:
#             for line in f.readline():
#                 list_dir = line.split(' ')[0]
#                 list_value = line.split(' ')[1]
#                 # line_dict = fun(list_tmp, len(list_tmp)-1)
#                 # 如何通过上面的字典串递归找到soap报文里面的数据，
#                 # 并通过字典中的数据替换掉soap报文中对应字段的数据
#                 file_dic = xmltodict.parse(mockfile)
#                 # line_dict.keys()
#                 for i in list_dir:
#                     file_dic = file_dic[i]
#
#                 # print("line_dict :",line_dict)
#
#
#     return None



def mock_handler(mockfile):
    file_dic = xmltodict.parse(mockfile)
    print('请输入返回码 ：')
    ReturnCode = input()
    print('请输入返回信息 ：')
    ReturnMsg = input()
    file_dic['soap:Envelope']['soap:Body']['s:RspUsLmtChg']['s:RspSvcHeader']['s:ReturnCode'] = ReturnCode
    print(str(file_dic['soap:Envelope']['soap:Body']['s:RspUsLmtChg']['s:RspSvcHeader']['s:ReturnCode']))
    file_dic['soap:Envelope']['soap:Body']['s:RspUsLmtChg']['s:RspSvcHeader']['s:ReturnMsg'] = ReturnMsg
    file_xml = xmltodict.unparse(file_dic)
    f = open(filepath,'w')
    f.write(file_xml)
    f.close()
    print("file_xml : ", f)

if __name__ == '__main__':
    file = open(filepath)
    mock_file = file.read()
    mock_handler(mock_file)
    file.close()

# from bs4 import BeautifulSoup
# import xml.etree.cElementTree as ET
# import xml
# file_content = open('UsLmtChg.xml')
# try:
#     SoapMessage = file_content.read()
# finally:
#     file_content.close()
#
# soup = BeautifulSoup(SoapMessage,"lxml")
# print(soup.s.)
# print(soup)
#
#




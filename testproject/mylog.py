#!/usr/bin/env python
# -*- coding: utf-8-*-
# @author: lifeng29@163.com


import os
import socket
import xmltodict
import requests
import time
import logging
from flask import g,Flask,render_template,request
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# 通过键值查询嵌套字典中的该键值value信息
def _finditem(obj,key):
	if key in obj:return obj[key]
	for k,v in obj.items():
		if isinstance(v,dict):
			item = _finditem(v,key)
			if item is not None:
				return item

# 将tag文件中数据转换为字典数据
def tag2dict(filepath):
	with open(filepath,'r',encoding='utf-8') as f:
		dic = []
		for line in f.readlines():
			line = line.strip('\n')
			b = line.split(' ')
			dic.append(b)
	dic = dict(dic)
	return dic

# 处理返回报文的函数
# 如何通过修改文件的方式来修改返回信息，拿UsLmtChg.xml做试点

# def mock_handler(mockfile):
# 	file_dic = xmltodict.parse(mockfile)
# 	ReturnCode = tag2dict('UsLmtChg.tag')['s:ReturnCode']
# 	print('从tag文件获取到的返回码 ：',ReturnCode)
# 	ReturnMsg = tag2dict('UsLmtChg.tag')['s:ReturnMsg']
# 	print('从tag文件获取到的返回信息 ：', ReturnMsg)
# 	file_dic = ReturnCode
# 	file_dic = ReturnMsg
# 	file_xml = xmltodict.unparse(file_dic)
# 	print("file_xml : ",file_xml)

#通过传入两个字典参数，修改挡板文件

# 把tag中解析的字典{key,value}数据,通过key索引，将value值替换到返回报文的xml文件中
def dispose_dict(input_parameter,fixed_parameter):
	for input_key, input_value in input_parameter.items():
		for fixed_key, fixed_value in fixed_parameter.items():
			if input_key == fixed_key:
				if isinstance(fixed_parameter[fixed_key],str):
					fixed_parameter[fixed_key] = input_value
					break
				elif isinstance(fixed_parameter[fixed_key],list):
					if len(fixed_parameter[fixed_key]) == 0:
						fixed_parameter[fixed_key].append(input_value)
						break
			elif isinstance(fixed_value, dict):
				if len(fixed_value) != 0:
					dispose_dict(input_parameter,fixed_value)
			elif isinstance(fixed_value, list):
				if len(fixed_value) != 0:
					if isinstance(fixed_value[0], dict):
						for kv1 in fixed_value:
							dispose_dict(input_parameter, kv1)

	return fixed_parameter

# mock数据的操作方法
def mock_handler(mockfile,xmlfilepath,tagfilepath):
	Returndicts = tag2dict(tagfilepath)
	file_dic = xmltodict.parse(mockfile)
	print("dispose_dict   :",dispose_dict(Returndicts, file_dic))
	print(file_dic)
	# for returndict in Returndicts.items():
	# 	dictobj = dispose_dict(returndict,file_dic)
	dictobjtoxml = xmltodict.unparse(file_dic)
	# 将修改后的文件写回原文件中
	f = open(xmlfilepath,'w')
	f.write(dictobjtoxml)
	print("字典转化为xml文件 ：",dictobjtoxml)
	f.close()


@app.route('/services/', methods=['GET','POST'])
def services():

	#返回控制台mock的链接
	# print("mock地址为: ", request.base_url)
	g.base_url = request.base_url
	print("mockg地址为: ", g.base_url)
	logging.basicConfig(level=logging.DEBUG, filename='mockurl.log', filemode='a')
	# logging.info(request.base_url)
	logging.info(g.base_url)
	if request.method == 'POST':
		req = request.get_data()
		try:
			req_dic = xmltodict.parse(req)
			print("req_data   :",req_dic)
			action = req_dic['soap:Envelope']['soap:Header']['s:ReqHeader']['d:ServiceAction']
			action = action[5:]
			print("action :", action)
			serverid = req_dic['soap:Envelope']['soap:Header']['s:ReqHeader']['d:ServiceAdr']
			serverid = serverid.split('/')[-1]
		except Exception as ex:
			app.logger.warning('soap mock error:%s' % ex)
			# mock_count['Error'] += 1
			return render_template('MsgSendSvc.xml',serverid = serverid)
		# action 是字典要查找的键，如果查不到该键值，就返回‘Mock_default.xml’默认文件
		tplname = mock_cfg.get(action, 'Mock_default.xml')
		if tplname != 'Mock_default.xml':
			tagfilepath = './tag/' + str(action) + '.tag'		  #修改返回的xml报文的数据
			xmlfilepath = './templates/' + str(action) + '.xml'   #需要返回的xml报文
			mock_file = open(xmlfilepath).read()
			mock_handler(mock_file,xmlfilepath,tagfilepath)
			# mock_file.close()
			return render_template(tplname, serverid=serverid)
		else:
			app.logger.warning('template not find : %s' % action)
			return render_template(tplname, action=action, serverid=serverid)
	else:
		return 'ESB挡板运行中...'
		# return 'ESB挡板运行中：%s' % mock_count



if __name__ == '__main__':
	# 这里需要读取templates文件夹，看有哪些文件，形成下面的数据
	mock_cfg = {'MsgSendSvc': 'MsgSendSvc.xml', 'UsLmtChg': 'UsLmtChg.xml', 'LmtInfoQry': 'LmtInfoQry.xml'}
	mock_count = {'Error': 0}

	# 自定义日志对象
	logger = logging.getLogger("MYLOG")
	# 设置日志级别
	logger.setLevel(logging.DEBUG)
	# 设置日志的格式  asctime 时间   name 名字    levelname 日志级别  message 日志信息
	logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
	# 设置命令行输出
	sh = logging.StreamHandler()
	# 为命令行输出设置 显示格式
	sh.setFormatter(logging_format)
	# 将命令行输出这个操作添加到自定义日志中
	logger.addHandler(sh)
	# 定义文件记录日志配置
	fh = logging.FileHandler(filename='simu',encoding='utf-8')
	# 配置日志文件记录格式
	fh.setFormatter(logging_format)
	# 将文件记录配置存放到自定义logger 中
	app.logger.addHandler(fh)
	app.run('0.0.0.0', 9001, True, False)

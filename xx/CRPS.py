#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: lifeng29@163.com

import os

import copy
import traceback

import logzero
from logzero import logger as logz
import socket
import xmltodict
import threading


bind_ip = "0.0.0.0"
bind_port = 8816


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(50)

print("tcp mock listening on %s:%d" % (bind_ip, bind_port))

rsq_mb = """<?xml version="1.0" encoding="UTF-8"?>
<Message>
  <Head>
    <code>0</code>
    <desc>成功</desc>
  </Head>
  <Body>
    <data/>
  </Body>
</Message>
"""



def handle_client(client_socket):
    request = client_socket.recv(10240)
    logz.info("Received: %s" % request)
    rsp = ''
    try:
        req_xml = request.decode()
        print("req_xml",req_xml)

        xml_len = len(req_xml)
    except:
        rsp = 'input format error'
    if rsp == '':
        key_dic = {}
        try:
            req_dic = xmltodict.parse(req_xml)
            logz.info(req_dic)
            # head_dic = req_dic['Message']['Head']
            # Body_dic = req_dic['Message']['Body']
            #
            # key_dic['appkey'] = head_dic['appkey']
            # key_dic['biztype'] = head_dic['biztype']
            # key_dic['mobile'] = Body_dic['mobile']
            # key_dic['content'] = Body_dic['content']

            rsp_str = rsp_comp(key_dic)
        except:
            rsp_str = 'input xml format error'
    else:
        logz.info("req parse error ")
        rsp_str = rsp

    rsp_data = gen_rsp(rsp_str)
    client_socket.send(rsp_data)
    client_socket.close()

def rsp_comp(key_dic):
    '''
    rsp重组
    :param key_dic: 关键字段字典
    :return: rsp xml
    '''
    rsp_xml = ''
    try:
        mb_dic = xmltodict.parse(rsq_mb)
    except Exception as ex:
        logz.error('req mb tran dict error: %s' % traceback.format_exc())
        return rsp_xml

    return rsq_mb
    # return rsp_xml

def gen_rsp(rsp):
    rsp_enc = rsp.encode('utf8')
    return rsp_enc


while True:
    client, addr = server.accept()
    logz.info("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

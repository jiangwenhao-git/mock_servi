#!/usr/bin/env python
# -*- coding: utf-8-*-
# @author: lifeng29@163.com

import codecs
import datetime
import hashlib
import os
import random
import xml.dom.minidom as Dom

import logzero
from flask import *
from logzero import logger as logz

app = Flask(__name__)


class XMLGenerator:
    def __init__(self):
        self.doc = Dom.Document()

    def createNode(self, node_name):
        return self.doc.createElement(node_name)

    def addNode(self, node, prev_node=None):
        cur_node = node
        if prev_node is not None:
            prev_node.appendChild(cur_node)
        else:
            self.doc.appendChild(cur_node)
        return cur_node

    def setNodeAttr(self, node, att_name, value):
        cur_node = node
        cur_node.setAttribute(att_name, value)

    def setNodeValue(self, cur_node, value):
        node_data = self.doc.createTextNode(value)
        cur_node.appendChild(node_data)

    def genXml(self):
        xml = self.doc.toprettyxml(indent="\t", newl="\n", encoding="UTF-8")
        return xml.decode('utf8')


def md5_func(enc_str):
    md5 = hashlib.md5()
    md5.update(enc_str.encode('utf8'))
    md5_str = md5.hexdigest().upper()
    return md5_str


# bank_fund_no=95040000000114829&input_charset=GBK&modify_time=20190730170333&partner=1300090064&retcode=0000&retmsg=成功&service_version=1.0&sign_key_index=1&sign_type=MD5&sp_trans_id=10999000000745500
def raw_enc_str(rsp_dic):
    sort_list = sorted(rsp_dic.items(), key=lambda x: x[0])
    sort_str = ''
    for index, tup1 in enumerate(sort_list, 1):
        if len(tup1[1]) and len(sort_list) != index:
            key_str = tup1[0] + "=" + tup1[1] + '&'
            sort_str += key_str
        elif len(tup1[1]) and len(sort_list) == index:
            key_str = tup1[0] + "=" + tup1[1]
            sort_str += key_str

    fund_key = '1234a013a8b515349c307f1e448ce836'
    enc_str = sort_str + '&key=' + fund_key

    return enc_str


@app.route('/REST/<tran_type>', methods=['GET', 'POST'])
def services(tran_type):
    print("mock地址为: ", request.base_url)
    if request.method == 'POST':
        # 解析共同参数
        input_charset = request.form.get('input_charset')
        sign_key_index = request.form.get('sign_key_index')
        sign_type = request.form.get('sign_type')
        service_version = request.form.get('service_version')
        rsp_dic = {}
        rsp_dic['retcode'] = '0000'
        rsp_dic['attach'] = ''
        rsp_dic['sp_trans_id'] = '10999000000' + str(random.randrange(100000, 999999))
        rsp_dic['input_charset'] = 'UTF-8'
        rsp_dic['sign_key_index'] = sign_key_index
        rsp_dic['sign_type'] = sign_type
        rsp_dic['service_version'] = service_version

        # 设置xml数据
        myXML = XMLGenerator()
        node_root = myXML.createNode("root")
        myXML.addNode(node=node_root)

        if tran_type == 'pfb-ta-open':
            logz.warning('--pfb-ta-open start--')
            partner = request.form.get('partner')
            rsp_dic['partner'] = partner
            bank_fund_no = request.form.get('bank_fund_no')
            rsp_dic['bank_fund_no'] = bank_fund_no
            rsp_dic['retmsg'] = '成功'
            modify_time = request.form.get('acc_time')
            rsp_dic['modify_time'] = modify_time
            # 字段排序 str
            enc_str = raw_enc_str(rsp_dic)
            # ms5 加密
            md5_str = md5_func(enc_str)
            logz.warning('md5_str:%s' % md5_str)
            logz.warning('raw_sorted_str:%s' % enc_str)
            # 新xml attach node
            node_attach = myXML.createNode("attach")
            myXML.addNode(node_attach, node_root)
            myXML.setNodeValue(node_attach, '')

            node_bank_fund_no = myXML.createNode("bank_fund_no")
            myXML.addNode(node_bank_fund_no, node_root)
            myXML.setNodeValue(node_bank_fund_no, bank_fund_no)

            node_bank_input_charset = myXML.createNode("input_charset")
            myXML.addNode(node_bank_input_charset, node_root)
            myXML.setNodeValue(node_bank_input_charset, rsp_dic['input_charset'])

            node_modify_time = myXML.createNode("modify_time")
            myXML.addNode(node_modify_time, node_root)
            myXML.setNodeValue(node_modify_time, modify_time)

            node_partner = myXML.createNode("partner")
            myXML.addNode(node_partner, node_root)
            myXML.setNodeValue(node_partner, partner)

            node_retcode = myXML.createNode("retcode")
            myXML.addNode(node_retcode, node_root)
            myXML.setNodeValue(node_retcode, rsp_dic['retcode'])

            node_retmsg = myXML.createNode("retmsg")
            myXML.addNode(node_retmsg, node_root)
            myXML.setNodeValue(node_retmsg, rsp_dic['retmsg'])

            node_version = myXML.createNode("service_version")
            myXML.addNode(node_version, node_root)
            myXML.setNodeValue(node_version, service_version)

            node_sign = myXML.createNode("sign")
            myXML.addNode(node_sign, node_root)
            myXML.setNodeValue(node_sign, md5_str)

            node_sign_key = myXML.createNode("sign_key_index")
            myXML.addNode(node_sign_key, node_root)
            myXML.setNodeValue(node_sign_key, sign_key_index)

            node_sign_type = myXML.createNode("sign_type")
            myXML.addNode(node_sign_type, node_root)
            myXML.setNodeValue(node_sign_type, sign_type)

            # 基金账号
            node_trans_id = myXML.createNode("sp_trans_id")
            myXML.addNode(node_trans_id, node_root)
            myXML.setNodeValue(node_trans_id, rsp_dic['sp_trans_id'])

        else:
            logz.warning('--pfb-ta-close start--')
            # 解约操作
            channel_id = request.form.get('channel_id')
            # todo 获取实时时间
            modify_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            out_trade_no = '201201905300000000820'
            retmsg = '0000'
            sp_user = ''
            trade_status = '0'
            transaction_id = request.form.get('transaction_id')
            rsp_dic['modify_time'] = modify_time
            rsp_dic['out_trade_no'] = out_trade_no
            rsp_dic['retmsg'] = retmsg
            rsp_dic['sp_user'] = sp_user
            rsp_dic['trade_status'] = trade_status
            rsp_dic['transaction_id'] = transaction_id

            # 字段排序 str
            enc_str = raw_enc_str(rsp_dic)
            # ms5 加密
            md5_str = md5_func(enc_str)

            logz.warning('md5_str:%s' % md5_str)
            logz.warning('raw_sorted_str:%s' % enc_str)
            # 新xml attach node
            node_attach = myXML.createNode("attach")
            myXML.addNode(node_attach, node_root)
            myXML.setNodeValue(node_attach, '')

            node_channel_id = myXML.createNode("channel_id")
            myXML.addNode(node_channel_id, node_root)
            myXML.setNodeValue(node_channel_id, channel_id)

            node_input_charset = myXML.createNode("input_charset")
            myXML.addNode(node_input_charset, node_root)
            myXML.setNodeValue(node_input_charset, rsp_dic['input_charset'])

            node_modify_time = myXML.createNode("modify_time")
            myXML.addNode(node_modify_time, node_root)
            myXML.setNodeValue(node_modify_time, rsp_dic['modify_time'])

            node_out_trade_no = myXML.createNode("out_trade_no")
            myXML.addNode(node_out_trade_no, node_root)
            myXML.setNodeValue(node_out_trade_no, rsp_dic['out_trade_no'])

            node_retcode = myXML.createNode("retcode")
            myXML.addNode(node_retcode, node_root)
            myXML.setNodeValue(node_retcode, rsp_dic['retcode'])

            node_retmsg = myXML.createNode("retmsg")
            myXML.addNode(node_retmsg, node_root)
            myXML.setNodeValue(node_retmsg, rsp_dic['retmsg'])

            node_service_version = myXML.createNode("service_version")
            myXML.addNode(node_service_version, node_root)
            myXML.setNodeValue(node_service_version, rsp_dic['service_version'])

            node_sign = myXML.createNode("sign")
            myXML.addNode(node_sign, node_root)
            myXML.setNodeValue(node_sign, md5_str)

            node_channel_id = myXML.createNode("channel_id")
            myXML.addNode(node_channel_id, node_root)
            myXML.setNodeValue(node_channel_id, channel_id)

            node_sign_key_index = myXML.createNode("sign_key_index")
            myXML.addNode(node_sign_key_index, node_root)
            myXML.setNodeValue(node_sign_key_index, sign_key_index)

            node_sign_type = myXML.createNode("sign_type")
            myXML.addNode(node_sign_type, node_root)
            myXML.setNodeValue(node_sign_type, sign_type)

            node_sp_trans_id = myXML.createNode("sp_trans_id")
            myXML.addNode(node_sp_trans_id, node_root)
            myXML.setNodeValue(node_sp_trans_id, rsp_dic['sp_trans_id'])

            node_sp_user = myXML.createNode("sp_user")
            myXML.addNode(node_sp_user, node_root)
            myXML.setNodeValue(node_sp_user, sp_user)

            node_trade_status = myXML.createNode("trade_status")
            myXML.addNode(node_trade_status, node_root)
            myXML.setNodeValue(node_trade_status, trade_status)

            node_transaction_id = myXML.createNode("transaction_id")
            myXML.addNode(node_transaction_id, node_root)
            myXML.setNodeValue(node_transaction_id, transaction_id)

        xml_data = myXML.genXml()
        response = make_response(xml_data)
        response.headers['Content-Type'] = 'application/xml,charset=utf-8'
        return response
    else:
        return 'YJT挡板运行中...'
        # return 'YJT挡板运行中：%s' % mock_count



# if __name__ == '__main__':
#     # logger init
#     logzero.logfile(filename=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'yjt_mock.log'), maxBytes=10e6,
#                     backupCount=3, encoding='UTF-8',
#                     disableStderrLogger=True)
#     # mock count
#     mock_count = {'count': 0}
#     app.run(host='0.0.0.0', port=8228, debug=False)
#     logz.info('Running on http://0.0.0.0:8228/')
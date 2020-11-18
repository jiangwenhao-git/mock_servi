import esb_simu
import post_demo
import YJT_Mock
import os
import logging
import threading
import CRPS_mock
import logzero
from logzero import logger as logz
from flask import *

def soap_services_esb(host,port,threaded,debug):#这里的host,port是针对返回mock链接的构成数据，我也需要抓取传入的数据来进行匹配
    print("soap_service : esb_simu.py")
    # 需要放出一个参数入口出来，用于记录和分发挡板接口信息
    # 目前一个python控制，起不了多个服务，准备实现启动多个服务（ok），首先起了多个服务，才能实现分发机制
    # 创建另外一个挡板服务，用来测试挡板的分发机制（挡板已经开发好，用post_demo.py）(ok)
    # 需要匹配获取到的接口链接与mock生成的接口链接
    # 如何通过config文件将请求地址与mock地址一一映射，返回请求地址的mock地址（可以通过解析获取soap报文的地址信息来获取）
    # 构建真实的soap报文传递接口
    # 要不要写一个函数，用于记录mock地址信息，通过这个函数返回出去

    # 主要功能：服务一直启动着，监听到有向真实系统接口传递信息的action时，将判断（判断依据不清楚，是人工判断？）是否走真实系统
    # 还是走mock接口，如果走mock接口
    # 从ESB提前获取接口request报文放入文件夹中，取名XXX_req.xml，将从ESB中提前获取针对本次request报文的response报文反馈回去
    # 如何反馈？解析request报文中的交易码和action，读取到交易码数据，进行指定匹配。
    # 如何通过配置文件配置接口信息和挡板链接（是否有必要）
    # 如何通过动态修改返回文件

    handler = logging.FileHandler('simu.log', encoding='utf-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    esb_simu.app.run(host=host, port=port, threaded=threaded, debug=debug)

def soap_service_post(host,port,threaded,debug):
    print("http_service : post_demo.py")
    post_demo.app.run(host=host, port=port, threaded=threaded, debug=debug)


def soap_service_YJT(host,port,threaded,debug):
    print("soap_service : YJT_Mock.py")

    # logger init
    logzero.logfile(filename=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'yjt_mock.log'), maxBytes=10e6,
                    backupCount=3, encoding='UTF-8',
                    disableStderrLogger=True)
    logz.info('Running on http://0.0.0.0:8228/')
    YJT_Mock.app.run(host=host, port=port, threaded=threaded, debug=debug)

def sop_service_CRPS():
    print("sop_service : CRPS_mock.py")
    client, addr = CRPS_mock.server.accept()
    CRPS_mock.logz.info("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
    client_handler = threading.Thread(target=CRPS_mock.handle_client, args=(client,))
    client_handler.start()

threads = []

threads.append(threading.Thread(target=soap_services_esb,args=('0.0.0.0', 9001, True, False)))
threads.append(threading.Thread(target=soap_service_post,args=('0.0.0.0', 9002, True, False)))
threads.append(threading.Thread(target=soap_service_YJT,args=('0.0.0.0', 8228, True, False)))
threads.append(threading.Thread(target=sop_service_CRPS))

if __name__ =='__main__':
    for t in threads:
        # t.setDaemon(True)
        t.start()





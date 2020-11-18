import logging
#  配置日志级别为 debug  写入文件，文件权限为追加。
logging.basicConfig(level=logging.DEBUG,filename='example.log',filemode='a')

logging.debug("this is debug")
logging.info("this is info")
logging.warning("this is warning")
logging.error("this is error")
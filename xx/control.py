import os
import logging
import threading
import xx.CRPS
from flask import *

def sop_service_CRPS():
    print("sop_service : CRPS.py")
    client, addr = xx.CRPS.server.accept()
    xx.CRPS.logz.info("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))


threads = []

threads.append(threading.Thread(target=xx.CRPS.handle_client, args=(xx.CRPS.client,)))

if __name__ == '__main__':
    for t in threads:
        # t.setDaemon(True)
        t.start()





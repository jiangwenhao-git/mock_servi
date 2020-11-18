from ftplib import FTP
import time
import tarfile

def ftpconnect(host,username,passwd):
    ftp = FTP()
    # ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
    ftp.connect(host,21)
    ftp.login(username,passwd)
    return ftp

def downloadfile(ftp,remotepath,localpath):
    bufsize = 1024
    fp = open(localpath,'wb')
    ftp.retrbina
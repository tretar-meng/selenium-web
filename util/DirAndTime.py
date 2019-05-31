# encoding=utf-8

import time,os
from datetime import datetime
from config.VarConfig import screenPicturesDir
from config.VarConfig import firefoxDriveFilePath

#获取当前日期
def getCurrentDate():
    timeTup=time.localtime()
    CurrentDate=str(timeTup.tm_year)+"-"+\
        str(timeTup.tm_mon)+"-"+str(timeTup.tm_mday)
    return CurrentDate

#获取当前时间
def getCurrentTime():
    timeStr=datetime.now()
    nowTime=timeStr.strftime('%H- %M- %S- %f')
    return nowTime

#创建截图存放的目录
def createCurrentDateDir():
    dirName=os.path.join(screenPicturesDir, getCurrentDate())
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    return dirName

if __name__=='__main__':
    print getCurrentDate()
    print createCurrentDateDir()
    print getCurrentTime()
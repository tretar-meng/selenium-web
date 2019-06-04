#encoding=utf-8
#本文件用于实现具体的页面动作

from selenium import webdriver
from config.VarConfig import firefoxDriveFilePath
from util.ObjectMap import getElement
from util.DirAndTime import *
from util.WaitUtil import WaitUtil
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
# import win32api
# import win32con


#定义全局driver变量
driver=None
#全局的等待类实例对象
waitUtil=None

# VK_CODE={
#     'enter':0x0D,
#     'ctrl':0x11,
#     'a':0x41,
#     'v':0x56,
#     'x':0x58
# }
#
# #键盘键按下
# def keyDown(keyName):
#     win32api.keybd_event(VK_CODE[keyName],0,0,0)
# #键盘键抬起
# def keyUp(keyName):
#     win32api.keybd_event(VK_CODE[keyName],0,win32con.KEYEVENTF_KEYUP,0)

def open_browser(browserName,*arg):
    #打开浏览器
    global driver,waitUtil
    try:
        # browserName.lower()=='firefox'
        # #创建firefox浏览器的一个options实例对象
        # firefox_options=Options()
        # #添加屏蔽——ignore—certificate—errors提示信息设置参数项
        # firefox_options.add_experimental_option(
        #     "excludeSwitches",
        #     ["ignore-certificate-errors"])
        # driver=webdriver.Firefox(
        #     executable_path=firefoxDriveFilePath,
        #     firefox_options=firefox_options)
        driver=webdriver.Firefox(executable_path=firefoxDriveFilePath)
        waitUtil=WaitUtil(driver)
    except Exception,e:
        raise e

def visit_url(url,*arg):
    #访问某个网址
    global driver
    try:
        driver.get(url)
    except Exception,e:
        raise e

def ctrl_keys(locationType,locatorExpression,keybord_key,*arg):
    #按下Ctrl+键盘按键
    global driver
    try:
        getElement(driver,locationType,locatorExpression).send_keys(Keys.CONTROL+keybord_key)
    except Exception,e:
        raise e

def refresh_browser(*arg):
    #刷新浏览器
    global driver
    try:
        driver.refresh()
    except Exception, e:
        raise e

def setSize_browser(width,height,*arg):
    #定义浏览器大小
    global driver
    try:
        driver.set_window_size(width,height)
    except Exception, e:
        raise e

def slide_browser(*arg):
    #下滑浏览器至底部
    global driver
    try:
        js = "var q=document.documentElement.scrollTop=100000"
        driver.execute_script(js)
    except Exception, e:
        raise e

def close_browser(*arg):
    #关闭浏览器
    global driver
    try:
        driver.quit()
    except Exception,e:
        raise e


def simulateASingleKeys_Enter(*arg):
    #使用回车键
    global driver
    try:
        ActionChains(driver).send_keys(Keys.ENTER).perform()
    except Exception, e:
        raise e


def web_forward(*arg):
    # 前进
    global driver
    try:
        driver.forward()
    except Exception, e:
        raise e

def web_back(*arg):
    # 后退
    global driver
    try:
        driver.back()
    except Exception, e:
        raise e

def sleep(sleepSeconds,*arg):
    # 强制等待
    try:
        time.sleep(int(sleepSeconds))
    except Exception, e:
        raise e

def implicitly_wait(sleepSeconds,*arg):
    # 隐式等待
    try:
        driver.implicitly_wait(int(sleepSeconds))
    except Exception, e:
        raise e


def clear(locationType,locatorExpression,*arg):
    #清除输入框默认内容
    global driver
    try:
        getElement(driver,locationType,locatorExpression).clear()
    except Exception, e:
        raise e

def input_string(locationType,locatorExpression,inputContent):
    #在页面输入框中输入数据
    global driver
    try:
        getElement(driver,locationType,locatorExpression).send_keys(inputContent)
    except Exception, e:
        raise e

def click(locationType,locatorExpression,*arg):
    #单击页面元素
    global driver
    try:
        getElement(driver,locationType,locatorExpression).click()
    except Exception, e:
        raise e

def assert_string_in_pagesource(assertString,*arg):
    #断言页面源码是否存在某关键字或关键字符串
    global driver
    try:
        assert assertString in driver.page_source,\
            u"%s not found in page source!"% assertString
    except AssertionError,e:
        raise AssertionError(e)
    except Exception,e:
        raise e

def assert_title(titleStr,*args):
    #断言页面标题是否存在某关键字或关键字符串
    global driver
    try:
        assert titleStr in driver.title,\
            u"%s not found in title!"% titleStr
    except AssertionError,e:
        raise AssertionError(e)
    except Exception,e:
        raise e

def getTitle(*arg):
    #获取页面标题
    global driver
    try:
        return driver.title
    except Exception, e:
        raise e

def getPageSource(*arg):
    #获取页面源码
    global driver
    try:
        return driver.page_source
    except Exception, e:
        raise e

def switch_to_frame(locationType,frameLocatorExpression,*arg):
    #切换进入frame
    global driver
    try:
        driver.switch_to_frame(getElement(driver,locationType,frameLocatorExpression))
    except Exception, e:
        print "frame error"
        raise e

def switch_to_default_content(*arg):
    #切出frame
    global driver
    try:
        driver.switch_to.default_content()
    except Exception, e:
        raise e

def switch_window(window_num,*arg):
    #切换标签页
    global driver
    try:
        handle = driver.window_handles[int(window_num)]
        driver.switch_to.window(handle)
    except Exception,e:
        raise e

def switch_alert_accept():
    #弹窗中点击确定
    global driver
    try:
        alert_window_a = driver.switch_to.alert
        alert_window_a.accept()
    except Exception,e:
        raise e

def switch_alert_dismiss():
    #弹窗中点击取消
    global driver
    try:
        alert_window_d = driver.switch_to.alert
        alert_window_d.dismiss()
    except Exception,e:
        raise e

def maxmize_browser():
    #窗口最大化
    global driver
    try:
        driver.maximize_window()
    except Exception,e:
        raise e

def capture_screen(*args):
    #截取屏幕图片
    global driver
    currTime=getCurrentTime()
    picNameAndPath=str(createCurrentDateDir())+"\\"+str(currTime)+".png"
    try:
        driver.get_screenshot_as_file(picNameAndPath.replace('\\',r'\\'))
    except Exception,e:
        raise e
    else:
        return picNameAndPath

def enter(*args):
    #按enter键
    global driver
    try:
        ActionChains(driver).send_keys(Keys.ENTER).perform()
    except Exception, e:
        print ('1111111111')


# def waitPresenceOfElementLocated(locationType,locatorExpression,*arg):
#         '''
#         显示等待页面出现在DOM中，但并不一定可见，存在则返回该页面元素对象
#         '''
#     global waitUtil
#     try:
#         waitUtil.presenceOfElementLocated(locationType,locatorExpression)
#     except Exception,e:
#         raise e


# def waitFrameToBeAvailableAndSwitchToIt(locationType, locatorExpression, *args)
#     '''
#     检查frame是否存在，存在则切换进frame控件中
#     '''
#     global waitUtil
#     try:
#         waitUtil.frameToBeAvailableAndSwitchToIt(locationType, locatorExpression)
#     except Exception, e:
#         # 抛出异常信息给上层调用者
#         raise e


def waitVisibilityOfElementLocated(self, locationType, locatorExpression, *args):
    '''
    显式等待页面元素出现在DOM中，并且可见，存在则返回该页面元素对象
    '''
    global waitUtil
    try:
        waitUtil.visibilityOfElementLocated(locationType, locatorExpression)
    except Exception, e:
        raise e
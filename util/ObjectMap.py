#encoding=utf-8
#本文件用于实现页面定位元素

from selenium.webdriver.support.ui import  WebDriverWait

#获取单个页面元素对象
def getElement(driver,locationType,locatorExpression):
    try:
        element=WebDriverWait(driver,30).until\
            (lambda x:x.find_element(by=locationType,value=locatorExpression))
        return element
    except Exception,e:
        raise e

#获取多个相同页面的元素对象，以list返回
def getElement(driver,locationType,locatorExpression):
    try:
        elements = WebDriverWait(driver, 30).until\
            (lambda x: x.find_element(by=locationType, value=locatorExpression))
        return elements
    except Exception, e:
        raise e

if __name__=='__mian__':
    from selenium import webdriver
    #进行单元测试
    driver=webdriver.Firefox(executable_path="E:\BaiduNetdiskDownload\driver\Firefox\geckodriver.exe")
    driver.get("https://www.baidu.com")
    searchBox=getElement(driver,"id","kw")
    #打印页面对象的标签名
    print searchBox.tag_name
    aList=getElement(driver,"tag name","a")
    print len(aList)
    driver.quit()

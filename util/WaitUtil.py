#encoding=utf-8
#本文件用于实现智能等待页面元素的出现

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WaitUtil(object):

    def __init__(self,driver):
        self.locationTypeDict={
            "xpath":By.XPATH,
            "id":By.ID,
            "name":By.NAME,
            "class_name":By.CLASS_NAME,
            "tag_name":By.TAG_NAME,
            "link_text":By.LINK_TEXT,
            "partial_link_text":By.PARTIAL_LINK_TEXT
        }
        self.driver=driver
        self.wait=WebDriverWait(self.driver,30)

    def presenceOfElementLocated(self,locatorMethod,locatorExpression,*arg):
        '''
        显示等待页面出现在DOM中，但并不一定可见，存在则返回该页面元素对象
        '''
        try:
            if self.locationTypeDict.has_key(locatorMethod.lower()):
                self.wait.until(
                    EC.presence_of_element_located((
                        self.locationTypeDict[locatorMethod.lower()],
                        locatorExpression)))
            else:
                raise TypeError(u"未找到定位元素，请确定定位方法是否写正确")
        except Exception,e:
            raise e

    def frameToBeAvailableAndSwitchToIt(self,locationType,locatorExpression,*arg):
        '''
        检查frame是否存在，存在则切换进frame控件中
        '''
        try:
            self.wait.until(EC.frame_to_be_available_and_switch_to_it
                            ((self.locationTypeDict[locationType.lower()],
                              locatorExpression)))
        except Exception,e:
            #抛出异常信息给上层调用者
            raise e

    def visibilityOfElementLocated(self,locationType,locatorExpression,*arg):
        '''显式等待页面元素出现在DOM中，并且可见，存在则返回该页面元素对象'''
        try:
            self.wait.until(
                EC.visibility_of_element_located((
                    self.locationTypeDict[locationType.lower()],
                    locatorExpression)))
        except Exception,e:
            raise e
        
if __name__=='__mian__':
    from selenium import webdriver
    driver=webdriver.Firefox(executable_path="E:\BaiduNetdiskDownload\driver\Firefox\geckodriver.exe")
    driver.get("http://mail.126.com")
    waitUtil=WaitUtil(driver)
    waitUtil.frame_available_and_switch_to_it("id","x-URS-iframe")
    e=waitUtil.visibility_element_located("xpath","//input[@name='email']")
    e.send_keys("success")
    driver.quit()


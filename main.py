# encoding=utf-8

import sys
import errno
from testScripts.test_for_redemption import *
from config import VarConfig
from report import parser

#设置此次测试环境编码为utf8
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__=='__main__':
    global excelObj
    # global screenPicturesDir

    

    # 每读取到一个Excel文件执行一遍循环
    for dataFilePath in excel_files:
        excelObj.loadWorkBook(dataFilePath)

        # 给每个Excel创建一个异常截图目录
        parent_path = dataFilePath.split('\\')
        parent_path[0] = parent_path[0]+'\\'
        testData_position = parent_path.index('testData')
        parent_path.insert(testData_position+1,'exceptionpictures')
        parent_path[-1] = parent_path[-1].split('.')[0]
        screenShotDir = os.path.join(*parent_path)
        # 面对已存在目录的异常处理
        try:
            os.makedirs(screenShotDir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(screenShotDir):
                pass
            else:
                raise

        VarConfig.screenPicturesDir = screenShotDir
        test_for_redemption()
    

    testExcel = parser.getAllTestExcel()
    for fileMeta in testExcel:
        parser.parseTestResult(fileMeta)
    
    parser.tidyReport()
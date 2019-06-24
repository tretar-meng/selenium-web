#encoding=utf-8
#本文件用于定义整个框架中所需要的一些全局变量
import os

# FIXME
parentDirPath = os.getcwd()

#火狐浏览器驱动存放路径
firefoxDriveFilePath=parentDirPath+"\driver\geckodriver-v0.24.0-win64.exe"

#异常截图存放路径
screenPicturesDir = ''

#测试数据存放的绝对路径
work_dir = parentDirPath+"\\testData"

# 读取路径中的所有文件
all_files = []
for parent,dirnames,filenames in os.walk(work_dir):
    for filename in filenames:
        file = os.path.join(parent,filename)
        all_files.append(file)

# 提取路径中的所有Excel文件
global excel_files
excel_files = []
for excel in all_files:
    if excel.endswith('xlsx'):
        excel_files.append(excel)

#测试数据文件中，测试用例表中部分列对应的数字序号
testCase_testCaseName=2
testCase_frameWorkName=4
testCase_testStepSheetName=5
testCase_dataSourceSheetName=6
testCase_isExecute=7
testCase_runTime=8
testCase_testResult=9

#用例步骤表中，部分列对应的数字序号
testStep_testStepDescribe=2
testStep_keyWords=3
testStep_locationType=4
testStep_locatorExpression=5
testStep_operateValue=6
testStep_runTime=7
testStep_testResult=8
testStep_errorInfo=9
testStep_errorPic=10

#数据源表格中，是否执行行列对应的数字编号
dataSource_isExcute=8
dataSource_runtime=9
dataSource_result=10
dataSource_name=3


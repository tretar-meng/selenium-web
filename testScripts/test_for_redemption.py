# encoding=utf-8
from action.PageAction import *
from util.ParseExcel import ParseExcel
from config.VarConfig import *
import time
import traceback

#创建解析Excel对象

excelObj=ParseExcel()

#用例或用例步骤执行结束后，像excel中执行结果信息
def writeTestResult(sheetObj,rowNo,colsNo,testResult,
                    errorInfo=None,picPath=None):
    #测试通过结果为绿色，失败为红色
    colorDict={"pass":"green","failed":"red","none":"green"}

    # 因为“测试用例”工作表和“用例步骤Sheet表”中都有测试执行时间和测试
    # 测试结果列，定义此字典对象是为了区分具体应该写哪个工作表
    colsDict = {
        "testCase":[testCase_runTime,testCase_testResult],
        "caseStep":[testStep_runTime,testStep_testResult],
        "dataSheet":[dataSource_runtime,dataSource_result]}
    try:
        # 在测试步骤sheet中，写入测试时间
        excelObj.writeCellCurrentTime(sheetObj,\
                                      rowNo=rowNo,colsNo=colsDict[colsNo][0])
        # 在测试步骤sheet中，写入测试结果
        excelObj.writeCell(sheetObj, content=testResult,
                           rowNo=rowNo, colsNo=colsDict[colsNo][1], style=colorDict[testResult])
        if errorInfo and picPath:
            # 在测试步骤sheet中，写入异常信息
            excelObj.writeCell(sheetObj,content=errorInfo,rowNo=rowNo,\
                               colsNo=testStep_errorInfo)
            # 在测试步骤sheet中，写入异常截图路径
            excelObj.writeCell(sheetObj,content=picPath,rowNo=rowNo,colsNo=testStep_errorInfo)
        elif colsNo == 'caseStep':
            # 在测试步骤sheet中，清空异常信息单元格
            excelObj.writeCell(sheetObj, content="", \
                                   rowNo=rowNo, colsNo=testStep_errorInfo)
            # 在测试步骤sheet中，清空异常信息单元格
            excelObj.writeCell(sheetObj,content="",\
                               rowNo=rowNo,colsNo=testStep_errorPic)
    except Exception as e:
        print u"写excel时发生异常,",+traceback.print_exc()

#数据驱动框架
def dataDriverFun(dataSourceSheetObj,stepSheetObj):
    try:
        # 获取数据源表中是否执行列对象
        dataIsExecuteColumn = excelObj.getColumn(
            dataSourceSheetObj,dataSource_isExcute)
        # 获取数据源表中“员工姓名”列对象
        nameColumn = excelObj.getColumn(dataSourceSheetObj,dataSource_name)
        # 获取测试步骤表中存在数据区域的行数
        stepRowNums = excelObj.getRowsNumber(stepSheetObj)
        # 记录成功执行的数据条数
        successDatas = 0
        # 记录被设置为执行的数据条数
        requiredDatas = 0
        for idx,data in enumerate(dataIsExecuteColumn[1:]):
            # 遍历数据源表，准备进行数据驱动测试
            # 因为第一行是标题行，所以从第二行开始遍历
            if data.value == "y":
                print u'开始%s'%(nameColumn[idx+1].value)
                requiredDatas +=1
                # 定义记录执行成功步骤数变量
                successStep = 0
                for index in xrange(2,stepRowNums+1):
                    # 获取数据驱动测试步骤表中第index行对象
                    rowObj = excelObj.getRow(stepSheetObj,index)
                    # 获取关键字作为调用的函数名
                    keyWord = rowObj[testStep_keyWords -1].value
                    # 获取操作元素的定位表达式作为调用函数的参数
                    locationType = rowObj[testStep_locationType -1].value
                    # 获取操作元素的定位表达式作为调用的函数的参数
                    locatorExpression = rowObj[testStep_locatorExpression -1].value
                    # 获取操作值作为调用函数的参数
                    operateValue = rowObj[testStep_operateValue -1].value
                    if isinstance(operateValue,long):
                        operateValue = str(operateValue)
                    if isinstance(operateValue, int):
                        operateValue = str(operateValue)
                        # 构造需要执行的python表达式，此表达式对应的是PageAction.py文件
                        # 中的页面动作函数调用的字符串表示
                    tmpStr = "'%s','%s'"%(locationType.lower(),locatorExpression.replace(\
                            "'",'"'))if locationType and locatorExpression else""
                    if operateValue and operateValue.isalpha() and len(operateValue)==1:
                        # 如果operateValue变量是字母且为1，说明有操作值从数据源表中
                        # 根据坐标获取对应单元格的数据
                        coordinate = operateValue+str(idx+2)
                        operateValue = excelObj.getCellOfValue(dataSourceSheetObj,\
                                                               coordinate=coordinate)
                    if tmpStr:
                        operateValue=str(operateValue)
                        tmpStr+=\
                        ",u'"+operateValue+"'" if operateValue else ""
                    else:
                        operateValue = str(operateValue)
                        tmpStr +=\
                        "u'"+operateValue+"'" if operateValue else ""
                    # keyWord=str(keyWord)
                    runStr = keyWord+"("+tmpStr+")"
                    print(runStr)
                    try:
                        if operateValue!=u"否" and operateValue!=u"不输入":
                            eval(runStr)
                    except Exception as e:
                        print(u'执行步骤%s发生异常'%rowObj[testStep_testStepDescribe-1].value)
                        print traceback.print_exc()
                        # # 截取异常屏幕图片
                        capturePic = capture_screen()
                        # # 获取详细的异常堆栈信息
                        errorInfo = traceback.format_exc()
                        writeTestResult(stepSheetObj, rowNo=index, \
                                        colsNo="caseStep", testResult="failed", \
                                        errorInfo=str(errorInfo), picPath=capturePic)
                    else:
                        successStep+=1
                        writeTestResult(stepSheetObj, rowNo=index, colsNo="caseStep", \
                                        testResult="pass")
                        print(u'执行步骤%s成功'%rowObj[testStep_testStepDescribe-1].value)
                if stepRowNums == successStep+1:
                    successDatas+=1
                    # 如果成功执行的步骤数等于步骤表中给出的步骤数
                    # 说明第idx+2行的数据执行通过，写入通过信息
                    writeTestResult(dataSourceSheetObj,rowNo=idx+2,colsNo="dataSheet",\
                                        testResult="pass")
                else:
                    # 写入失败信息
                    writeTestResult(dataSourceSheetObj,rowNo=idx+2,colsNo="dataSheet",\
                                        testResult="failed")
            else:
                # 将不需要执行的数据行的执行时间和执行结果单元格清空
                writeTestResult(dataSourceSheetObj,rowNo=idx+2,colsNo="dataSheet",\
                                testResult="none")
        if requiredDatas == successDatas:
            # 只要当成功执行的数据条数等于被设置为需要执行的数据条数，
            # 才表示调用数据驱动的测试用例执行通过
            return 1
        # 表示调用数据驱动的测试用例执行失败
        return None
    except Exception as e:
        raise e

def test_for_redemption():
    try:
        # 根据Excel文件中的sheet名获取sheet对象
        caseSheet = excelObj.getSheetByName(u'测试用例')
        # 获取测试用例sheet中是否执行列对象
        isExecuteColumn = excelObj.getColumn(caseSheet,testCase_isExecute)
        # 记录执行成功的测试用例个数
        successfulCase = 0
        # 记录需要执行的用例个数
        requiredCase =0

        for idx,i in enumerate(isExecuteColumn[1:]):
            # 因为用例sheet中第一行为标题行，无须执行
            caseName = excelObj.getCellOfValue(caseSheet, rowNo=idx + 2,colsNo=testCase_testCaseName)

            if i.value.lower() == "y":
                requiredCase += 1
                # 获取测试用例表中，第idx+1行中
                # 用例执行时所使用的框架类型
                useFrameWorkName = excelObj.getCellOfValue( \
                    caseSheet, rowNo=idx + 2, colsNo=testCase_frameWorkName)
                # 获取测试用例列中，第idx+1行中执行用例的步骤sheet名
                stepSheetName = excelObj.getCellOfValue( \
                    caseSheet, rowNo=idx + 2, colsNo=testCase_testStepSheetName)
                print ('----------' + stepSheetName)
                if useFrameWorkName == u'数据':
                    print(u'***********调用数据驱动************')
                    # 获取测试用例表中，第idx+1行，执行框架为数据驱动的用例所使用的数据sheet名
                    dataSheetName = excelObj.getCellOfValue( \
                        caseSheet, rowNo=idx + 2, colsNo=testCase_dataSourceSheetName)
                    # 获取第idx+1行测试用例的步骤sheet对象
                    stepSheetObj = excelObj.getSheetByName(stepSheetName)
                    # 获取第idx+1行测试用例使用的数据sheet对象
                    dataSheetObj = excelObj.getSheetByName(dataSheetName)
                    # 通过数据驱动框架执行添加数据
                    result = dataDriverFun(dataSheetObj, stepSheetObj)
                    if result:
                        print(u'用例%s执行成功' % (caseName))
                        successfulCase += 1
                        writeTestResult(caseSheet, rowNo=idx + 2, \
                                        colsNo="testCase", testResult="pass")
                    else:
                        print(u'用例%s执行失败' % (caseName))
                        writeTestResult(caseSheet, rowNo=idx + 2, colsNo="testCase", testResult="failed")
                elif useFrameWorkName == u"关键字":
                    print("*************调用关键字驱动****************")
                    caseStepObj = excelObj.getSheetByName(stepSheetName)
                    stepNums = excelObj.getRowsNumber(caseStepObj)
                    successfulSteps = 0
                    print(u'测试用例共%s步' % (stepNums-1))
                    for index in range(2, stepNums + 1):
                        # 因为第一行标题行无须执行
                        # 获取步骤sheet中第index行对象
                        stepRow = excelObj.getRow(caseStepObj, index)
                        # 获取关键字作为调用的函数名
                        keyWord = stepRow[testStep_keyWords - 1].value
                        # 获取操作元素定位方式作为调用的函数的参数
                        locationType = stepRow[testStep_locationType - 1].value
                        # 获取操作元素的定位表达式作为调用函数的参数
                        locatorExpression = stepRow[testStep_locatorExpression - 1].value
                        # 获取操作值为调用函数的参数
                        operateValue = stepRow[testStep_operateValue - 1].value
                        if isinstance(operateValue, long):
                            # 如果operateValue值为数字型，
                            # 将其转换为字符串，方便字符串拼接
                            operateValue = str(operateValue)
                        # 构造需要执行的Python表达式，此表达式对应的是PageAction.py文件
                        # 中的页面动作函数调用的字符串表达式
                        tmpStr = "'%s','%s'" % (locationType.lower(), \
                                                locatorExpression.replace("'", '"') \
                                                ) if locationType and locatorExpression else ""
                        if tmpStr:
                            tmpStr += \
                                ",u'" + operateValue + "'" if operateValue else ""
                        else:
                            tmpStr += \
                                "u'" + operateValue + "'" if operateValue else ""

                        runStr = keyWord + "(" + tmpStr + ")"
                        print(runStr)
                        try:
                            # 通过eval函数，将拼接的页面动作函数调用的字符串表示
                            # 当成有效的Python表达式执行，从而执行测试步骤的sheet
                            # 中关键字在PageAction.py文件中对应的映射方法，
                            # 来完成对页面元素的操作
                            eval(runStr)
                        except Exception as e:
                            print(u"执行步骤%s发生异常" % (stepRow[testStep_testStepDescribe - 1].value))
                            # 截取异常屏幕图片
                            capturePic = capture_screen()
                            # 获取详细的异常堆栈信息
                            errorInfo = traceback.format_exc()
                            writeTestResult(caseStepObj, rowNo=index, \
                                            colsNo="caseStep", testResult="failed", \
                                            errorInfo=str(errorInfo), picPath=capturePic)
                        else:
                            successfulSteps += 1
                            print(u'执行步骤%s成功' % (stepRow[testStep_testStepDescribe - 1].value))
                            writeTestResult(caseStepObj, rowNo=index, colsNo="caseStep", testResult="pass")
                    if successfulSteps == stepNums - 1:
                        successfulCase += 1
                        print(u'用例%s执行通过' % (caseName))
                        writeTestResult(caseSheet, rowNo=idx + 2, \
                                        colsNo="testCase", testResult="pass")
                    else:
                        print(u"用例%s执行失败" % (caseName))
                        writeTestResult(caseSheet, rowNo=idx + 2, colsNo="testCase", testResult="failed")
            else:
                # 清空不需要执行用例的执行时间和执行结果，
                # 异常信息，异常图片单元格
                writeTestResult(caseSheet, rowNo=idx + 2, \
                                colsNo="testCase", testResult="failed")
        print(u"共%s条用例，%s条需要被执行，成功执行%s条" \
                 % (len(isExecuteColumn) - 1, requiredCase, successfulCase))
    except Exception as e:
        print("出现异常" + traceback.format_exc())

if __name__=='__main__':
    test_for_redemption()

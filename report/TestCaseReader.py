# encoding=utf-8

from config import VarConfig


class TestCaseReader(object):

    def __init__(self,exObject):

        # excel Object
        self.exObject = exObject
        self.testcaseIdx = 1 
        self.testcaseSheet = exObject.getSheetByName(u"测试用例")
        self.testcaseSheetRowN = exObject.getRowsNumber(self.testcaseSheet)

        # following is the current testcase state
        self.stepSheet = None
        self.dataSheet = None
        self.currentTestcaseMeta = None
        # data-driven or keyword-driven
        self.frameworkType = None
        self.currentStepIdx = 1
        self.stepSheetRowN = 0
        self.currentDataIdx = 1
        self.dataSheetRowN = 0 

        self.currentStep = {}

    
    def loadNextTestcase(self):

        self.testcaseIdx += 1
        if self.testcaseIdx > self.testcaseSheetRowN:
            return False
        
        testcaseRow = self.exObject.getRow(self.testcaseSheet, self.testcaseIdx)

        self.frameworkType = testcaseRow[VarConfig.testCase_frameWorkName-1].value

        # 获取步骤sheet名
        stepSheetName = testcaseRow[VarConfig.testCase_testStepSheetName-1].value
        self.stepSheet = self.exObject.getSheetByName(stepSheetName)
        self.stepSheetRowN = self.exObject.getRowsNumber(self.stepSheet)

        if self.frameworkType == u'数据':
            # 获取数据sheet名
            dataSheetName = testcaseRow[VarConfig.testCase_dataSourceSheetName-1].value
            self.dataSheet = self.exObject.getSheetByName(dataSheetName)
            self.dataSheetRowN = self.exObject.getRowsNumber(self.dataSheet)

        # reset state
        self.currentStepIdx = 1
        self.currentDataIdx = 1


        self.currentTestcaseMeta = {
            "name":self.stepSheet.title,
            "desc":testcaseRow[VarConfig.testCase_testCaseName - 1].value,
            "shouldExc":testcaseRow[VarConfig.testCase_isExecute - 1].value,
            "result":testcaseRow[VarConfig.testCase_testResult - 1].value,
            "steps":[],
        }
        
        return True
    
    def nextStep(self):

        self.currentStepIdx += 1
        if self.currentStepIdx > self.stepSheetRowN:
            return False
        
        stepRow = self.exObject.getRow(self.stepSheet, self.currentStepIdx)
        
        stepDesc = stepRow[VarConfig.testStep_testStepDescribe - 1].value
        stepRunTime = stepRow[VarConfig.testStep_runTime - 1].value
        stepResult = stepRow[VarConfig.testStep_testResult - 1].value
        stepErr = stepRow[VarConfig.testStep_errorInfo - 1].value
   
        self.currentStep = {
            "stepDesc":stepDesc.replace('\n',''),
            "stepRunTime":stepRunTime,
            "stepResult":stepResult,
            "stepErr":stepErr,
        }

        return True
    
    def getTestcaseMeta(self):

        return self.currentTestcaseMeta

    def getStep(self):

        return self.currentStep

        
        
        

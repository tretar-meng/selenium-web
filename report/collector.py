# encoding=utf-8

import datetime
from config import VarConfig

class Collector(object):

    def __init__(self):
        # data[module][filename][testcase]
        self.data = {} 

        # context fot quick setting
        self.context = {
            "module":None,
            "filename":None,
            "testcase":None,
        }
    
    def newModule(self,module):

        # FIXME:
        if module not in self.data:
            self.data[module] = {}
        self.context["module"] = module
    
    def newTestFile(self,filename):
        self.data[self.context["module"]][filename] = {}
        self.context["filename"] = filename

    def newTestCase(self,testcase):
        self.data[self.context["module"]][self.context["filename"]][testcase["name"]] = testcase

        self.context["testcase"] = testcase["name"]

    def setContext(self,module , filename,testcase):
        self.context["module"] = module
        self.context["filename"] = filename
        self.context["testcase"] = testcase
    
    def appendStep( self , step , module=None , filename=None , testcase=None ):
        if module == None:
            module = self.context["module"]
        if filename == None:
            filename = self.context["filename"]
        if testcase == None:
            testcase = self.context["testcase"]

        self.data[module][filename][testcase]["steps"].append(step)
    
    def fileScopeMetric(self,exFile):

        metric = {
            "total": len(exFile["testcases"]),
            "pass" : 0,
            "failed": 0,
        }

        for case in exFile["testcases"]:
            if case["shouldExc"] == "y":
                if  case["result"] == "pass":
                    metric["pass"]+=1
                else:
                    metric["failed"]+=1
        
        return metric

    def moduleScopeMetric(self,module):

        metric = {
            "total": len(module["files"]),
            "pass" : 0,
            "failed": 0,
        }

        for exFile in module["files"]:
            if exFile["failed"] > 0:
                metric["failed"]+=1
            else:
                metric["pass"]+=1


        return metric

    
    def dumpData(self):

        # encode data to render to the tmpl file
        modules = []
        for moduleName,module in self.data.items():

            files = []
            for filename,file in module.items():

                exFile = {
                    "name":filename,
                    "testcases":file.values(),
                }

                metric = self.fileScopeMetric(exFile)
                exFile.update(metric)

                if exFile["failed"] > 0:
                    exFile["status"] = u"失败"
                else:
                    exFile["status"] = u"通过"

                files.append(exFile)
            
            # 
            mModule = {
                "name":moduleName,
                "files":files,
            }

            mModule.update(self.moduleScopeMetric(mModule))
            if mModule["failed"] > 0:
                mModule["status"] = u"失败"
            else:
                mModule["status"] = u"通过"

            modules.append(mModule)

        return modules

                    



# encoding=utf-8

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
        self.data[self.context["module"]][self.context["filename"]][testcase] = {
            "steps":[],
        }
        self.context["testcase"] = testcase

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
    
    def dumpData(self):

        # encode data to render to the tmpl file
        modules = []
        for moduleName,module in self.data.items():

            files = []
            for filename,file in module.items():
                testcases = []
                for testcaseName,testcase in file.items():
                    testcases.append({
                        "name":testcaseName,
                        "steps":testcase["steps"],
                    })

                files.append({
                    "name":filename,
                    "testcases":testcases,
                })
            
            modules.append({
                "name":moduleName,
                "files":files,
            })

        return modules

                    



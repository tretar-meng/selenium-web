# encoding=utf-8

import os
from util import ParseExcel
from config import VarConfig
from collector import Collector
from TestCaseReader import TestCaseReader
from jinja2 import Template


ResultCollector = Collector() 


def getAllTestExcel():
    # 读取路径中的所有文件
    work_dir =  os.path.join( os.getcwd() , "testData" )

    # { module:"${dirName}", filename:"${testFileWithoutSuffix'.xlsx'}" , filepath:"" }
    all_files = []
    for parent,dirnames,filenames in os.walk(work_dir):
        for filename in filenames:
            if filename.endswith("xlsx"):
                file = os.path.join(parent,filename)
                all_files.append({
                    "module":os.path.split(parent)[1],
                    "filename":filename.split('.')[0],
                    "filepath":file,
                })
    return all_files


def parseTestResult(testExcel):


    exParser = ParseExcel.ParseExcel()
    exParser.loadWorkBook(testExcel["filepath"])

    ResultCollector.newModule(testExcel["module"])
    ResultCollector.newTestFile(testExcel["filename"])
    

    # fetch testcases
    testcaseReader = TestCaseReader(exParser)

    while testcaseReader.loadNextTestcase():

        ResultCollector.newTestCase(testcaseReader.getTestcaseMeta())

        while testcaseReader.nextStep():

            ResultCollector.appendStep(testcaseReader.getStep())

def tidyReport():

    # TODO
    tmpF=open(os.path.join(VarConfig.tmpl_dir , "index.js.jinja") , "r")
    tmplStr=tmpF.read()
    tmpF.close()


    renderedFile=Template(tmplStr).render(modules=ResultCollector.dumpData())
       
    outputFile=open(os.path.join(VarConfig.tmpl_dir , "index.js"),"w")
    outputFile.write(renderedFile)
    outputFile.close()




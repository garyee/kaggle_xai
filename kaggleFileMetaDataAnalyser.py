from kaggleEnums import getKaggleRefFromFilePathPartStr
from kaggleHelper import bash
from kaggleDownloader import getDataSetPath
import json
import os
import re

def getMetaDateFilePath(dataSetPath):
    return dataSetPath+'dataset-metadata.json'

def analyseDataSetMetaData(dataSetRef,resDict):
    dataSetPath = getDataSetPath(dataSetRef)
    metaDataFilePath=getMetaDateFilePath(dataSetPath)
    if not os.path.isfile(metaDataFilePath) :
        bash('kaggle datasets metadata -p '+dataSetPath+' '+getKaggleRefFromFilePathPartStr(dataSetRef))
    if os.path.isfile(metaDataFilePath) :
        analyseOneMetaDataFile(metaDataFilePath,resDict)
        os.remove(metaDataFilePath)

def analyseOneMetaDataFile(filePath,resDict):
    
    with open(filePath, encoding='utf-8') as f:
        metaData={}
        if os.stat(filePath).st_size == 0:
            os.remove(filePath)
            print(filePath+' was empty and thus removed!')
            return
        try:
            metaData = json.load(f)
        except ValueError:
            print('Decoding JSON has failed for: '+filePath)
        if 'keywords' in metaData:
            for keywords in metaData['keywords']:
                for dataType,keyWordArr in metaDataType.items():
                    if(len(keyWordArr)>0):
                        for typeRegex in keyWordArr:
                            tmp=re.search(typeRegex, keywords.strip().lower())
                            if re.search(typeRegex, keywords.strip().lower()) is not None:
                                resDict['type']=dataType
                                break
                for goal in metaDataGoal:
                    if goal.strip().lower() in keywords.strip().lower():
                        resDict['tab_goal']=goal
                        break

#See DB Fields & order matters:
metaDataType={
    'Tabular':[r'tabular'],
    'Image':[r'computer vision'],
    'Video':[r'^video$'],
    'Text':[r'nlp',r'linguistics'],
    'DB':[r'db'],
    'Time Series':[r'time series'],
    'Misc':[],
}

metaDataGoal=['regression','classification']
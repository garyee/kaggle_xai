from kaggleHelper import bash
from kaggleDownloader import getDataSetPath
import json
import os

def getMetaDateFilePath(dataSetPath):
    return dataSetPath+'dataset-metadata.json'

def analyseDataSetMetaData(dataSetRef,resDict):
    dataSetPath = getDataSetPath(dataSetRef)
    metaDataFilePath=getMetaDateFilePath(dataSetPath)
    if not os.path.isfile(metaDataFilePath) :
        bash('kaggle datasets metadata -p '+dataSetPath+' '+dataSetRef)
    analyseOneMetaDataFile(metaDataFilePath,resDict)
    os.remove(metaDataFilePath)

def analyseOneMetaDataFile(filePath,resDict):
    with open(filePath) as f:
        metaData={}
        try:
            metaData = json.load(f)
        except ValueError:
            print('Decoding JSON has failed for: '+filePath)
        if 'keywords' in metaData:
            for keywords in metaData['keywords']:
                for dataType in metaDataType:
                    if dataType.strip().lower() in keywords.strip().lower():
                        resDict['type']=dataType
                        break
                for goal in metaDataGoal:
                    if goal.strip().lower() in keywords.strip().lower():
                        resDict['tab_goal']=goal
                        break

#See DB Fields & order matters:
metaDataType=['Time Series','Tabular']
metaDataGoal=['regression','classification']

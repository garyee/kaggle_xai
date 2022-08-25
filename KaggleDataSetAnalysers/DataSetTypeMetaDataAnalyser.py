import json
import os
import re
from KaggleDataSetAnalysers.KaggleDataSetAnalyser import KaggleDataSetAnalyser
from Downloaders.kaggleCodeDownloader import getDataSetPath
from utils.kaggleEnums import metaDataGoal, KaggleEntityType, getKaggleRefFromFilePathPartStr
from utils.DataSetTypes import DataSetTypes
from utils.kaggleHelper import bash, setTypeAndCertainty

class DataSetTypeMetaDataAnalyser(KaggleDataSetAnalyser):
    
    def analyse(self,entityRef,entityType,resDict,kernelCountPerDataSet):
        if entityType==KaggleEntityType.DATASET:
                self.analyseDataSetMetaData(entityRef,resDict)

    def analyseDataSetMetaData(self,dataSetRef,resDict):
        dataSetPath = getDataSetPath(dataSetRef)
        metaDataFilePath=self.getMetaDateFilePath(dataSetPath)
        if not os.path.isfile(metaDataFilePath) :
            bash('kaggle datasets metadata -p '+dataSetPath+' '+getKaggleRefFromFilePathPartStr(dataSetRef))
        if os.path.isfile(metaDataFilePath) :
            if os.stat(metaDataFilePath).st_size > 0:
                self.analyseOneMetaDataFile(metaDataFilePath,resDict)
            os.remove(metaDataFilePath)

    def analyseOneMetaDataFile(self,filePath,resDict):
        with open(filePath, encoding='utf-8') as f:
            metaData={}
            try:
                metaData = json.load(f)
            except ValueError:
                print('Decoding JSON has failed for: '+filePath)
            if 'keywords' in metaData:
                for keywords in metaData['keywords']:
                    for dataSetType in DataSetTypes:
                        # for dataType,keyWordArr in metaDataType.items():
                        regexArr=dataSetType.getMetaDataKeywordRegexes()
                        if(len(regexArr)>0):
                            for typeRegex in regexArr:
                                if re.search(typeRegex, keywords.strip().lower()) is not None:
                                    setTypeAndCertainty(dataSetType,dataSetType.getMetaDataTypeCertanties(),resDict)
                                    break
                    for goal in metaDataGoal:
                        if goal.strip().lower() in keywords.strip().lower():
                            resDict['tab_goal']=goal
                            break
                
    def getMetaDateFilePath(self,dataSetPath):
        return dataSetPath+'dataset-metadata.json'

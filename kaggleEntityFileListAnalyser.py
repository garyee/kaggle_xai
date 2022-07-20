from kaggleEnums import KaggleEntityType
from kaggleHelper import kaggleCommand2DF
import os
import re

fileTypeFileExtensions = {
    'Tabular': ['csv','xls'],
    'Image':['jpg','gif','png'],
    'Video':['mpg','mp4','mpeg'],
    'Text':[''],
    'DB':['db','sqlite'],
    'Time Series':[],
    'Misc':[]
}

ignoreExtensions=['tfrec']

def analyseEntityFileList(entityRef,resDict,entityType=KaggleEntityType.DATASET):
  command='kaggle datasets files '+entityRef
  if entityType==KaggleEntityType.COMPETITION:
    command='kaggle competitions files -q '+entityRef
  fileList = kaggleCommand2DF(command)
  countPerType={}
  overAllFileSize=0
  for index, row in fileList.iterrows():
    filename=row['name']
    fileSize=parseFileSize(row['size'])
    overAllFileSize+=fileSize
    _, file_extension = os.path.splitext(filename)
    file_extension=file_extension.lstrip('.').lower();
    if file_extension not in ignoreExtensions:
        for fileType, extensionArray in fileTypeFileExtensions.items():
            if file_extension in extensionArray:
                if fileType not in countPerType:
                    countPerType[fileType]=fileSize
                else:
                    countPerType[fileType]+=fileSize
        maxType=None
        maxFileSizeSum=0
        for fileTypeCounted, countedFileSizePerType in countPerType.items():
            if(countedFileSizePerType/overAllFileSize>maxFileSizeSum):
                maxType=fileTypeCounted
                maxFileSizeSum=countedFileSizePerType/overAllFileSize
        if maxType is not None:
            resDict['type']=maxType
    
def parseFileSize(fileSizeStr):
    units = {"B": 1, "KB": 2**10, "MB": 2**20, "GB": 2**30, "TB": 2**40 ,
             "":  1, "KIB": 10**3, "MIB": 10**6, "GIB": 10**9, "TIB": 10**12}
    m = re.match(r'^([\d\.]+)\s*([a-zA-Z]{0,3})$', str(fileSizeStr).strip())
    number, unit = float(m.group(1)), m.group(2).upper()
    return int(number*units[unit])

analyseEntityFileList("calebreigada/us-air-quality-1980present",{})
import os
import shutil
import pandas as pd
from utils.DataSetTypes import DataSetTypes
from utils.KaggleCommands.KaggleCommand import KaggleCommandOperations
from utils.KaggleCommands.KaggleCommandFactory import KaggleCommandFactory
from utils.kaggleEnums import compressionExtensions,baseTmpPath,KaggleEntityType, getKaggleEntityString, getPathNameFromKaggleRef, isArchiveFile
from utils.kaggleHelper import bash,kaggleCommand2DF
from utils.webStuff import acceptCompetitionRules

def getFileListByDataSetRef(dataSetRef,dataSetType =KaggleEntityType.DATASET):
    # command ='kaggle '+getKaggleEntityString(dataSetType,True)+' files '+dataSetRef
    # fileList = kaggleCommand2DF(command)
    fileList = KaggleCommandFactory.buildCommand(dataSetType, KaggleCommandOperations.FILES).execute()
    return list(fileList.iloc[:,0])


def getTrainingFileName(fileList):
    res=None
    countTableFiles=0
    lastTableFileName=None
    downloadedAtLeastOneFile=False
    #simple train.csv case
    if('train.csv' in fileList):
        return 'train.csv'
    #there is only one file case
    if(len(fileList)==1):
        return fileList[0]
    #iterate fileList
    for fullfileName in fileList:
        #imediat return in case of train.csv
        filename, file_extension = os.path.splitext(fullfileName)
        if(filename.strip().lower()=='train'):
            return fullfileName
        if(isArchiveFile(fullfileName) and (filename=='train' or filename=='train.csv')):
            return fullfileName
        if(file_extension in  DataSetTypes.TABULAR.getExtensions()):
            countTableFiles+=1
    if(countTableFiles==1 and lastTableFileName is not None):
        return lastTableFileName
    return None

def getTrainingFileAsDataframe(dataSetRef,dataSetType,fileName):
    filePath=downloadOneFile(dataSetRef,dataSetType,fileName)
    dataframe=openFileToDataframe(filePath)
    return filePath,dataframe

def openFileToDataframe():
    #TODO
    return pd.DataFrame([])

def downloadOneFile(dataSetRef, dataSetType,fileName,isZip,accetanceTry=0):
  tmpPath=getTmpPathforDataSetFile(dataSetRef)
  if(not os.path.exists(tmpPath)):
    os.mkdir(tmpPath)
  res= bash('kaggle '+getKaggleEntityString(dataSetType,True)+' download -q -f '+fileName+' -p '+tmpPath+''+(' --unzip' if isZip else'')+' '+dataSetRef)
  if '403 - Forbidden' in res:
    if(dataSetType == KaggleEntityType.COMPETITION):
      if(accetanceTry<6):
        acceptCompetitionRules(dataSetRef)
        downloadOneFile(dataSetRef, dataSetType,fileName,isZip,accetanceTry+1)
      else:
        raise Exception('Accept Rules attemps overflow: '+dataSetRef)
  else:
      #print('downloaded files for '+getKaggleEntityString(dataSetType)+' '+dataSetRef)
      return getTmpPathforDataSetFile(dataSetRef)+fileName
  return None

def getTmpPathforDataSetFile(dataSetRef):
  return baseTmpPath+getPathNameFromKaggleRef(dataSetRef)+"/"

def deleteTrainFileDir(trainingfilePath):
    if(trainingfilePath is not None):
        parent_dir = os.path.dirname(trainingfilePath)
        shutil.rmtree(parent_dir)
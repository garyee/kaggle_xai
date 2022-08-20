import os
import shutil
from utils.kaggleEnums import baseTmpPath,KaggleEntityType, getKaggleEntityString, getPathNameFromKaggleRef, isArchiveFile
from utils.kaggleHelper import bash,kaggleCommand2DF
from utils.webStuff import acceptCompetitionRules

def downloadDataSetFilesByDataSetRef(dataSetRef,dataSetType =KaggleEntityType.DATASET):
  command ='kaggle '+getKaggleEntityString(dataSetType,True)+' files '+dataSetRef
  fileList = kaggleCommand2DF(command)
  downloadedAtLeastOneFile=False
  for fileName in list(fileList.iloc[:,0]):
    isZip=isArchiveFile(fileName)
    if(fileName.strip().lower()=='train.csv'):
      filePath=downloadOneFile(dataSetRef,dataSetType,fileName,isZip)
      downloadedAtLeastOneFile=True
      return filePath
    # if re.match(r'.*train.*\..*', fileName.strip().lower()):
    #   print(dataSetRef+' '+fileName)
  if(not downloadedAtLeastOneFile):
    print('No file found for: '+getKaggleEntityString(dataSetType)+' '+dataSetRef)
  return None

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
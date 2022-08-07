import os
import re
import shutil
from utils.DataSetTypes import DataSetTypes
from utils.kaggleEnums import tmpPath,KaggleEntityType,getKaggleEntityBasePath,getKaggleEntityString,getPathNameFromKaggleRef, isArchiveFile,testKernelsRefs
from utils.kaggleHelper import bash,kaggleCommand2DF
#from tqdm.notebook import tqdm
from tqdm import tqdm

from utils.webStuff import acceptCompetitionRules

def getTestKernels():
    for middleEntityType,kernelDict in testKernelsRefs.keys():
      for middleEntityRef,kernelRef in kernelDict.keys():
        downloadKernelByRef(kernelRef,middleEntityRef,middleEntityType)

def getAllKernelsForKaggleMostVotedEntity(entityType=KaggleEntityType.DATASET,page=1):
  sortStr=''
  if(entityType==KaggleEntityType.DATASET):
    sortStr='--sort-by votes'
  elif(entityType==KaggleEntityType.COMPETITION):
    sortStr='--sort-by numberOfTeams'
  commandStr='kaggle '+getKaggleEntityString(entityType,True)+' list -s tabular'
  pagination(commandStr,getKernelsByParentEntity,entityType.getPageSize(),entityType)
    
  
  # while kernelList4CurrDataSet.shape[0]!=i:
  # while entityList.shape[0]!=i:
  #   for currentDataSetRef in tqdm(list(mostVotedEntityList.iloc[:,0])):
  #     getKernelsByParentEntity('tring(entityType)+' '+currentDataSetRef,currentDataSetRef,entityType)

def getKernelsByParentEntity(currentDataSetRef,entityType,_=None):
    commandStr='kaggle kernels list --language python --sort-by voteCount --'+getKaggleEntityString(entityType)+' '+currentDataSetRef
    pagination(commandStr,downloadKernelByRef,KaggleEntityType.KERNEL.getPageSize(),currentDataSetRef,entityType)
    
    # print(currentDataSetRef)
    # kernelList4CurrDataSet = kaggleCommand2DF(commandStr)
    # page=1
    # i=0
    # # if(kernelList4CurrDataSet.shape[0]>30):
    # pbar=tqdm(total=kernelList4CurrDataSet.shape[0])
    # while kernelList4CurrDataSet.shape[0]!=i:
    #   currentKernelRef=kernelList4CurrDataSet.iloc[i,0]
    #   status=downloadKernelByRef(currentKernelRef,currentDataSetRef,entityType)
    #   # print(str(page)+'-'+str(kernelList4CurrDataSet.shape[0])+'-'+str(i)+': '+status)
    #   pbar.update(1)
    #   i+=1
    #   if(i%kernelListPageSize==0):
    #     pbar.refresh()
    #     kernelList4CurrDataSet = kaggleCommand2DF('kaggle kernels list --language python --sort-by voteCount --page '+str(page)+' --page-size '+str(kernelListPageSize)+' --'+getKaggleEntityString(entityType)+' '+currentDataSetRef)
    #     pbar.total = pbar.total+kernelList4CurrDataSet.shape[0]
    #     i=0
    #     page+=1
    # pbar.close()

def getCommandStr(original,page,pageSize):
  tempCommandStr=original+' --page '+str(page)
  if(pageSize>20):
    tempCommandStr+=' --page-size '+str(pageSize)
  return tempCommandStr

def pagination(commandStr,callback,entityTypePageSize,param1,param2=None):
  page=1
  currentList = kaggleCommand2DF(getCommandStr(commandStr,page,entityTypePageSize))
  i=0
  pbar=tqdm(total=currentList.shape[0])
  while currentList.shape[0]!=i:
    # currentKernelRef=currentList.iloc[i,0]
    callback(currentList.iloc[i,0],param1,param2)
    pbar.update(1)
    i+=1
    if(i%entityTypePageSize==0):
      pbar.refresh()
      currentList = kaggleCommand2DF(kaggleCommand2DF(getCommandStr(commandStr,page,entityTypePageSize)))
      pbar.total = pbar.total+currentList.shape[0]
      i=0
      page+=1
    pbar.close()

def downloadKernelByRef(kernelRef,parentEntitySetRef,parentEntityType=KaggleEntityType.DATASET):
  path4currentKernel=getKernelPath(kernelRef,parentEntitySetRef,parentEntityType)
  if(not os.path.exists(path4currentKernel)):
    res=bash('kaggle kernels pull '+kernelRef+' -p '+path4currentKernel)
    # if 'Source code downloaded' not in res:
    #   if('404 - Not Found' in res:
  else:
    print('skipped '+kernelRef)

def getKernelPath(kernelRef,middleEntityRef='',parentEntityType=KaggleEntityType.DATASET):
  kernelRefDirName=getPathNameFromKaggleRef(kernelRef)
  middleRefDirName=getPathNameFromKaggleRef(middleEntityRef)
  pathStump=getKaggleEntityBasePath(parentEntityType)+'/'+middleRefDirName+'/'
  if(parentEntityType==KaggleEntityType.NONE):
    pathStump=getKaggleEntityBasePath(parentEntityType)+'/'
  if(not os.path.exists(pathStump)):
    os.mkdir(pathStump)
  return pathStump+kernelRefDirName+'/'

def getDataSetPath(dataSetRef):
  middleRefDirName=getPathNameFromKaggleRef(dataSetRef)
  pathStump=getKaggleEntityBasePath(KaggleEntityType.DATASET)+'/'+middleRefDirName+'/'
  if(not os.path.exists(pathStump)):
    os.mkdir(pathStump)
  return pathStump

def deleteDataSetFolder(dataSetRef):
  dataSetPath=getDataSetPath(dataSetRef)
  if os.path.exists(dataSetPath) and os.access(dataSetPath, os.W_OK):
    # shutil.rmtree(dataSetPath,ignore_errors=False,onerror=retryDeletingFile)
    shutil.rmtree(dataSetPath,ignore_errors=True)
    print ("Directory deleted: "+dataSetPath)
  else:
      print ("Directory does not exist or is not accessable: "+dataSetPath)

# def retryDeletingFile(func, path, exc):
#   import stat
#   # Is the error an access error?
#   if not os.access(path, os.W_OK):
#     os.chmod(path, stat.S_IWUSR)
#     func(path)
#   else:
#     raise Exception('File could not be deleted even on second try: '+path)



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
  return tmpPath+getPathNameFromKaggleRef(dataSetRef)+"/"

def deleteTrainFileDir(trainingfilePath):
  if(trainingfilePath is not None):
    parent_dir = os.path.dirname(trainingfilePath)
    shutil.rmtree(parent_dir)

getAllKernelsForKaggleMostVotedEntity(KaggleEntityType.DATASET,34)
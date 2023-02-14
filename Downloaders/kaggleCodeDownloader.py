import os
import re
import shutil
from utils.DownloaderErrors import PageDoesNotExistError
from utils.kaggleEnums import KaggleEntityType,getKaggleEntityBasePath,getKaggleEntityString,getPathNameFromKaggleRef, testKernelsRefs
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
  pagination(commandStr,getKernelsByParentEntity,entityType,entityType,None,page)
  
def getKernelsByParentEntity(currentDataSetRef,entityType,_=None):
    commandStr='kaggle kernels list --language python --sort-by voteCount --'+getKaggleEntityString(entityType)+' '+currentDataSetRef
    pagination(commandStr,downloadKernelByRef,KaggleEntityType.KERNEL,currentDataSetRef,entityType)
    
def getCommandStr(original,page,pageSize):
  tempCommandStr=original+' --page '+str(page)
  if(pageSize>20):
    tempCommandStr+=' --page-size '+str(pageSize)
  return tempCommandStr

def pagination(commandStr,callback,paginatedType,param1,param2=None,startPage=1):
  page=startPage
  try:
    currentList = kaggleCommand2DF(getCommandStr(commandStr,page,paginatedType.getPageSize()))
  except PageDoesNotExistError:
    return
  i=0
  pbar=tqdm(total=currentList.shape[0])
  while i<currentList.shape[0]:
    if(paginatedType==KaggleEntityType.DATASET):
      print(getKaggleEntityString(paginatedType)+ ': ' + currentList.iloc[i,0]+' '+str(page))
    callback(currentList.iloc[i,0],param1,param2)
    pbar.update(1)
    i+=1
    if((currentList.shape[0])==i and currentList.shape[0]>0.5*paginatedType.getPageSize()):
      page+=1
      pbar.refresh()
      i=0
      try:
        currentList = kaggleCommand2DF(getCommandStr(commandStr,page,paginatedType.getPageSize()))
        pbar.total = pbar.total+currentList.shape[0]
      except PageDoesNotExistError:
            i=currentList.shape[0]+1
  pbar.close()

def downloadKernelByRef(kernelRef,parentEntitySetRef,parentEntityType=KaggleEntityType.DATASET):
  path4currentKernel=getKernelPath(kernelRef,parentEntitySetRef,parentEntityType)
  if(not os.path.exists(path4currentKernel)):
    res=bash('kaggle kernels pull '+kernelRef+' -p '+path4currentKernel)
    # if 'Source code downloaded' not in res:
    #   if('404 - Not Found' in res:
  # else:
    #print('skipped '+kernelRef)

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


import os
import re
import shutil
from utils.CustomExceptions import PageDoesNotExistError
from utils.KaggleCommands.KaggleCommand import KaggleCommand, KaggleCommandOperations
from utils.kaggleEnums import KaggleEntityType,getKaggleEntityBasePath,getKaggleEntityString,getPathNameFromKaggleRef, testKernelsRefs
#from tqdm.notebook import tqdm
from tqdm import tqdm

from utils.webStuff import acceptCompetitionRules

def getTestKernels():
    for middleEntityType,kernelDict in testKernelsRefs.keys():
      for middleEntityRef,kernelRef in kernelDict.keys():
        downloadKernelByRef(kernelRef,middleEntityRef,middleEntityType)

def getAllKernelsForKaggleMostVotedEntity(entityType=KaggleEntityType.DATASET,page=1,sortStr=''):
  # commandStr='kaggle '+getKaggleEntityString(entityType,True)+' list -s tabular'+sortStr
  command= KaggleCommand.buildCommand(entityType, KaggleCommandOperations.LIST,{"sort-by":sortStr})
  pagination(command,getKernelsByParentEntity,entityType,entityType,None,page)
  
def cleanDataSetRef(ref):
  if(ref.startswith("https://www.kaggle.com/")):
    return ref.rsplit('/', 1)[-1]
  else:
    return ref

def getKernelsByParentEntity(currentEntityRef,entityType,_=None):
    # commandStr='kaggle kernels list --language python --sort-by voteCount --'+getKaggleEntityString(entityType)+' '+currentDataSetRef
    params={"sort-by":"voteCount","language":"python"}
    params[getKaggleEntityString(entityType)]=currentEntityRef;
    command = KaggleCommand.buildCommand(
      KaggleEntityType.KERNEL,
      KaggleCommandOperations.LIST,
      params,currentEntityRef)
    pagination(command,downloadKernelByRef,KaggleEntityType.KERNEL,currentEntityRef,entityType)
    
# def getCommandStr(original,page,pageSize):
#   tempCommandStr=original+' --page '+str(page)
#   if(pageSize>20):
#     tempCommandStr+=' --page-size '+str(pageSize)
#   return tempCommandStr

def pagination(command,callback,paginatedType,param1,param2=None,startPage=1):
  page=startPage
  try:
    # currentList = kaggleCommand2DF(getCommandStr(commandStr,page,paginatedType.getPageSize()))
    command.parameters={'page':page,"page-size":paginatedType.getPageSize()}
    currentList = command.execute()
  except PageDoesNotExistError:
    return
  i=0
  pbar=tqdm(total=len(currentList))
  while i<len(currentList):
    if(paginatedType==KaggleEntityType.DATASET):
      print(getKaggleEntityString(paginatedType)+ ': ' + currentList[i].ref+' '+str(page))
    callback(cleanDataSetRef(currentList[i].ref),param1,param2)
    pbar.update(1)
    i+=1
    if((len(currentList))==i and len(currentList)>0.5*paginatedType.getPageSize()):
      page+=1
      pbar.refresh()
      i=0
      try:
        # currentList = kaggleCommand2DF(getCommandStr(commandStr,page,paginatedType.getPageSize()))
        command.parameters={'page':page,"page-size":paginatedType.getPageSize()}
        currentList = command.execute()
        pbar.total = pbar.total+len(currentList)
      except PageDoesNotExistError:
            i=len(currentList)+1
  pbar.close()

def downloadKernelByRef(kernelRef,parentEntitySetRef,parentEntityType=KaggleEntityType.DATASET):
  path4currentKernel=getKernelPath(kernelRef,parentEntitySetRef,parentEntityType)
  if(not os.path.exists(path4currentKernel)):
    os.makedirs(path4currentKernel)
    command=KaggleCommand.buildCommand(KaggleEntityType.KERNEL,KaggleCommandOperations.DOWNLOAD,{'path':path4currentKernel},kernelRef)
    res = command.execute()
    f = open(path4currentKernel+res['metadata']['slug']+'.ipynb', "w")
    f.write(res['blob']['source'])
    f.close()
    # res=bash('kaggle kernels pull '+kernelRef+' -p '+path4currentKernel)
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


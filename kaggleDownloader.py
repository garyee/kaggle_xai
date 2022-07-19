import os
from kaggleEnums import KaggleEntityType,getKaggleEntityBasePath,getKaggleEntityString,getPathNameFromKaggleRef,kernelListPageSize,testKernelsRefs
from kaggleHelper import bash,kaggleCommand2DF
#from tqdm.notebook import trange, tqdm
from tqdm import tqdm

def getTestKernels():
    for middleEntityType,kernelDict in testKernelsRefs.keys():
      for middleEntityRef,kernelRef in kernelDict.keys():
        downloadKernelByRef(kernelRef,middleEntityRef,middleEntityType)

def getAllKernelsForKaggleMostVotedEntity(entity=KaggleEntityType.DATASET,page=1):
  sortStr=''
  if(entity==KaggleEntityType.DATASET):
    sortStr='--sort-by votes'
  elif(entity==KaggleEntityType.COMPETITION):
    sortStr='--sort-by numberOfTeams'
  mostVotedEntityList = kaggleCommand2DF('kaggle '+getKaggleEntityString(entity,True)+' list '+sortStr)
  for currentDataSetRef in tqdm(list(mostVotedEntityList.iloc[:,0])):
    getKernelsByParentEntity('kaggle kernels list --sort-by voteCount --page '+str(page)+' --page-size '+str(kernelListPageSize)+' --'+getKaggleEntityString(entity)+' '+currentDataSetRef,currentDataSetRef,entity)

def getKernelsByParentEntity(commandStr,currentDataSetRef,entityType):
    print(currentDataSetRef)
    kernelList4CurrDataSet = kaggleCommand2DF(commandStr)
    page=1
    i=0
    pbar=tqdm(total=kernelList4CurrDataSet.shape[0])
    while kernelList4CurrDataSet.shape[0]!=i:
      currentKernelRef=kernelList4CurrDataSet.iloc[i,0]
      status=downloadKernelByRef(currentKernelRef,currentDataSetRef,entityType)
      # print(str(page)+'-'+str(kernelList4CurrDataSet.shape[0])+'-'+str(i)+': '+status)
      pbar.update(1)
      i+=1
      if(i%kernelListPageSize==0):
        pbar.refresh()
        kernelList4CurrDataSet = kaggleCommand2DF('kaggle kernels list --language python --sort-by voteCount --page '+str(page)+' --page-size '+str(kernelListPageSize)+' --'+getKaggleEntityString(entityType)+' '+currentDataSetRef)
        pbar.total = pbar.total+kernelList4CurrDataSet.shape[0]
        i=0
        page+=1
    pbar.close()

def downloadKernelByRef(kernelRef,parentEntitySetRef,parentEntityType=KaggleEntityType.DATASET):
  path4currentKernel=getKernelPath(kernelRef,parentEntitySetRef,parentEntityType)
  if(not os.path.exists(path4currentKernel)):
    res=bash('kaggle kernels pull '+kernelRef+' -p '+path4currentKernel)
  #   print(res)
    return "downloaded"
  else:
  #   print('skipped '+currentKernelRef)
    return "skipped"

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
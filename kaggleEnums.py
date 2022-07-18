from enum import Enum
import os

class KaggleEntityType(Enum):
  DATASET = 1
  COMPETITION = 2
  NONE = 3

class KernelLanguage(Enum):
  PYTHON = 1
  NONE = 2

parentEntityPathStrList=['datasets','competitions','none']

basePath= '/content/drive/MyDrive/Colab/Kaggle/kernels/'
basePathPerDataSet= basePath+'datasets'
basePathPerCompetitions= basePath+'competitions'
basePathNone= basePath+'none'

if(not os.path.exists(basePathPerDataSet)):
    os.mkdir(basePathPerDataSet)
if(not os.path.exists(basePathPerCompetitions)):
  os.mkdir(basePathPerCompetitions)
if(not os.path.exists(basePathNone)):
  os.mkdir(basePathNone)

def getKaggleEntityString(entity,multiple=False):
  if entity==KaggleEntityType.DATASET:
    if multiple:
      return 'databases'
    else:
      return 'database'
  elif entity==KaggleEntityType.COMPETITION:
    if multiple:
      return 'competitions'
    else:
      return 'competition'
  return ''

def getKaggleEntityTypeFromString(entityStr):
  if entityStr=='databases' or entityStr=='database':
    return KaggleEntityType.DATASET
  if entityStr=='competitions' or entityStr=='competition':
      return KaggleEntityType.COMPETITION
  if entityStr=='none':
      return KaggleEntityType.NONE
  raise Exception("EntityStr not recognized!")

def getAllInfoFromKernelPath(filePath):
  if basePath not in filePath:
    print(filePath+'is not a kernel path1!')
    return
  currentPathStr=filePath.replace(basePath,'')
  pathPartsList=currentPathStr.split('/')
  if pathPartsList[0] not in parentEntityPathStrList:
    print(filePath+'is not a kernel path2!')
    return
  parentEntityType=getKaggleEntityTypeFromString(pathPartsList[0])
  if parentEntityType==KaggleEntityType.NONE and len(pathPartsList)==3:
    entityRef=getKaggleRefFromFilePathPartStr(pathPartsList[1])
    kernelFileName=pathPartsList[2]
    parentEntityRef=None
  elif len(pathPartsList)==4:
    parentEntityRef=pathPartsList[1]
    entityRef=getKaggleRefFromFilePathPartStr(pathPartsList[2])
    kernelFileName=pathPartsList[3]
  else:
    print(filePath+'is not a kernel path3!')
    return
  return parentEntityType,parentEntityRef,entityRef,kernelFileName
  


def getKaggleEntityBasePath(entityType=KaggleEntityType.DATASET):
  if entityType==KaggleEntityType.COMPETITION:
      return basePathPerCompetitions
  elif entityType==KaggleEntityType.DATASET:
    return basePathPerDataSet
  else:
    return basePathNone

def getPathNameFromKaggleRef(kaggleRef):
  return kaggleRef.replace('/','_____')

def getKaggleRefFromFilePathPartStr(filePathPart):
  return filePathPart.replace('_____','/')
from enum import Enum
import os

class KaggleEntityType(Enum):
  DATASET = 1
  COMPETITION = 2
  NONE = 3

def getEntityTypeFromString(str):
    if(str==1):
        return KaggleEntityType.COMPETITION
    elif(str==0):
        return KaggleEntityType.DATASET
    return KaggleEntityType.NONE

def getIsCompetitionfromEntityType(type):
    if(type==KaggleEntityType.COMPETITION):
        return 1
    return 0

class KernelLanguage(Enum):
  PYTHON = 1
  NONE = 2

kernelListPageSize=100

testKernelsRefs={KaggleEntityType.DATASET: {},
                 KaggleEntityType.COMPETITION:{
                  'titanic':'vbmokin/merging-fe-prediction-xgb-lgb-logr-linr',
                  'widsdatathon2022':'shreyasajal/wids-datathon-2022-explainable-ai-walkthrough'
                 },
                 KaggleEntityType.NONE: {'none1':'datacog314/tutorial-machine-learning-interpretability',
                                         'none2':'devsubhash/explainable-ai-using-explainerdashboard'}
                }
#vbmokin/merging-fe-prediction-xgb-lgb-logr-linr - ['PH_PFI', 'PH_SHAP']

parentEntityPathStrList=['datasets','competitions','none']

#filePath= '/content/drive/MyDrive/Colab'
filePath="C:/Users/garyee/gDrive/Colab/Kaggle/"
basePath= filePath+'kernels/'
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
      return 'datasets'
    else:
      return 'dataset'
  elif entity==KaggleEntityType.COMPETITION:
    if multiple:
      return 'competitions'
    else:
      return 'competition'
  return ''

def getKaggleEntityTypeFromString(entityStr):
  if entityStr=='datasets' or entityStr=='dataset':
    return KaggleEntityType.DATASET
  if entityStr=='competitions' or entityStr=='competition':
      return KaggleEntityType.COMPETITION
  if entityStr=='none':
      return KaggleEntityType.NONE
  raise Exception("EntityStr not recognized!")

def getAllInfoFromKernelPath(filePath):
  if basePath not in filePath:
    print(filePath+' is not a kernel path1!')
    return
  currentPathStr=filePath.replace(basePath,'')
  # pathPartsList=currentPathStr.split('/')
  normalized_path = os.path.normpath(currentPathStr)
  pathPartsList = normalized_path.split(os.sep)
  # pathPartsList=os.path.split(currentPathStr)
  if pathPartsList[0] not in parentEntityPathStrList:
    print(filePath+' is not a kernel path2!')
    return
  parentEntityType=getKaggleEntityTypeFromString(pathPartsList[0])
  if parentEntityType==KaggleEntityType.NONE and len(pathPartsList)==3:
    entityRef=getKaggleRefFromFilePathPartStr(pathPartsList[1])
    kernelFileName=pathPartsList[2]
    parentEntityRef=None
  elif len(pathPartsList)==4:
    parentEntityRef=getKaggleRefFromFilePathPartStr(pathPartsList[1])
    entityRef=getKaggleRefFromFilePathPartStr(pathPartsList[2])
    kernelFileName=pathPartsList[3]
  else:
    print(filePath+' is not a kernel path3!')
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

metaDataGoal=['regression','classification']

def getAllKnownExtensions():
    return ['csv',
            'xls',
            'xlsx',
            'npy',
            'parquet',
            'paruqet',
            'npz',
            'tsv',
            'json',
            'db',
            'sqlite',
            'jpg',
            'gif',
            'png',
            'mpg',
            'mp4',
            'mpeg',
            'tfrec',
            'txt',
            'pdf',
            'sh',
            'py',
            'md',
            'pkl',
            'r',
            'zip',
            'gz',
            'readme',
            'bz2',
            'm',
            'h5',
            'docx',
            'so',
            'encrypted',
            'dcm',
            'torrent',
            '7z',
            'xyz',
            'rtf',
            'tif',
            'mp3',
            ]


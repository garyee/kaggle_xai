import os
import pandas as pd
from io import StringIO
from utils.DataSetTypes import DataSetTypes
from utils.DownloaderErrors import PageDoesNotExistError
import subprocess

def bash(command):
    x = subprocess.check_output(command)
    # # charDectRes=chardet.detect(x)
    resStr=x.decode('utf-8')
    return resStr
    # output = os.popen(command).read()
    # return output

def kaggleCommand2DF(command):
  result=bash(command+" --csv")
  if('No datasets found' in result or 'No kernels found' in result):
    raise PageDoesNotExistError(command)
  return pd.read_csv(StringIO(result))

def setTypeAndCertainty(type,typeCertainty,resDict):
  resDict['type'],resDict['type_certainty']=getTypeAndCertainty(type,typeCertainty,resDict.get('type'),resDict.get('type_certainty'))

def getTypeAndCertainty(type,typeCertainty,resTypeStr=None,resSetCertainty=None):
    if(resTypeStr is not None and resSetCertainty is not None):
        resType=DataSetTypes(resTypeStr)
        if(type==resType):
            return type.value,max(typeCertainty,resSetCertainty)
        if(resSetCertainty>typeCertainty):
            return resType.value,resSetCertainty
    return type.value,typeCertainty
import os
import pandas as pd
from io import StringIO

from kaggleDownloader import getDataSetPath
from utils.DataSetTypes import DataSetTypes

def bash(command):
    output = os.popen(command).read()
    return output

def kaggleCommand2DF(command):
  result=bash(command+" --csv")
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

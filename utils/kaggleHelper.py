import os
import pandas as pd
from io import StringIO

def bash(command):
    output = os.popen(command).read()
    return output

def kaggleCommand2DF(command):
  result=bash(command+" --csv")
  return pd.read_csv(StringIO(result))

def setTypeAndCertainty(type,typeCertainty,resDict):
  resDict['type'],resDict['type_certainty']=getTypeAndCertainty(type,typeCertainty,resDict.get('type'),resDict.get('type_certainty'))



def getTypeAndCertainty(type,typeCertainty,resType=None,resSetCertainty=None):
    if(resType is not None and resSetCertainty is not None):
        if(type==resType):
            return type.value,max(typeCertainty,resSetCertainty)
        if(resSetCertainty>typeCertainty):
            return resType.value,resSetCertainty
    return type.value,typeCertainty
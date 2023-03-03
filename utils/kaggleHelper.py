import json
import os
import pandas as pd
from io import StringIO
from utils.DataSetTypes import DataSetTypes
from utils.DownloaderErrors import PageDoesNotExistError
import subprocess

def bash(command):
  try:
    x = subprocess.check_output(command)
    resStr=x.decode('utf-8')
  except subprocess.CalledProcessError:
    print('there has been an subprocess error with: '+command)
    resStr=None
    # # charDectRes=chardet.detect(x)
  return resStr
    # output = os.popen(command).read()
    # return output

def kaggleCommand2DF(command):
  result=bash(command+" --csv")
  if(result is None):
    return pd.DataFrame();
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

def writeToWordCountJson(word,filename):
  filename=filename+'.json'
  words={}

  if os.path.exists(filename):
    with open(filename) as f:
      try:
        words = json.load(f)
      except (ValueError) as e:
        words = {}
    
  with open(filename, 'w') as fw:
    if(word in words):
      words[word]+=1
    else:
      words[word]=1
    json.dump(words, fw, indent=4,sort_keys=True)

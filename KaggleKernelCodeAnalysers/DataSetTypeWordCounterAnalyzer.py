from itertools import count
import re
from KaggleKernelCodeAnalysers.KaggleKernelCodeAnalyzer import KaggleKernelCodeAnalyzer
from utils.kaggleEnums import KaggleEntityType
from utils.DataSetTypes import DataSetTypes
from utils.kaggleHelper import setTypeAndCertainty

class DataSetTypeWordCounterAnalyzer(KaggleKernelCodeAnalyzer):

  CELLTYPEFILTERARR = []

  def __init__(self):
    self._type_vote_per_data_set = {}
    self._kernel_matches = {}
    self._kernel_count = 0

  def analyseCell(self,sourceCell):
    for dataSetType in DataSetTypes:
      regexArr= dataSetType.getWordCountRefExes()
      if(len(regexArr)>0):
        for typeRegex in regexArr:
          if re.search(typeRegex, sourceCell.strip().lower()) is not None:
            regExMatchCount=len(re.findall(typeRegex, sourceCell.strip().lower()))
            # if(regExMatchCount>1):
            if(dataSetType not in self._kernel_matches):
              self._kernel_matches[dataSetType]=regExMatchCount
            else:
              self._kernel_matches[dataSetType]=+regExMatchCount

  def onLastCell(self):
    maxType=None
    maxCount=0
    for dataType, count in self._kernel_matches.items():
      if(count>maxCount):
        maxType=dataType
        maxCount=count
    if(maxType is not None):
      if(maxType not in self._type_vote_per_data_set):
        self._type_vote_per_data_set[maxType] = 1
      else:
        self._type_vote_per_data_set[maxType] += 1
    self._kernel_matches={}
    self._kernel_count+=1    

  def onDataSetChanged(self,resultDataSetDict):
    dataSetFinalType=None
    dataSetFinalCount=0
    for dataType, count in self._type_vote_per_data_set.items():
      if(count>dataSetFinalCount):
        dataSetFinalType=dataType
        dataSetFinalCount=count
    if(dataSetFinalType is not None and self._kernel_count>30):
      countToOverAllRatio=dataSetFinalCount/self._kernel_count
      typeCertainty=min(int(countToOverAllRatio*100),dataSetFinalType.getWordCountCertanties())
      setTypeAndCertainty(dataSetFinalType,typeCertainty,resultDataSetDict)
    self._type_vote_per_data_set={}
    self._kernel_count=0


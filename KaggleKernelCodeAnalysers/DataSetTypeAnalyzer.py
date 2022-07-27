from itertools import count
import re
from KaggleKernelCodeAnalysers.KaggleKernelCodeAnalyzer import KaggleKernelCodeAnalyzer
from utils.kaggleEnums import DataSetTypes, KaggleEntityType
from utils.kaggleHelper import setTypeAndCertainty

class DataSetTypeAnalyzer(KaggleKernelCodeAnalyzer):

  typeVotePerDataSet={}
  countMatchPerTypeOverAllCellsPerKernel={}
  
  def analyseCell(self,sourceCell,isLastCell,currentDataSetChanged,resultKernelDict,resultDataSetDict):
    dataSetFinalType=None
    dataSetFinalCount=0
    maxType=None
    maxCount=0
    for dataSetType in DataSetTypes:
      regexArr= dataSetType.getSourceCodeRegExes()
      if(len(regexArr)>0):
        for typeRegex in regexArr:
          if re.search(typeRegex, sourceCell.strip().lower()) is not None:
            regExMatchCount=len(re.findall(typeRegex, sourceCell.strip().lower()))
            if(dataSetType not in self.countMatchPerTypeOverAllCellsPerKernel):
              self.countMatchPerTypeOverAllCellsPerKernel[dataSetType]=regExMatchCount
            else:
              self.countMatchPerTypeOverAllCellsPerKernel[dataSetType]=+regExMatchCount
    if(isLastCell):
      for dataType, count in self.countMatchPerTypeOverAllCellsPerKernel.items():
        if(count>maxCount):
          maxType=dataType
          maxCount=count
      if(maxType is not None):
        if(maxType not in self.typeVotePerDataSet):
          self.typeVotePerDataSet[maxType] = 1
        else:
          self.typeVotePerDataSet[maxType] += 1
      self.countMatchPerTypeOverAllCellsPerKernel={}
      maxType=None
      maxCount=0
      #will be None for the frist kernel of the first DS
      if(currentDataSetChanged==True):
        for dataType, count in self.typeVotePerDataSet.items():
          if(count>dataSetFinalCount):
            dataSetFinalType=dataType
            dataSetFinalCount=count
        if(dataSetFinalType is not None):
          setTypeAndCertainty(dataSetFinalType,dataSetFinalType.getCodeTypeCertanties(),resultDataSetDict)
        self.typeVotePerDataSet={}
        dataSetFinalType=None
        dataSetFinalCount=0

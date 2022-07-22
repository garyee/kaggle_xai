import re
from KaggleKernelCodeAnalysers.KaggleKernelCodeAnalyzer import KaggleKernelCodeAnalyzer
from kaggleEnums import DataSetTypes

class DataSetTypeAnalyzer(KaggleKernelCodeAnalyzer):

  
  def __init__(self, regExMatchCountPerType={}):
    self.regExMatchCountPerType = regExMatchCountPerType

  def analyseCell(self,cell,cellType):
    for dataSetType in DataSetTypes:
      regexArr= dataSetType.getSourceCodeRegExes()
      if(len(regexArr)>0):
        for typeRegex in regexArr:
          if re.search(typeRegex, ) is not None:
            regExMatchCount=len(re.findall(typeRegex, cell.strip().lower()))
            if(dataSetType not in self.regExMatchCountPerType):
              self.regExMatchCountPerType[dataSetType]=regExMatchCount
            else:
              self.regExMatchCountPerType[dataSetType]=+regExMatchCount
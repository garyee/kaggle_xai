from itertools import count
import re
from KaggleKernelCodeAnalysers.KaggleKernelCodeAnalyzer import KaggleKernelCodeAnalyzer
from utils.kaggleEnums import KaggleEntityType
from utils.DataSetTypes import DataSetTypes
from utils.kaggleHelper import setTypeAndCertainty

class DataSetTargetColumnNameFinder(KaggleKernelCodeAnalyzer):

  CELLTYPEFILTERARR = ['code']

  def __init__(self):
    self.dataFrameName = None
    self.targetName=None
    self.targetNameVoteArr={}
  
  def analyseCell(self,sourceCell):
    if(self.targetName is None):
        dataFrameNameRegex=r"(\S+)\s*=.*pd\.read_csv\(.*train.*\)"
        targetColumnName=None
        
        regExMatchCount=re.findall(dataFrameNameRegex, sourceCell.strip().lower())
        if(len(regExMatchCount)>=1 and self.dataFrameName is None):
            self.dataFrameName=regExMatchCount[0]
        
        if(self.dataFrameName is not None):
            yTargetRegex=r"([.\S]+)\s*=\s*"+self.dataFrameName+"\[['|\"](.*)['|\"]]"
            yTargetMatchCount=re.findall(yTargetRegex, sourceCell.strip().lower())
            if(len(yTargetMatchCount)>=1 ):
                firstMatch=yTargetMatchCount[0]
                targetVariableName=firstMatch[0]
                targetColumnName=firstMatch[1]

        if(targetColumnName is not None):
            self.targetName=targetColumnName

        
    # for dataSetType in DataSetTypes:
    #   regexArr= dataSetType.getWordCountRefExes()
    #   if(len(regexArr)>0):
    #     for typeRegex in regexArr:
    #       if re.search(typeRegex, sourceCell.strip().lower()) is not None:
    #         regExMatchCount=len(re.findall(typeRegex, sourceCell.strip().lower()))
    #         if(regExMatchCount>1):
    #           if(dataSetType not in self._kernel_matches):
    #             self._kernel_matches[dataSetType]=regExMatchCount
    #           else:
    #             self._kernel_matches[dataSetType]=+regExMatchCount

  def onLastCell(self,resultKernelDict):
    if(self.targetName is not None):
        if(self.targetName not in self.targetNameVoteArr):
            self.targetNameVoteArr[self.targetName]=1
        else:
            self.targetNameVoteArr[self.targetName]+=1
    self.dataFrameName=None
    self.targetName=None

  def onDataSetChanged(self,resultDataSetDict):
    targetNameMaxCount=0
    targetNameWinner=None
    if(len(self.targetNameVoteArr.keys())>0):
        for targetName in self.targetNameVoteArr.keys():
            count=self.targetNameVoteArr[targetName]
            if(count>targetNameMaxCount):
                targetNameWinner=targetName
                targetNameMaxCount=count
        if(targetNameWinner is not None):
            resultDataSetDict['tab_target_col']=targetNameWinner
    self.targetNameVoteArr={}


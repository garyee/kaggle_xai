from itertools import count
import re
from KaggleKernelCodeAnalysers.KaggleKernelCodeAnalyzer import KaggleKernelCodeAnalyzer
from utils.kaggleEnums import KaggleEntityType
from utils.DataSetTypes import DataSetTypes
from utils.kaggleHelper import setTypeAndCertainty, writeToWordCountJson

class DataSetTargetColumnNameFinder(KaggleKernelCodeAnalyzer):

  CELLTYPEFILTERARR = ['code']
  possibleTargetVariableNames=['y','Y','y_train','Y_train','target']

  def __init__(self):
    self.dataFrameName = None
    self.targetName=None
    self.targetNameVoteArr={}
    self.modelsTrained=0
    self.predictionsMade=0
    self.kernelsWhichTrainOrPredictedCount=0
  
  def analyseCell(self,sourceCell):
    #Detect targetVariable
    if(self.targetName is None):
        dataFrameNameRegex=r"(\S+)\s*=.*pd\.read_csv\(.*train.*\)"
        targetColumnName=None
        
        regExMatchCount=re.findall(dataFrameNameRegex, sourceCell.strip().lower())
        if(len(regExMatchCount)>=1 and self.dataFrameName is None):
            self.dataFrameName=regExMatchCount[0]
        
        
        if(self.dataFrameName is not None):
          #"([A-Za-z0-9_]+)\s*=\s*"+self.dataFrameName+"\[['|\"]([^]]*)['|\"]]"
            yTargetRegex=r"([A-Za-z0-9_]+)\s*=\s*"+self.dataFrameName+"\[['|\"]([^]]*)['|\"]]"
            yTargetMatchCount=re.findall(yTargetRegex, sourceCell.strip().lower())
            if(len(yTargetMatchCount)>=1 ):
                firstMatch=yTargetMatchCount[0]
                targetVariableName=firstMatch[0]
                targetColumnName=firstMatch[1]

        if(targetColumnName is not None):
            self.targetName=targetColumnName

    #detect fit/train
    trainRegex=r"\.fit\("
    modelsTrainedMatchCount=re.findall(trainRegex, sourceCell.strip().lower())
    if(len(modelsTrainedMatchCount)>=1 ):
      self.modelsTrained+=len(modelsTrainedMatchCount)

    predictRegex=r"\.predict\("
    predictionsMadeMatchCount=re.findall(predictRegex, sourceCell.strip().lower())
    if(len(predictionsMadeMatchCount)>=1 ):
      self.predictionsMade+=len(predictionsMadeMatchCount)
        
    #detect targetValueName
    #TODO
        
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

  def onLastCell(self,resultKernelDict,kernelIndex):
    if(self.targetName is not None):
        writeToWordCountJson(self.targetName,'targetNamesCount')
        if(self.targetName not in self.targetNameVoteArr):
            self.targetNameVoteArr[self.targetName]=1
        else:
            self.targetNameVoteArr[self.targetName]+=1
    if(self.modelsTrained>0):
       resultKernelDict['modelsTrained']=self.modelsTrained
    if(self.predictionsMade>0):
      resultKernelDict['predictionsMade']=self.predictionsMade
    if(self.modelsTrained>0 or self.predictionsMade>0):
      self.kernelsWhichTrainOrPredictedCount+=1
    self.dataFrameName=None
    self.targetName=None
    self.modelsTrained=0
    self.predictionsMade=0


  def onDataSetChanged(self,resultDataSetDict,kernelCountPerDataSet):
    targetNameMaxCount=5
    targetNameWinner=None
    if(len(self.targetNameVoteArr.keys())>0):
        for targetName in self.targetNameVoteArr.keys():
            count=self.targetNameVoteArr[targetName]
            if(count>targetNameMaxCount):
                targetNameWinner=targetName
                targetNameMaxCount=count
        if(targetNameWinner is not None):
            resultDataSetDict['tab_target_col']=targetNameWinner
    if(self.kernelsWhichTrainOrPredictedCount>0):
            proba=self.kernelsWhichTrainOrPredictedCount/kernelCountPerDataSet*100
            if(proba>100):
              print('proba error in:'+resultDataSetDict['dataSetRef'])
            resultDataSetDict['tab_has_target_propability']=int(proba)
    self.kernelsWhichTrainOrPredictedCount=0
    self.targetNameVoteArr={}


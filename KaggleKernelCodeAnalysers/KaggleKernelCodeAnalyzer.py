from abc import ABC, abstractmethod

class KaggleKernelCodeAnalyzer(ABC):
  
  @classmethod
  @property
  @abstractmethod
  def CELLTYPEFILTERARR(ctfa):
      raise NotImplementedError

  @classmethod
  @abstractmethod
  def analyseCell(self,sourceCode,cellType):
        pass

  @classmethod
  @abstractmethod
  def onDataSetChanged(self,resultDataSetDict):
        pass
  
  @classmethod
  @abstractmethod
  def onLastCell(self,resultKernelDict):
        pass

  def analyse(self,cells,resultKernelDict):
    #datasetChanges occur right before the first kernel of the new one
    indexOfLastSourceCell=None
    if(len(self.CELLTYPEFILTERARR)>0):
      for reverseIndex, cell in reversed(list(enumerate(cells))):
        if('cell_type' in cell and cell['cell_type'] in self.CELLTYPEFILTERARR):
          indexOfLastSourceCell=reverseIndex
          break
    else:
      indexOfLastSourceCell=len(cells)-1

    for index,cell in enumerate(cells):
      isLastCell=index==indexOfLastSourceCell if indexOfLastSourceCell is not None else index==len(cells)-1
      if(len(self.CELLTYPEFILTERARR)>0):
        if 'cell_type' in cell and cell['cell_type'] not in self.CELLTYPEFILTERARR:
          continue
      if 'source' in cell and cell['source'] is not None:
          if type(cell['source']) == str:
            self.analyseCell(cell['source'])
      if(isLastCell):
        self.onLastCell(resultKernelDict)
        break

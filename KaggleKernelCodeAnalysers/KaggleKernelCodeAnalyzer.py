from abc import ABC, abstractmethod

class KaggleKernelCodeAnalyzer(ABC):
  
  # @classmethod
  # @abstractmethod
  # def getHeader(self):
  #       pass

  @classmethod
  @abstractmethod
  def analyseCell(self,sourceCode,cellType):
        pass

  def analyse(self,cells,currentDataSetChanged,resultKernelDict,resultDataSetDict):
    indexOfLastSourceCell=None
    for reverseIndex, cell in reversed(list(enumerate(cells))):
      if('cell_type' in cell and cell['cell_type'] == 'code'):
        indexOfLastSourceCell=reverseIndex
        break
    for index,cell in enumerate(cells):
      isLastCell=index==indexOfLastSourceCell if indexOfLastSourceCell is not None else index==len(cells)-1
      if cell['cell_type'] == 'code' and 'source' in cell and cell['source'] is not None:
          if type(cell['source']) == str:
            self.analyseCell(cell['source'],isLastCell,currentDataSetChanged,resultKernelDict,resultDataSetDict)
      if(isLastCell):
        break

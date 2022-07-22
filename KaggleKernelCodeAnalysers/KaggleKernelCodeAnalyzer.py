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

  def analyse(self,kernelCode):
    for cell in kernelCode['cells']:
      if cell['cell_type'] == 'code' and 'source' in cell and cell['source'] is not None:
          if type(cell['source']) == str:
            self.analyse(cell['source'],cell['cell_type'])

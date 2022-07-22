from abc import ABC, abstractmethod

class KaggleDataSetAnalyser(ABC):
  
  # @classmethod
  # @abstractmethod
  # def getHeader(self):
  #       pass

  @classmethod
  @abstractmethod
  def analyse(self,entityRef,entityType,resDict):
        pass

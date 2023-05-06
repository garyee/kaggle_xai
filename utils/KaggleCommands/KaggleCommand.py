from enum import Enum
from utils.CustomExceptions import CommandTypDoesNotExist
from utils.KaggleCommands.initKaggleApi import getApi
from utils.kaggleEnums import KaggleEntityType
from abc import ABC, abstractmethod

# kaggle competitions {list, files, download, submit, submissions, leaderboard}
# kaggle datasets {list, files, download, create, version, init}
# kaggle kernels {list, init, push, pull, output, status}
# kaggle config {view, set, unset}

#res= bash('kaggle '+getKaggleEntityString(dataSetType,True)+' download -q -f '+fileName+' -p '+tmpPath+''+(' --unzip' if isZip else'')+' '+dataSetRef)
#res=bash('kaggle kernels pull '+kernelRef+' -p '+path4currentKernel)
#currentList = kaggleCommand2DF(getCommandStr(commandStr,page,paginatedType.getPageSize()))
#command ='kaggle '+getKaggleEntityString(dataSetType,True)+' files '+dataSetRef



class KaggleCommand():

    INITALPARAMETERS = {"sort-by":None,
                    "size":None,
                    "file-type":None,
                    "license-name":None,
                    "tag-ids":None,
                    "search":None,
                    "user":None,
                    "mine":False,
                    "page":1,
                    "max-size":None,
                    "min-size":None}

    def __init__(self, entity, operation, parameters={},entityRef=None):
        self._entity = entity
        self._operation = operation
        self._parameters = {**self.INITALPARAMETERS, **parameters}
        self._entityRef = entityRef
    
    @property
    def entity(self):
            return self._entity
    
    @property
    def operation(self):
            return self._operation
    
    @property
    def parameters(self):
            return self._parameters
    
    @parameters.setter
    def parameters(self, new_parameters):
        self._parameters = {**self._parameters, **new_parameters}
    
    @property
    def entityRef(self):
            return self._entityRef

    @staticmethod
    def buildCommand(entity, operation, parameters={},entityRef=None):
        return KaggleCommand(entity, operation, parameters,entityRef)
        
        
    def execute(self):    
        if self.entity==KaggleEntityType.DATASET:
            if(self.operation==KaggleCommandOperations.LIST):
                #https://github.com/Kaggle/kaggle-api/blob/15cb3f2490db9e0fad4b7662e3621ad949232510/kaggle/api/kaggle_api_extended.py#L828
                del self._parameters['page-size']
                del self._parameters['sort-by']
                del self._parameters['file-type']
                del self._parameters['license-name']
                del self._parameters['tag-ids']
                del self._parameters['max-size']
                del self._parameters['min-size']
                #return https://github.com/Kaggle/kaggle-api/blob/15cb3f2490db9e0fad4b7662e3621ad949232510/kaggle/models/kaggle_models_extended.py#L67
                return getApi().dataset_list(**self.parameters)
            else:
                raise CommandTypDoesNotExist()
        elif self.entity==KaggleEntityType.COMPETITION:
            raise CommandTypDoesNotExist(str(self.entity)+' '+str(self.operation))
        elif self.entity==KaggleEntityType.KERNEL:
            if(self.operation==KaggleCommandOperations.DOWNLOAD):
                #https://github.com/Kaggle/kaggle-api/blob/15cb3f2490db9e0fad4b7662e3621ad949232510/kaggle/api/kaggle_api_extended.py#L828
                del self._parameters['sort-by']
                del self._parameters['size']
                del self._parameters['file-type']
                del self._parameters['license-name']
                del self._parameters['tag-ids']
                del self._parameters['search']
                del self._parameters['user']
                del self._parameters['mine']
                del self._parameters['page']
                del self._parameters['max-size']
                del self._parameters['min-size']
                path=self._parameters['path']
                del self._parameters['path']
                res = getApi().kernel_pull(self.entityRef.split("/")[0],self.entityRef.split("/")[1],**self.parameters)
                f = open(path+res['metadata']['slug']+'.ipynb', "w",encoding="utf-8")
                f.write(res['blob']['source'])
                f.close()
            elif(self.operation==KaggleCommandOperations.LIST):
                #https://github.com/Kaggle/kaggle-api/blob/15cb3f2490db9e0fad4b7662e3621ad949232510/kaggle/api/kaggle_api_extended.py#L828
                del self._parameters['size']
                del self._parameters['file-type']
                del self._parameters['license-name']
                del self._parameters['tag-ids']
                del self._parameters['max-size']
                del self._parameters['min-size']
                del self._parameters['sort-by']
                del self._parameters['page-size']
                return getApi().kernels_list(**self.parameters)
            else:
                raise CommandTypDoesNotExist(str(self.entity)+' '+str(self.operation))
        else:
            raise CommandTypDoesNotExist(str(self.entity)+' '+str(self.operation))

class KaggleCommandOperations(Enum):
  LIST = 1
  files = 2
  DOWNLOAD = 3
  submit = 4
  submissions = 5
  leaderboard = 6
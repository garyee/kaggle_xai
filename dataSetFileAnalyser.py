from kaggleDownloader import downloadDataSetFilesByDataSetRef
from utils.DataSetTypes import DataSetTypes
import utils.database as database
from utils.kaggleEnums import KaggleEntityType

def analyseDataSets():
    database.initConnection()
    dataSetRefs=database.getAllEntityRefs()
    for entityRef,isCompetition in dataSetRefs:
        dataSetType=DataSetTypes
        analyzeDataSetFiles(entityRef,KaggleEntityType.DATASET if isCompetition==0 else KaggleEntityType.COMPETITION)
    database.closeConnection()

def analyzeDataSetFiles(entityRef,type =KaggleEntityType.DATASET):
    downloadDataSetFilesByDataSetRef(entityRef,type)

analyseDataSets()
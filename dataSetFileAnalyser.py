from kaggleDownloader import deleteTrainFileDir, downloadDataSetFilesByDataSetRef
from utils.DataSetTypes import DataSetTypes
import utils.database as database
from utils.kaggleEnums import KaggleEntityType, getEntityTypeFromCompetitionInt
from tqdm import tqdm

from utils.webStuff import setupDriver, shutDownDriver

def analyseDataSets():
    database.initConnection()
    setupDriver()
    dataSetRefs=database.getAllTabularEntityRefs()
    for entityRef,isCompetition in tqdm(dataSetRefs):
        dataSetType=DataSetTypes
        analyzeDataSetFiles(entityRef,getEntityTypeFromCompetitionInt(isCompetition))
    database.closeConnection()
    shutDownDriver()


def analyzeDataSetFiles(entityRef,type =KaggleEntityType.DATASET):
    trainingfilePath=downloadDataSetFilesByDataSetRef(entityRef,type)
    if(trainingfilePath is not None):
        analyseTrainFile(trainingfilePath)
        deleteTrainFileDir(trainingfilePath)

def analyseTrainFile(trainingfilePath):
    print(trainingfilePath)

analyseDataSets()
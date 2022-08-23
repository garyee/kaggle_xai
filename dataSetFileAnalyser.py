from Downloaders.kaggleCodeDownloader import deleteTrainFileDir
from Downloaders.kaggleDataSetDownloader import downloadDataSetFilesByDataSetRef, getFileListByDataSetRef, getTrainingFileAsDataframe, getTrainingFileName
from utils.DataSetTypes import DataSetTypes
import utils.database as database
from utils.kaggleEnums import KaggleEntityType, getEntityTypeFromCompetitionInt, getKaggleEntityString
from tqdm import tqdm

from utils.webStuff import setupDriver, shutDownDriver

def analyseDataSets():
    database.initConnection()
    setupDriver()
    dataSetRefs=database.getAllTabularDatabaseRefs()
    for entityRef,isCompetition in tqdm(dataSetRefs):
        analyzeDataSetFiles(entityRef,getEntityTypeFromCompetitionInt(isCompetition))
    database.closeConnection()
    shutDownDriver()


def analyzeDataSetFiles(entityRef,type = KaggleEntityType.DATASET):
    fileList=getFileListByDataSetRef(entityRef,type)
    trainingFileName=getTrainingFileName(fileList)
    if(trainingFileName is None):
        print('No file found for: '+getKaggleEntityString(type)+' '+entityRef)
    filePath=getTrainingFileAsDataframe(entityRef,type,trainingFileName)
    

    if(filePath is not None):
        deleteTrainFileDir(filePath)

def analyseTrainFile(trainingfilePath):
    print(trainingfilePath)

analyseDataSets()
from tqdm import tqdm
import database
from kaggleEnums import KaggleEntityType
from kaggleFileMetaDataAnalyser import analyseDataSetMetaData
from kaggleEntityFileListAnalyser import analyseEntityFileList

def analyseAllAndSetType(dataSetList):
    database.initConnection()
    for entityDict in tqdm(dataSetList):
        analyseOneEntity(entityDict[0],database.getEntityTypeFromDBentry(entityDict[1]))
    database.closeConnection()

def analyseOneEntity(entityRef,entityType):
    if(entityType!=KaggleEntityType.NONE):
        resultingRow={'dataSetRef':entityRef}
        #DownloadMetadata
        if entityType==KaggleEntityType.DATASET:
            analyseDataSetMetaData(entityRef,resultingRow)
        if 'type' not in resultingRow:
            analyseEntityFileList(entityRef,resultingRow,entityType)
        if 'type' in resultingRow:
            database.updateEntityTypeAndGoal(resultingRow)
        #DownloadFiles
        #AnalyseMetadata-keywords
        
        #AnalyseFiles(extensions, fileCount etc)
        #SetType to DataBase
        #DeleteFiles
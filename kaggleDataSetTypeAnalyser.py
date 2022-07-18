import database
from kaggleEnums import KaggleEntityType
from kaggleFileMetaDataAnalyser import analyseDataSetMetaData
from kaggleEntityFileListAnalyser import analyseEntityFileList

def analyseAllAndSetType(dataSetList):
    database.initConnection()
    for entityDict in dataSetList:
        analyseOneEntity(entityDict['dataBaseRef'],database.getEntityTypeFromDBentry(entityDict['is_competition']))
    database.closeConnection()

def analyseOneEntity(entityRef,entityType):
    if(entityType!=KaggleEntityType.NONE):
        resultingRow={'dataSetRef':entityRef}
        #DownloadMetadata
        if entityType==KaggleEntityType.DATASET:
            analyseDataSetMetaData(entityRef,resultingRow)
        if 'type' not in resultingRow:
            analyseEntityFileList(entityRef,resultingRow)
        database.updateEntityTypeAndGoal(resultingRow)
        #DownloadFiles
        #AnalyseMetadata-keywords
        
        #AnalyseFiles(extensions, fileCount etc)
        #SetType to DataBase
        #DeleteFiles
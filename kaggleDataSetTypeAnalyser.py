from database import getEntityTypeFromDBentry, updateEntityTypeAndGoal
from kaggleEnums import KaggleEntityType
from kaggleFileMetaDataAnalyser import analyseDataSetMetaData
from kaggleEntityFileListAnalyser import analyseEntityFileList

def analyseAllAndSetType(dataSetList):
    for entityDict in dataSetList:
        analyseOneEntity(entityDict['dataBaseRef'],getEntityTypeFromDBentry(entityDict['is_competition']))

def analyseOneEntity(entityRef,entityType):
    if(entityType!=KaggleEntityType.NONE):
        resultingRow={'dataSetRef':entityRef}
        #DownloadMetadata
        if entityType==KaggleEntityType.DATASET:
            analyseDataSetMetaData(entityRef,resultingRow)
        if 'type' not in resultingRow:
            analyseEntityFileList(entityRef,resultingRow)
        updateEntityTypeAndGoal(resultingRow)
        #DownloadFiles
        #AnalyseMetadata-keywords
        
        #AnalyseFiles(extensions, fileCount etc)
        #SetType to DataBase
        #DeleteFiles
from kaggleFileMetaDataAnalyser import analyseDataSetMetaData

def analyseAllAndSetType(dataSetList):
    for dataSetRef in dataSetList:
        analyseOneDataSet(dataSetRef)

def analyseOneDataSet(dataSetRef):
    resultingRow={'dataSetRef':dataSetRef}
    #DownloadMetadata
    analyseDataSetMetaData(dataSetRef,resultingRow)
    # if('type' not in resultingRow):
        
    #DownloadFiles
    #AnalyseMetadata-keywords
    
    #AnalyseFiles(extensions, fileCount etc)
    #SetType to DataBase
    #DeleteFiles
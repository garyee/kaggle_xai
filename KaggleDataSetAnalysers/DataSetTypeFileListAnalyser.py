import os
import re
from KaggleDataSetAnalysers.KaggleDataSetAnalyser import KaggleDataSetAnalyser
from utils.kaggleEnums import KaggleEntityType, getAllKnownExtensions
from utils.DataSetTypes import DataSetTypes
from utils.kaggleHelper import kaggleCommand2DF, setTypeAndCertainty
import utils.database as database

class DataSetTypeFileListAnalyser(KaggleDataSetAnalyser):
    
    def analyse(self,entityRef,entityType,resDict):
        command='kaggle datasets files '+entityRef
        if entityType==KaggleEntityType.COMPETITION:
            command='kaggle competitions files -q '+entityRef
        fileList = kaggleCommand2DF(command)
        countPerType={}
        overAllFileSize=0
        if fileList.empty:
            database.shiftDataSetToBlackList(entityRef,entityType,"Has no Files!")
        else:
            for index, row in fileList.iterrows():
                filename=row['name']
                fileSize=self.parseFileSize(row['size'])
                _, file_extension = os.path.splitext(filename)
                file_extension=file_extension.lstrip('.').lower().strip();
                if file_extension!='':
                    overAllFileSize+=fileSize
                    self.fillCountArr(file_extension,countPerType,fileSize,entityRef)
            self.getFileTypeFromCountArr(countPerType,overAllFileSize,resDict)

    def fillCountArr(self,file_extension,countPerType,fileSize,entityRef):
        fileType=DataSetTypes.MISC
        if file_extension in getAllKnownExtensions():
            for dataSetType in DataSetTypes:
                if file_extension in dataSetType.getExtensions():
                    fileType=dataSetType
                    break
        else:
            print("New Unknown File-Extention'"+file_extension+"' in "+entityRef)
        if fileType not in countPerType:
            countPerType[fileType]=fileSize
        else:
            countPerType[fileType]+=fileSize

    def getFileTypeFromCountArr(self,countPerType,overAllFileSize,resDict):
        maxType=DataSetTypes.MISC
        maxFileSizeRatio=0
        for fileTypeCounted, countedFileSizePerType in countPerType.items():
            fileRatio=countedFileSizePerType/overAllFileSize
            if(fileRatio>maxFileSizeRatio):
                maxType=fileTypeCounted
                maxFileSizeRatio=countedFileSizePerType/overAllFileSize
        typeCertainty=min(int(maxFileSizeRatio*100),maxType.getExtensionsCertanties())
        setTypeAndCertainty(maxType,typeCertainty,resDict)

    def parseFileSize(self,fileSizeStr):
        units = {"B": 1, "KB": 2**10, "MB": 2**20, "GB": 2**30, "TB": 2**40 ,
                "":  1, "KIB": 10**3, "MIB": 10**6, "GIB": 10**9, "TIB": 10**12}
        m = re.match(r'^([\d\.]+)\s*([a-zA-Z]{0,3})$', str(fileSizeStr).strip())
        number, unit = float(m.group(1)), m.group(2).upper()
        return int(number*units[unit])
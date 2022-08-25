import os
#from tqdm.notebook import trange, tqdm
from tqdm import tqdm
import json
from KaggleDataSetAnalysers.DataSetTypeFileListAnalyser import DataSetTypeFileListAnalyser
from KaggleDataSetAnalysers.KaggleDataSetAnalyser import KaggleDataSetAnalyser
from utils.kaggleEnums import basePath,KaggleEntityType, KernelLanguage, getAllInfoFromKernelPath, getEntityTypeFromCompetitionInt, getIsCompetitionfromEntityType, getKernelPathfromRef, testKernelsRefs
from Downloaders.kaggleCodeDownloader import downloadKernelByRef,getKernelPath
from KaggleKernelCodeAnalysers.KaggleKernelCodeAnalyzer import KaggleKernelCodeAnalyzer
import utils.database as database

def getTestKernelFiles():
    matches=[]
    for entityType,kernelInfoDict in testKernelsRefs.items():
        if(len(kernelInfoDict)>0):
            for middleEntityRef, kernelRef in kernelInfoDict.items():
                downloadKernelByRef(kernelRef,middleEntityRef,entityType)
                matches += getAllNoteBooksInPath(getKernelPath(kernelRef,middleEntityRef,entityType))
    return matches

def getAllNoteBooksInPath(directory=basePath):
    matches = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
          if(file.endswith('ipynb')):
            matches.append(os.path.join(subdir, file).replace("\\\\","/").replace("\\","/"))
    return matches

def getAllTabularKernels():
    database.initConnection()
    kernelRefs=database.getAllTabularKernelsRefs()
    res=[]
    for kernelRef,dataSetRef,is_competition in tqdm(kernelRefs):
        kernelPath=getKernelPathfromRef(kernelRef,dataSetRef,getEntityTypeFromCompetitionInt(is_competition))
        noteBookPaths=getAllNoteBooksInPath(kernelPath)
        if(len(noteBookPaths)>0):
            res.append(noteBookPaths[0])
    database.closeConnection()
    return res

def merge_two_dicts(x, y):
    if(len(x)==0):
        return y
    if(len(y)==0):
        return x
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

def analyseTestKernels():
    return anaylseKernels(getTestKernelFiles())

def analyseAllKernels(dataSetAnalysers=[],kernelAnalysers = []):
    return anaylseKernels(getAllNoteBooksInPath(),intanciacteAnalysers(dataSetAnalysers,KaggleDataSetAnalyser),intanciacteAnalysers(kernelAnalysers,KaggleKernelCodeAnalyzer))

def analyseAllTabularKernels(dataSetAnalysers=[],kernelAnalysers = []):
    return anaylseKernels(getAllTabularKernels(),intanciacteAnalysers(dataSetAnalysers,KaggleDataSetAnalyser),intanciacteAnalysers(kernelAnalysers,KaggleKernelCodeAnalyzer))

def intanciacteAnalysers(analysers,baseClass):
    returnArr=[]
    if(analysers):
        for analyser in analysers:
            if issubclass(analyser, baseClass ):
                returnArr.append(analyser())
    return returnArr

def anaylseKernels(filePaths,dataSetAnalysersInstances=[],kernelAnalysersInstances = []):
    database.initConnection()
    lastDataSetRef=None
    resultDataSetDict={}
    kernelCountPerDataSet=0
    for filePath in tqdm(filePaths):
        if os.path.exists(filePath):
            kernelCountPerDataSet+=1
            parentEntityType,parentEntityRef,entityRef,kernelFileName = getAllInfoFromKernelPath(filePath)
            if(parentEntityRef is not None and parentEntityType is not None):
                #Insert DB into dataset_info
                currentDataSetChanged=parentEntityRef!=lastDataSetRef
                if(currentDataSetChanged):
                    # print('INIT new DS: '+parentEntityRef)
                    # update DS db with dict
                    kernelAnalysersCloseDataSet(parentEntityType,resultDataSetDict,kernelCountPerDataSet,kernelAnalysersInstances)
                    kernelCountPerDataSet=0
                    if(lastDataSetRef is not None and 'dataSetRef' in resultDataSetDict and len(resultDataSetDict.keys())>2):
                        database.updateDataSetToDB(resultDataSetDict)
                    resultDataSetDict={
                            'dataSetRef':parentEntityRef,'is_competition':getIsCompetitionfromEntityType(parentEntityType)
                    }
                    # one time per DS analyse and update Dict
                    database.insertDataBase(parentEntityRef,getIsCompetitionfromEntityType(parentEntityType))
                    analyseDataSet(parentEntityRef,parentEntityType,resultDataSetDict,kernelCountPerDataSet,dataSetAnalysersInstances)
                    lastDataSetRef=parentEntityRef
                # insert KernelDB row directly and update DS dict if needed
                resultKernelDict={
                    'dataSetRef':parentEntityRef,'kernelRef':entityRef
                }
                analyseKernelFile(filePath,resultKernelDict,kernelCountPerDataSet,kernelAnalysersInstances)
                database.insertKernel(resultKernelDict)
            else:
                print('DataSet got deleted for kernel: '+kernelFileName)
    database.closeConnection()

def analyseDataSet(dataSetRef,dataSetType,resultDataSetDict,kernelCountPerDataSet,dataSetAnalysersInstances=[]):
    if(dataSetType!=KaggleEntityType.NONE and dataSetAnalysersInstances):
        for dataSetAnalyser in dataSetAnalysersInstances:
            dataSetAnalyser.analyse(dataSetRef,dataSetType,resultDataSetDict,kernelCountPerDataSet)

def kernelAnalysersCloseDataSet(dataSetType,resultDataSetDict,kernelCountPerDataSet,kernelAnalysersInstances = []):
    if(dataSetType!=KaggleEntityType.NONE and kernelAnalysersInstances):
        for kernelAnalyser in kernelAnalysersInstances:
            kernelAnalyser.onDataSetChanged(resultDataSetDict,kernelCountPerDataSet)
    
def analyseKernelFile(filePath,resultKernelDict,kernelIndex,kernelAnalysersInstances = []):
    if os.path.exists(filePath):
        if os.stat(filePath).st_size == 0:
            os.remove(filePath)
            print(filePath+' was empty and thus removed!')
            return
        with open(filePath, encoding='utf-8') as f:
            kernelCode={}
            try:
                kernelCode = json.load(f)
            except ValueError as e:
                print('Decoding JSON has failed for: '+filePath)
            language=KernelLanguage.NONE

            # if hasattr(kernelCode['metadata'],'kernelspec'):
            #   if hasattr(kernelCode['metadata']['kernelspec'], 'language'):
            #     if kernelCode['metadata']['kernelspec']['language']=='python':
            #       language=KernelLanguage.PYTHON
            #   elif hasattr(kernelCode['metadata']['kernelspec'], 'name') and 'python' in kernelCode['metadata']['kernelspec']['name']:
            #     language=KernelLanguage.PYTHON
            if 'cells' in kernelCode:
                for kernelAnalyser in kernelAnalysersInstances:
                        kernelAnalyser.analyse(kernelCode['cells'],resultKernelDict,kernelIndex)


# analyseOneKernelFile('C:/Users/garyee/gDrive/Colab/Kaggle/kernels/datasets/kaggle_____meta-kaggle/benhamner_____predicting-which-scripts-get-votes/predicting-which-scripts-get-votes.ipynb')
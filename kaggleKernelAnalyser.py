import os
#from tqdm.notebook import trange, tqdm
from tqdm import tqdm
import json
from KaggleDataSetAnalysers.DataSetTypeFileListAnalyser import DataSetTypeFileListAnalyser
from KaggleDataSetAnalysers.KaggleDataSetAnalyser import KaggleDataSetAnalyser
from kaggleEnums import basePath,KaggleEntityType, KernelLanguage, getAllInfoFromKernelPath, getIsCompetitionfromEntityType, testKernelsRefs
from kaggleDownloader import downloadKernelByRef,getKernelPath
from KaggleKernelCodeAnalysers.KaggleKernelCodeAnalyzer import KaggleKernelCodeAnalyzer
import database

def getTestKernelFiles():
    matches=[]
    for entityType,kernelInfoDict in testKernelsRefs.items():
        if(len(kernelInfoDict)>0):
            for middleEntityRef, kernelRef in kernelInfoDict.items():
                downloadKernelByRef(kernelRef,middleEntityRef,entityType)
                matches += getAllFilePaths(getKernelPath(kernelRef,middleEntityRef,entityType))
    return matches

def getAllFilePaths(directory=basePath):
    matches = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
          if(file.endswith('ipynb')):
            matches.append(os.path.join(subdir, file).replace("\\\\","/").replace("\\","/"))
    return matches

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
    return anaylseKernels(getAllFilePaths(),dataSetAnalysers,kernelAnalysers)

def anaylseKernels(filePaths,dataSetAnalysers=[],kernelAnalysers = []):
    database.initConnection()
    lastDataSetRef=None
    resultDataSetDict={}
    for filePath in tqdm(filePaths):
        parentEntityType,parentEntityRef,entityRef,kernelFileName = getAllInfoFromKernelPath(filePath)
        #Insert DB into dataset_info
        if(parentEntityRef!=lastDataSetRef):
            # print('INIT new DS: '+parentEntityRef)
            # update DS db with dict
            if(lastDataSetRef is not None and 'dataSetRef' in resultDataSetDict and len(resultDataSetDict.keys())>2):
                database.updateDataSetToDB(resultDataSetDict)
            resultDataSetDict={
                    'dataSetRef':parentEntityRef,'is_competition':getIsCompetitionfromEntityType(parentEntityType)
            }
            # one time per DS analyse and update Dict
            database.insertDataBase(parentEntityRef,getIsCompetitionfromEntityType(parentEntityType))
            analyseDataSet(parentEntityRef,parentEntityType,resultDataSetDict,dataSetAnalysers)
            lastDataSetRef=parentEntityRef
        # insert KernelDB row directly and update DS dict if needed
        # analyseKernelFile(filePath,entityRef,kernelAnalysers)
    database.closeConnection()

def analyseDataSet(dataSetRef,dataSetType,resultDataSetDict,dataSetAnalysers=[]):
    if(dataSetType!=KaggleEntityType.NONE):
        for dataSetAnalyser in dataSetAnalysers:
            if issubclass(dataSetAnalyser, KaggleDataSetAnalyser ):
                analyser=dataSetAnalyser()
                analyser.analyse(dataSetRef,dataSetType,resultDataSetDict)
    
def analyseKernelFile(filePath,entityRef,analysers = []):
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
        if hasattr(kernelCode,'cells'):
            for analyser in analysers:
                if issubclass(analyser, KaggleKernelCodeAnalyzer ):
                    analyser=dataSetAnalyser()
                    analyser.analyse(dataSetRef,dataSetType,resultDataSetDict)
                    # analyser.analyse(kernelCode['cells'],resultDict)


# analyseOneKernelFile('C:/Users/garyee/gDrive/Colab/Kaggle/kernels/datasets/kaggle_____meta-kaggle/benhamner_____predicting-which-scripts-get-votes/predicting-which-scripts-get-votes.ipynb')
import os
from tqdm.notebook import trange, tqdm
import json
from kaggleEnums import basePath,KaggleEntityType, KernelLanguage, getAllInfoFromKernelPath
from main import testKernelsRefs
from kaggleDownloader import downloadKernelByRef,getKernelPath
from KaggleKernelCodeAnalyzer import XaiAnalyser
import database

def analyseTestKernels():
    return anaylseKernels(getTestKernelFiles())

def analyseAllKernels():
    return anaylseKernels(getAllFilePaths)

def anaylseKernels(filePaths):
    database.initConnection()
    matches={}
    for filePath in tqdm(filePaths):
        parentEntityType,parentEntityRef,entityRef,kernelFileName = getAllInfoFromKernelPath(filePath)
        if parentEntityRef is not None:
            database.insertRowOrIncrementKernelCount(parentEntityRef,1 if parentEntityType==KaggleEntityType.COMPETITION else 0)
        new_matches=analyseOneKernelFile(filePath)
        matches = merge_two_dicts(matches,new_matches)
    database.closeConnection()
    return matches

def analyseOneKernelFile(filePath,write2File=True):
    matches={}
    with open(filePath) as f:
        kernelCode={}
        try:
            kernelCode = json.load(f)
        except ValueError:
            print('Decoding JSON has failed for: '+filePath)
        language=KernelLanguage.NONE

        # if hasattr(kernelCode['metadata'],'kernelspec'):
        #   if hasattr(kernelCode['metadata']['kernelspec'], 'language'):
        #     if kernelCode['metadata']['kernelspec']['language']=='python':
        #       language=KernelLanguage.PYTHON
        #   elif hasattr(kernelCode['metadata']['kernelspec'], 'name') and 'python' in kernelCode['metadata']['kernelspec']['name']:
        #     language=KernelLanguage.PYTHON
        if hasattr(kernelCode,'cells'):
            for cell in kernelCode['cells']:
                matches=merge_two_dicts(matches, XaiAnalyser.analyse(cell,getAllInfoFromKernelPath(filePath)))
        return matches

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
            matches.append(os.path.join(subdir, file))
    return matches

def merge_two_dicts(x, y):
    if(len(x)==0):
        return y
    if(len(y)==0):
        return x
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z
from abc import abstractmethod
import re

class KaggleKernelCodeAnalyzer:
  
  @classmethod
  @abstractmethod
  def getHeader(self):
        pass

  @classmethod
  @abstractmethod
  def analyse(self,cell,cellType):
        pass

class XaiAnalyser(KaggleKernelCodeAnalyzer):

  explainableAITermesDict = {
    "PH_ALE": ["import.*ALE","import.*plot_ale"],
    "PH_PFI": ["eli5\.show_weights.*","xai.feature_importance"],
#    "IM": ["sklearn.ensemble"],
    "PH_LIME": ["import.*lime","from\slime\simport","skater.core.local_interpretation.lime."],
    "PH_PDP": ["from pdpbox"], 
    "IM_FI": ["lgbm.plot_importance","xgb.plot_importance"],
    "PH_SHAP": ["shap.","from alibi.explainers import KernelShap"],
    "DABL": ["dabl."],
    "PH_GLOBAL_SURR": ['skater.model'],
    "IM_RULELIST" : ["skater.core.global_interpretation.interpretable_models.brlc"],
    "DASHBOARD" : ["from explainerdashboard"],
    "IM_GAM" :["from pygam import"]
  }

  def getHeader():
    xaiMethodKeys=list(XaiAnalyser.explainableAITermesDict.keys())
    #xaiMethodKeys.append('filepath')
    return xaiMethodKeys

  def analyse(self,cell,filePath):
    matches={}
    if cell['cell_type'] == 'code' and 'source' in cell and cell['source'] is not None:
          for key,regularExpressions in XaiAnalyser.explainableAITermesDict.items():
            if (filePath not in matches) or (type(matches[filePath]) is list and key not in matches[filePath]):
              for regex in regularExpressions:
                if type(cell['source']) == str:
                  if re.search(re.compile(regex, re.S), cell['source']):
                    if(filePath in matches and type(matches[filePath]) == list and key not in matches[filePath]):
                      matches[filePath].append(key)
                    else:
                      matches[filePath]=[key]
                else:
                  print('cell[source] of unknown type was found: '+str(type(cell['source'])))
                  print('-----------')
                  print(cell['source'])
                  print('-----------')
    return matches

class KernelMetaDataAnalyser(KaggleKernelCodeAnalyzer):

  def getHeader():
    return []

  def analyse(self,cell,filepath):
    matches={}

    return matches


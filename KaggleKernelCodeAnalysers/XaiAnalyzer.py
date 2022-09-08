import re
import utils.database as database
from KaggleKernelCodeAnalysers.KaggleKernelCodeAnalyzer import KaggleKernelCodeAnalyzer

class XaiAnalyser(KaggleKernelCodeAnalyzer):

  CELLTYPEFILTERARR=['code']

  xaiMethodsResSet={}

  termsDict= {
  "PH_ALE": ["import.*ALE","import.*plot_ale"],
  "PH_PFI": ["eli5\.show_weights.*","xai\.feature_importance"],
#    "IM": ["sklearn.ensemble"],
  "PH_LIME": ["import.*lime","from\slime\simport","skater\.core\.local_interpretation\.lime\."],
  "PH_PDP": ["from pdpbox"], 
  "IM_FI": ["lgbm\.plot_importance","xgb\.plot_importance"],
  "PH_SHAP": ["shap\.","from alibi\.explainers import KernelShap"],
  "DABL": ["dabl\."],
  "PH_GLOBAL_SURR": ['skater\.model'],
  "IM_RULELIST" : ["skater\.core\.global_interpretation\.interpretable_models\.brlc"],
  "DASHBOARD" : ["from explainerdashboard"],
  "IM_GAM" :["from pygam import"],
  #functional Data analysis - e.g. anova
  "FDA" :["import skfda"],
  "Anova": ["from skfda\.inference\.anova","from pyfanova\.fanova", "from fanova"]
}

  def __init__(self):
    self._xaiMethodsResSet = {}

  def analyseCell(self,sourceCell):
    for key,regularExpressions in XaiAnalyser.termsDict.items():
      for regex in regularExpressions:
          if re.search(re.compile(regex, re.S), sourceCell):
              if(key not in self.xaiMethodsResSet):
                  self.xaiMethodsResSet[key]=1
    # if(isLastCell):
      # typeVotePerDataSet['kernelRef']=KernelRef
      # database.insertOrUpdateKernelXAI
      # typeVotePerDataSet={}

  def onLastCell(self,resultKernelDict,kernelIndex):
    database.addXAIMethodToKernelCreateColumnIfNeeded(self.xaiMethodsResSet,resultKernelDict['kernelRef'])
    self.xaiMethodsResSet={}

  def onDataSetChanged(self,resultDataSetDict,kernelCountPerDataSet):
        pass
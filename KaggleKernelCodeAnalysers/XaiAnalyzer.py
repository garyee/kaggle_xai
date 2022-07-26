from KaggleKernelCodeAnalysers.KaggleKernelCodeAnalyzer import KaggleKernelCodeAnalyzer

class XaiAnalyser(KaggleKernelCodeAnalyzer):

  termsDict= {
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
  "IM_GAM" :["from pygam import"],
  #functional Data analysis - e.g. anova
  "FDA" :["import skfda"],
  "Anova": ["from skfda.inference.anova","from pyfanova.fanova", "from fanova"]
}

#   def getHeader():
#     xaiMethodKeys=list(XaiAnalyser.explainableAITermesDict.keys())
#     #xaiMethodKeys.append('filepath')
#     return xaiMethodKeys

  def analyse(self,cell,resultDict):
    matches={}
    for key,regularExpressions in XaiAnalyser.termsDict.items():
        if (filePath not in matches) or (type(matches[filePath]) is list and key not in matches[filePath]):
            for regex in regularExpressions:
                if re.search(re.compile(regex, re.S), cell['source']):
                    if(filePath in matches and type(matches[filePath]) == list and key not in matches[filePath]):
                        matches[filePath].append(key)
                    else:
                        matches[filePath]=[key]
    return matches
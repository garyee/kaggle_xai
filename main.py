from kaggleEnums import KaggleEntityType

filePath= '/content/drive/MyDrive/Colab'

kernelListPageSize=100

testKernelsRefs={KaggleEntityType.DATASET: {},
                 KaggleEntityType.COMPETITION:{
                  'titanic':'vbmokin/merging-fe-prediction-xgb-lgb-logr-linr',
                  'widsdatathon2022':'shreyasajal/wids-datathon-2022-explainable-ai-walkthrough'
                 },
                 KaggleEntityType.NONE: {'none1':'datacog314/tutorial-machine-learning-interpretability',
                                         'none2':'devsubhash/explainable-ai-using-explainerdashboard'}
                }
#vbmokin/merging-fe-prediction-xgb-lgb-logr-linr - ['PH_PFI', 'PH_SHAP']
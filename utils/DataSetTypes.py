from enum import Enum

class DataSetTypes(Enum):
  TABULAR = 'Tabular'
  IMAGE = 'Image'
  VIDEO = 'Video'
  TEXT = 'Text'
  TIME_SERIES = 'Time Series'
  BIOCHEM = 'Bio_Chem'
  MISC = 'Misc'

  def getExtensions(self=None):
    extensionArray= {
      DataSetTypes.TABULAR: ['csv','xls','xlsx','npy','parquet','paruqet','npz','tsv','json','db','sqlite'],
      DataSetTypes.IMAGE:['jpg','gif','png','dcm'],
      DataSetTypes.VIDEO:['mpg','mp4','mpeg'],
      DataSetTypes.TEXT:[],
      DataSetTypes.TIME_SERIES:[],
      DataSetTypes.BIOCHEM:['xyz'],
      DataSetTypes.MISC:[],
    }
    if(self is None):
      return extensionArray
    return extensionArray[self]

  def getExtensionsCertanties(self=None):
    certainties= {
      DataSetTypes.TABULAR:60,
      DataSetTypes.IMAGE:90,
      DataSetTypes.VIDEO:90,
      DataSetTypes.TEXT:0,
      DataSetTypes.TIME_SERIES:0,
      DataSetTypes.BIOCHEM:100,
      DataSetTypes.MISC:20,
    }
    if(self is None):
      return certainties
    return certainties[self]

  def getSourceCodeRegExes(self=None):
    regExArray= {
      DataSetTypes.TABULAR: 
        [],
      DataSetTypes.IMAGE:
        [],
      DataSetTypes.VIDEO:
        [],
      DataSetTypes.TEXT:[
        'from nltk',
        'import nltk',
        'import spacy',
        'from spacy',
        'feature_extraction\.text',
        'sklearn.feature_extraction\.text',
        'Tokenizer',
        'Vectorizer',
      ],
      DataSetTypes.TIME_SERIES:[
        # '\.to_datetime\(',
        # 'date',
        # 'time',
        'time[^a-zA-Z0-9]{1}serie[s]*',
        # 'to_period',
        'statsmodels\.tsa',
        'from tsfresh',
        'import tsfresh',
        'from darts',
        'import darts',
        'from kats',
        'import kats',
        'from greykite',
        'import greykite',
        'from autots',
        'import autots',
      ],
      DataSetTypes.BIOCHEM:
        ['from ase'],
      DataSetTypes.MISC:
        [],
    }
    if(self is None):
      return regExArray
    return regExArray[self]

  def getCodeTypeCertanties(self=None):
    certainties= {
      DataSetTypes.TABULAR:0,
      DataSetTypes.IMAGE:0,
      DataSetTypes.VIDEO:0,
      DataSetTypes.TEXT:100,
      DataSetTypes.TIME_SERIES:100,
      DataSetTypes.BIOCHEM:70,
      DataSetTypes.MISC:0,
    }
    if(self is None):
      return certainties
    return certainties[self]

  def getMetaDataKeywordRegexes(self=None):
    #See DB Fields & order matters:
    regExArray= {
      DataSetTypes.TABULAR:[r'tabular'],
      DataSetTypes.IMAGE:[r'computer vision',r'image'],
      DataSetTypes.VIDEO:[r'^video$'],
      DataSetTypes.TEXT:[r'nlp',r'linguistics'],
      DataSetTypes.TIME_SERIES:[r'time series'],
      DataSetTypes.BIOCHEM:[],
      DataSetTypes.MISC:[],
    }
    if(self is None):
      return regExArray
    return regExArray[self]

  def getMetaDataTypeCertanties(self=None):
    certainties= {
      DataSetTypes.TABULAR:60,
      DataSetTypes.IMAGE:100,
      DataSetTypes.VIDEO:100,
      DataSetTypes.TEXT:90,
      DataSetTypes.TIME_SERIES:100,
      DataSetTypes.BIOCHEM:0,
      DataSetTypes.MISC:20,
    }
    if(self is None):
      return certainties
    return certainties[self]

    def __str__(self):
      return str(self.value)

# from KaggleDataSetAnalysers.DataSetTypeFileListAnalyser import DataSetTypeFileListAnalyser
# from KaggleDataSetAnalysers.DataSetTypeMetaDataAnalyser import DataSetTypeMetaDataAnalyser
# from KaggleKernelCodeAnalysers.DataSetTypeAnalyzer import DataSetTypeAnalyzer
# from KaggleKernelCodeAnalysers.DataSetTypeWordCounterAnalyzer import DataSetTypeWordCounterAnalyzer
from KaggleKernelCodeAnalysers.XaiAnalyzer import XaiAnalyser
from kaggleKernelAnalyser import analyseAllKernels
from utils.DataSetTypes import DataSetTypes

def fillDatabase():
    analyseAllKernels(kernelAnalysers=[XaiAnalyser])

fillDatabase()

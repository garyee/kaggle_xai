from KaggleDataSetAnalysers.DataSetTypeFileListAnalyser import DataSetTypeFileListAnalyser
from KaggleDataSetAnalysers.DataSetTypeMetaDataAnalyser import DataSetTypeMetaDataAnalyser
from KaggleKernelCodeAnalysers.DataSetTypeAnalyzer import DataSetTypeAnalyzer
from KaggleKernelCodeAnalysers.DataSetTypeWordCounterAnalyzer import DataSetTypeWordCounterAnalyzer
from kaggleKernelAnalyser import analyseAllKernels

def fillDatabase():
    analyseAllKernels(dataSetAnalysers=[DataSetTypeFileListAnalyser,DataSetTypeMetaDataAnalyser],kernelAnalysers=[DataSetTypeAnalyzer,DataSetTypeWordCounterAnalyzer])

fillDatabase()
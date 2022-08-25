from KaggleDataSetAnalysers.DataSetTypeFileListAnalyser import DataSetTypeFileListAnalyser
from KaggleDataSetAnalysers.DataSetTypeMetaDataAnalyser import DataSetTypeMetaDataAnalyser
from KaggleKernelCodeAnalysers.DataSetTypeAnalyzer import DataSetTypeAnalyzer
from KaggleKernelCodeAnalysers.DataSetTypeWordCounterAnalyzer import DataSetTypeWordCounterAnalyzer
from KaggleKernelCodeAnalysers.DataSetTargetColumnNameFinder import DataSetTargetColumnNameFinder
from KaggleKernelCodeAnalysers.XaiAnalyzer import XaiAnalyser
from kaggleKernelAnalyser import analyseAllKernels, analyseAllTabularKernels
from utils.DataSetTypes import DataSetTypes

def fillDatabase():
    # analyseAllKernels(
    #     dataSetAnalysers=[DataSetTypeFileListAnalyser,DataSetTypeMetaDataAnalyser],
    #     kernelAnalysers=[DataSetTypeAnalyzer,DataSetTypeWordCounterAnalyzer,XaiAnalyser])
    analyseAllTabularKernels(kernelAnalysers=[DataSetTargetColumnNameFinder])
fillDatabase()

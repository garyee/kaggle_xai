from kaggleDataSetTypeAnalyser import analyseAllAndSetType
from kaggleKernelAnalyser import analyseTestKernels,analyseAllKernels
import database

# analyseAllKernels()
# analyseTestKernels()

database.initConnection()
dataRefList=database.getAllEntityRefs()
database.closeConnection()
analyseAllAndSetType(dataRefList)
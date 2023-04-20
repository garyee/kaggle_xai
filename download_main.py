from Downloaders.kaggleCodeDownloader import getAllKernelsForKaggleMostVotedEntity
from utils.KaggleCommands.KaggleCommand import KaggleCommand, KaggleCommandOperations
from utils.kaggleEnums import KaggleEntityType

# ret=KaggleCommand.buildCommand(KaggleEntityType.DATASET, KaggleCommandOperations.LIST)
# print(ret.execute())
 
getAllKernelsForKaggleMostVotedEntity()
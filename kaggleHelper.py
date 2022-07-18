import os
import pandas as pd
from io import StringIO

def bash(command):
    output = os.popen(command).read()
    return output

def kaggleCommand2DF(command):
  result=bash(command+" --csv")
  return pd.read_csv(StringIO(result))
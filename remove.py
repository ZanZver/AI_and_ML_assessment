import csv
from os import remove
import pandas as pd
dataPath = "Data/Crime_Data_from_2010_to_2019.csv"
dataPathLite = "Data/Crime_Data_from_2010_to_2019-lite.csv"

def removeRows():
    dfLite = pd.read_csv(dataPath, index_col=False)
    dfLite2 = (dfLite.head(5000))
    dfLite2.to_csv(dataPathLite,index=False)

removeRows()
import csv
import pandas as pd
dataPath = "Data/Crime_Data_from_2010_to_2019.csv"
dataPathLite = "Data/Crime_Data_from_2010_to_2019-lite.csv"

def test4():
    dfLite = pd.read_csv(dataPath, index_col=False)
    dfLite2 = (dfLite.head(5000))
    dfLite2.to_csv(dataPathLite,index=False)

test4()
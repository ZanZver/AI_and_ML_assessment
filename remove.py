import csv
import pandas as pd
dataPath = "/Crime_Data_from_2010_to_2019.csv"
dataPathLite = "/Crime_Data_from_2010_to_2019-lite.csv"

def test4():
    dfLite = pd.read_csv(dataPath, index_col=0)
    dfLite2 = (dfLite.head(100))
    dfLite2.to_csv(dataPathLite,index=False)

test4()
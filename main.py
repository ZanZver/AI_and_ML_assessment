import pip

#=============================================================================================================================
#install modules on the PC if they are not installed
def import_or_install(package):
    #test if modules are installed on PC
    try: 
        __import__(package)
    #install module with pip if they are not installed
    except ImportError:
        pip.main(['install', package])   

#check if modules are installed on the PC
def modules_used():
    list_of_modules = ["loguru",
                       "sys",
                       "pandas",
                       "folium",
                       "webbrowser",
                       "numpy"]  
    #go across the list of modules used and pass it to import_or_install function for check
    for module in list_of_modules:
        import_or_install(module)

#check if modules are installed on the PC 
modules_used()
import sys
import pandas as pd
import folium
import numpy as np
#=============================================================================================================================
#check if depended .py modules are installed, if not stop the code 
try:
    import data_visualization as DV
except Exception as e:
    print("data_visualization.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

try:
    import data_processing as DP
except:
    print("data_processing.py not found. Stopping the code, please add it to the directory")
    sys.exit(1)

try:
    import machine_learning as ML
except:
    print("machine_learning.py not found. Stopping the code, please add it to the directory")
    sys.exit(1)
#=============================================================================================================================

p1 = DV.Person("John", 36)
p1.myfunc()

#dataPath = "/Users/zanzver/Documents/BCU/Year_3/CMP6202-A-S1-2021:22_Artificial_Intelligence_and_MachineLearning/Assessment_Information/Assessment1/AI_and_ML_assessment/data/Crime_Data_from_2010_to_2019.csv"
dataPathLite = "/Users/zanzver/Documents/BCU/Year_3/CMP6202-A-S1-2021:22_Artificial_Intelligence_and_MachineLearning/Assessment_Information/Assessment1/AI_and_ML_assessment/data/Crime_Data_from_2010_to_2019-lite.csv"

#df = pd.read_csv(dataPath, index_col=0)
dfLite = pd.read_csv(dataPathLite, index_col=False)

#print(df.head())

listOfColumnNames = pd.Index.tolist(dfLite.columns)
print(listOfColumnNames)
#print(dfLite.head(1))
#print(dfLite.iloc[:, 0])

#print(dfLite["LAT"].astype(float))
 
d1 = DV.DataVisualization(dfLite["LAT"].values, dfLite["LON"].values, dfLite["Crm Cd Desc"].values)
d1.createMap()
d1.openMap()
import pip

def import_or_install(package):
        #test if modules are installed on PC
        try: 
            __import__(package)
        #install module with pip if they are not installed
        except ImportError:
            pip.main(['install', package])   

def modulesUsed():
    try:
        list_of_modules = ["loguru",
                        "sys",
                        "pandas",
                        "folium",
                        "webbrowser",
                        "numpy",
                        "pygeocodio",
                        "geopy",
                        "geocodio",
                        "os",
                        "openrouteservice",
                        "json",
                        "PyQt5",
                        "math",
                        "graphviz"]  
        #go across the list of modules used and pass it to import_or_install function for check
        for module in list_of_modules:
            import_or_install(module)
        
        return(int(0))
    except Exception as e:
        print(e)
        return(int(1))

def loadFiles():
        returnDV = returnDP = returnML = returnWB = returnCR = int(1)

        try:
            import data_visualization as DV
            returnDV = int(returnDV) - int(1)
        except Exception as e:
            print("data_visualization.py not found. Stopping the code, please add it to the directory")
            print(e)
            sys.exit(1)

        try:
            import data_processing as DP
            returnDP = int(returnDP) - int(1)
        except Exception as e:
            print("data_processing.py not found. Stopping the code, please add it to the directory")
            print(e)
            sys.exit(1)

        try:
            import machine_learning as ML
            returnML = int(returnML) - int(1)
        except Exception as e:
            print("machine_learning.py not found. Stopping the code, please add it to the directory")
            print(e)
            sys.exit(1)

        try:
            import web_app as WB
            returnWB = int(returnWB) - int(1)
        except Exception as e:
            print("web_app.py not found. Stopping the code, please add it to the directory")
            print(e)
            sys.exit(1)

        try:
            import creds as CR
            returnCR = int(returnCR) - int(1)
        except Exception as e:
            print("creds.py not found. Stopping the code, please add it to the directory")
            print(e)
            sys.exit(1) 
        
        returnNum = int(returnDV) - int(returnDP) - int(returnML) - int(returnWB) - int(returnCR)
        if(int(returnNum) == int(0)):
            return (int(0))
        else:
            return (int(1))

def loadMainData():
    try:
        import pandas as pd
        mainData = pd.read_csv("Data/Crime_Data_from_2010_to_2019-lite.csv", index_col=False)
        return [int(0), mainData]
    except FileNotFoundError:
        return(2)
    except pd.errors.EmptyDataError:
        return(3)
    except pd.errors.ParserError:
        return(4)
    except Exception as e:
        return [1, e]

def loadDistrictData():
    try:
        import pandas as pd 
        districtData = pd.read_csv("Data/Reporting_Districts_data.csv", index_col=False)
        return [int(0), districtData]
    except FileNotFoundError:
        return(2)
    except pd.errors.EmptyDataError:
        return(3)
    except pd.errors.ParserError:
        return(4)
    except Exception as e:
        return [1, e]

def loadMocodesData():
    try:
        import pandas as pd
        mocodesData = pd.read_json("Data/MO_CODES_Numerical_20191119.json", orient ='index')
        return [int(0), mocodesData]
    except FileNotFoundError:
        return(2)
    except pd.errors.EmptyDataError:
        return(3)
    except pd.errors.ParserError:
        return(4)
    except Exception as e:
        return [1, e]
 
   
def loadUCRData():
    try:
        import json
        data = 0
        with open('Data/UCR-COMPSTAT062618.json', 'r') as myfile:
            data=myfile.read()
            
        obj = json.loads(data)
        return (int(0), obj)
    except FileNotFoundError:
        return(2)
    except Exception as e:
        return (1, e)

    
modulesUsedErrorCode = int(modulesUsed())
if(int(modulesUsedErrorCode) == int(0)):
    print("Modules have been successfully loaded")
elif(int(modulesUsedErrorCode) == int(1)):
    print("Error loading the modules")


loadFilesErrorCode = int(loadFiles())
if(int(loadFilesErrorCode) == int(0)):
    print("Files have been successfully loaded")
elif(int(loadFilesErrorCode) == int(1)):
    print("Error loading the files")

mainDataErrorCode, mainData = loadMainData()
if(int(loadFilesErrorCode) == int(0)):
    print("Data have been successfully loaded")
elif(int(loadFilesErrorCode) == int(1)):
    print("Error loading the data")
    print("Full error message: " + mainData)
elif(int(loadFilesErrorCode) == int(2)):
    print("Data not found.")
elif(int(loadFilesErrorCode) == int(3)):
    print("No data")
elif(int(loadFilesErrorCode) == int(4)):
    print("Data parse error")

districtDataErrorCode, districtData = loadDistrictData()
if(int(loadFilesErrorCode) == int(0)):
    print("Data have been successfully loaded")
elif(int(loadFilesErrorCode) == int(1)):
    print("Error loading the data")
    print("Full error message: " + districtData)
elif(int(loadFilesErrorCode) == int(2)):
    print("Data not found.")
elif(int(loadFilesErrorCode) == int(3)):
    print("No data")
elif(int(loadFilesErrorCode) == int(4)):
    print("Data parse error")

mocodesErrorCode, mocodesData = loadMocodesData()
if(int(loadFilesErrorCode) == int(0)):
    print("Data have been successfully loaded")
elif(int(loadFilesErrorCode) == int(1)):
    print("Error loading the data")
    print("Full error message: " + mocodesData)
elif(int(loadFilesErrorCode) == int(2)):
    print("Data not found.")
elif(int(loadFilesErrorCode) == int(3)):
    print("No data")
elif(int(loadFilesErrorCode) == int(4)):
    print("Data parse error")


ucrErrorCode, ucrData = loadUCRData()
if(int(loadFilesErrorCode) == int(0)):
    print("Data have been successfully loaded")
elif(int(loadFilesErrorCode) == int(1)):
    print("Error loading the data")
    print("Full error message: " + mocodesData)
elif(int(loadFilesErrorCode) == int(2)):
    print("Data not found.")

import sys as sys
import pandas as pd
import folium as folium
import numpy as np
from geocodio import GeocodioClient as GeocodioClient
import webbrowser as webbrowser
import os as os
from folium.plugins import MarkerCluster as MarkerCluster
import openrouteservice as openrouteservice
from openrouteservice import convert as convert
import json as json
import math as math
from numpy.core.numeric import NaN
from datetime import date as date
from datetime import datetime as datetime
from sklearn import model_selection as model_selection
from sklearn.tree import DecisionTreeRegressor as DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor as RandomForestRegressor
from sklearn.metrics import r2_score as r2_score
from sklearn.metrics import mean_squared_error as mean_squared_error
from math import sqrt as sqrt
from sklearn.model_selection import train_test_split as train_test_split
from sklearn.tree import export_graphviz as export_graphviz
import graphviz as graphviz

import data_visualization as DV
import data_processing as DP
import machine_learning as ML
import web_app as WB
import creds as CR

__all__ = [
    "sys",
    "pd",
    "folium",
    "np",
    "GeocodioClient",
    "webbrowser",
    "os",
    "MarkerCluster",
    "openrouteservice",
    "convert",
    "json",
    "DV",
    "DP",
    "ML",
    "WB",
    "CR",
    "mainData",
    "districtData",
    "math",
    "mocodesData",
    "datetime",
    "date",
    "model_selection", 
    "DecisionTreeRegressor", 
    "RandomForestRegressor", 
    "r2_score", 
    "mean_squared_error",
    "sqrt", 
    "train_test_split" ,
    "ucrData",
    "export_graphviz",
    "graphviz"]
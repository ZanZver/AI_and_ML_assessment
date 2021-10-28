#packages
import pip

#class Startup():


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
                        "PyQt5"]  
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
            return int(0)
        else:
            return int(1)

def loadData():
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

mainDataErrorCode, mainData = loadData()
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
    "mainData"]
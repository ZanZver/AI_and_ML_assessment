#packages
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

#check if modules are installed on the PC 
modules_used()
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
]


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
except Exception as e:
    print("data_processing.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

try:
    import machine_learning as ML
except Exception as e:
    print("machine_learning.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

try:
    import web_app as wb
except Exception as e:
    print("web_app.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

try:
    import creds as cr
except Exception as e:
    print("creds.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)


#=============================================================================================================================
import folium
import webbrowser
import os
import pandas as pd

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def myfunc(self):
        print("Hello my name is " + self.name)

class DataVisualization:
    def __init__(self, dataLAT, dataLON, crmCdDesc) -> None:
        self.dataLAT = dataLAT    
        self.dataLON = dataLON
        self.crmCdDesc = crmCdDesc
    
    def getLAT(self):
        return self.dataLAT

    def getLON(self):
        return self.dataLON

    def getCrmCdDesc(self):
        return self.crmCdDesc

    def createLocation(self):
        locationData = pd.DataFrame(data={
            'LAT': self.getLAT(), 
            'LON': self.getLON(),
            'crmCdDesc' : self.getCrmCdDesc()
            })
        return locationData

    def createMap(self):
        map = folium.Map(location=[34.052235, -118.243683], tiles="OpenStreetMap", zoom_start=14)
        locdf = self.createLocation()
        for index, location_info in locdf.iterrows():
            folium.CircleMarker(
                [location_info["LAT"], 
                location_info["LON"]],
                popup=location_info["crmCdDesc"],
                color='#69b3a2',
                fill=True,
                fill_color='#69b3a2'
                ).add_to(map)

        map.save("map.html")

    def openMap(self):
        webbrowser.open('file://' + os.path.realpath("map.html"))
        

#=============================================================================================================================
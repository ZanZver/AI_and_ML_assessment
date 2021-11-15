import sys
try:
    import startup as startup
except Exception as e:
    print("startup.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

from startup import *

globalMap = ""

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def myfunc(self):
        print("Hello my name is " + self.name)

class DataVisualization:
    def __init__(self,
        drNo,
        dateRptd,
        dateOcc,
        timeOcc,
        area,
        areaName,
        rptDistNo,
        part1or2,
        crmCd,
        crmCdDesc,
        mocodes,
        victAge,
        victSex,
        victDescent,
        premisCd,
        premisDesc,
        weaponUsedCd,
        weaponDesc,
        status,
        statusDesc,
        crmCd1,
        crmCd2,
        crmCd3,
        crmCd4,
        location,
        crossStreet,
        locLAT,
        locLON
    ) -> None:
        self.drNo = drNo
        self.dateRptd = dateRptd
        self.dateOcc = dateOcc
        self.timeOcc = timeOcc
        self.area = area
        self.areaName = areaName
        self.rptDistNo = rptDistNo
        self.part1or2 = part1or2
        self.crmCd = crmCd
        self.crmCdDesc = crmCdDesc
        self.mocodes = mocodes
        self.victAge = victAge
        self.victSex = victSex
        self.victDescent = victDescent
        self.premisCd = premisCd
        self.premisDesc = premisDesc
        self.weaponUsedCd = weaponUsedCd
        self.weaponDesc = weaponDesc
        self.status = status
        self.statusDesc = statusDesc
        self.crmCd1 = crmCd1
        self.crmCd2 = crmCd2
        self.crmCd3 = crmCd3
        self.crmCd4 =  crmCd4
        self.location = location
        self.crossStreet = crossStreet
        self.locLAT = locLAT
        self.locLON = locLON
        
        #do try catch
    
    def getLAT(self):
        return self.locLAT

    def getLON(self):
        return self.locLON

    def getCrmCdDesc(self):
        return self.crmCdDesc

    def groupData(self):
        pass
        #TODO: put data points to the group (based on lat and lon), use that for making circles bigger or smaller

    def createLocation(self):
        locationData = startup.pd.DataFrame(data={
            'LAT': self.getLAT(), 
            'LON': self.getLON()
            })
        return locationData

    def createLocationDetail(self):
        locationDataDetail = startup.pd.DataFrame(data={
            'LAT': self.getLAT(), 
            'LON': self.getLON(),
            'crmCdDesc' : self.getCrmCdDesc()
            })
        return locationDataDetail

    def createMap(self):
        map2 = startup.folium.Map(location=[34.052235, -118.243683], tiles='OpenStreetMap', zoom_start=11)

        marker_cluster = startup.MarkerCluster().add_to(map2)
        locationlist = self.createLocation().values.tolist()
      
        for point in range(0, len(locationlist)):
            startup.folium.Marker(
                locationlist[point],
                popup=self.createLocationDetail()['crmCdDesc'][point],
                color='#69b3a2',
                fill=True,
                fill_color='#69b3a2'
            ).add_to(marker_cluster)
            
        global globalMap
        globalMap = map2

        try:
            map2.save("map.html")
            print("Map created successfully")
            return [int(0), map2]
        except Exception as e:
            print("Error saving map")
            print("Error code: " + str(e))
            return [int(1), None]

    def findDirectionsMap(self, origin, destination):
        client = rou = geometry = coords = ""
        try:
            client = startup.openrouteservice.Client(key = startup.CR.openrouteserviceAPIkey)
            coords = (origin, destination)
            rou = client.directions(coords, profile='foot-walking')
            pathCoordinates = client.directions(coords, profile='foot-walking',format_out= 'geojson', preference ='shortest',geometry= 'true')
            pathCoordinates = (pathCoordinates['features'][0]['geometry']['coordinates']) #old print
            geometry = client.directions(coords, profile='foot-walking')['routes'][0]['geometry']
        except Exception as e:
            print("Error connecting to the OpenRouteService API, check your credentials.")
            print("Could not find direction")
            return (int(1), None)

        decoded = startup.convert.decode_polyline(geometry)

        distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(rou['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
        duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(rou['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
        
        errorCode, createdMap = self.createMap()
        if(errorCode == int(1)):
            return (int(1), None)
        elif(errorCode == int(0)):
            pass
        #it is faster to use cached map, but it doesn't work 100% atm...
        #startup.os.remove("map.html")
        #createdMap = globalMap
        
        startup.folium.GeoJson(decoded).add_child(startup.folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(createdMap)

        startup.folium.Marker(
            location=list(coords[0][::-1]),
            popup="Start",
            icon=startup.folium.Icon(color="green",icon='fas fa-map-marker-alt', prefix='fa'),
        ).add_to(createdMap)

        startup.folium.Marker(
            location=list(coords[1][::-1]),
            popup="Finish",
            icon=startup.folium.Icon(color="lightred",icon='fas fa-map-marker-alt', prefix='fa'),
        ).add_to(createdMap)

        #createdMap.save("map.html")
        #createdMap = None
        #del createdMap

        try:
            createdMap.save("map.html")
            print("Directions found successfully")
            #return pathCoordinates
            return (int(0), pathCoordinates)
        except Exception as e:
            print("Error saving map")
            print("Error code: " + str(e))
            return (int(1), None)

    def getPath(self, origin, destination):
        client = ""
        try:
            client = startup.GeocodioClient(startup.CR.geocodioAPIkey)
        except Exception as e:
            print("Error connecting to the GeoCodio API, check your credentials.")
            print("Could not decode origin and destination location.")
            return(int(1))

        origin_location = client.geocode(str(origin))
        destination_location = client.geocode(str(destination))
        errorCode, pathCoordinates = self.findDirectionsMap(origin_location.coords[::-1], destination_location.coords[::-1])

        retrunCode = (int(0) + int(errorCode)) #return sum of error codes, if it is 0, then everything is fine, otherwise error
        if(retrunCode == int(0)):
            print("Route created successfully")
            startup.ML.testFindCoords(pathCoordinates)
            return (int(0))
        else:
            print("Routing has failed")
            return (int(1))

    def openMap(self):
        startup.webbrowser.open('file://' + startup.os.path.realpath("map.html"))

#=============================================================================================================================

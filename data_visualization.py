
try:
    import startup as startup
except Exception as e:
    print("startup.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

from startup import *

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def myfunc(self):
        print("Hello my name is " + self.name)

class DataVisualization:
    def __init__(self,
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
        locationData = pd.DataFrame(data={
            'LAT': self.getLAT(), 
            'LON': self.getLON()
            })
        return locationData

    def createLocationDetail(self):
        locationDataDetail = pd.DataFrame(data={
            'LAT': self.getLAT(), 
            'LON': self.getLON(),
            'crmCdDesc' : self.getCrmCdDesc()
            })
        return locationDataDetail

    def createMap(self):
        map2 = folium.Map(location=[34.052235, -118.243683], tiles='OpenStreetMap', zoom_start=11)

        marker_cluster = MarkerCluster().add_to(map2)
        locationlist = self.createLocation().values.tolist()
      
        for point in range(0, len(locationlist)):
            folium.Marker(
                locationlist[point],
                popup=self.createLocationDetail()['crmCdDesc'][point],
                color='#69b3a2',
                fill=True,
                fill_color='#69b3a2'
            ).add_to(marker_cluster)
            
        map2.save("map.html")
        return map2

    def findDirectionsMap(self, origin, destination):
        client = openrouteservice.Client(key = startup.cr.openrouteserviceAPIkey)

        coords = (origin, destination)
        #coords = ((-118.374865,33.990057),(-118.179727,34.000304))
        #print(type(coords))
        rou = client.directions(coords, profile='foot-walking')
        #res = client.directions(coords,profile="foot-walking")
        geometry = client.directions(coords, profile='foot-walking')['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)

        distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(rou['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
        duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(rou['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
        
        createdMap = self.createMap()
        folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(createdMap)

        folium.Marker(
            location=list(coords[0][::-1]),
            popup="Galle fort",
            icon=folium.Icon(color="green"),
        ).add_to(createdMap)

        folium.Marker(
            location=list(coords[1][::-1]),
            popup="Jungle beach",
            icon=folium.Icon(color="red"),
        ).add_to(createdMap)

        createdMap.save('map.html')

        return(0)

    def testMarker4(self, origin, destination):
        client = GeocodioClient(startup.cr.geocodioAPIkey)
        origin_location = client.geocode(origin)
        destination_location = client.geocode(destination)
        self.findDirectionsMap(origin_location.coords[::-1], destination_location.coords[::-1])
        return(0)

    def openMap(self):
        webbrowser.open('file://' + os.path.realpath("map.html"))

#=============================================================================================================================

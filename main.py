import sys

try:
    import startup as startup
except Exception as e:
    print("startup.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

from startup import *

dfLite = mainData
 
d2 = startup.DP.DataProcessing(startup.mainData)
d2.builder()
#from pprint import pprint
#pprint(vars(d2))


#print("====================================================")
#print("1")
#d2.drNoConstructor()
#print("====================================================")
#print("2")
#d2.dateRptdConstructor()
#print("====================================================")
#print("3")
#d2.dateOccConstructor()
#print("====================================================")
#print("4")
#d2.timeOccConstructor()
#print("====================================================")
#print("5")
#d2.areaConstructor()
#print("====================================================")
#print("6")
#d2.areaNameConstructor()
#print("====================================================")
#print("7")
#d2.rptDistNoConstructor()
#print("====================================================")
#print("8")
#d2.part1or2Constructor()
#print("====================================================")
#print("9")
#d2.crmCdConstructor()
#print("====================================================")
#print("10")
#d2.crmCdDescConstructor()
#print("====================================================")
#print("11")
#d2.mocodesConstructor()
#print("====================================================")
#print("12")
#d2.victAgeConstructor()
#print("====================================================")
#print("13")
#d2.victSexConstructor()
#print("====================================================")
#print("14")
#d2.victDescentConstructor()
#print("====================================================")
#print("15")
#d2.premisCdConstructor()
#print("====================================================")
#print("16")
#d2.premisDescConstructor()
#print("====================================================")
#print("17")
#d2.weaponUsedCdConstructor()
#print("====================================================")
#print("18")
#d2.weaponDescConstructor()
#print("====================================================")
#print("19")
#d2.statusConstructor()
#print("====================================================")
#print("20")
#d2.statusDescConstructor()
#print("====================================================")
#print("21")
#d2.crmCd1Constructor()
#print("====================================================")
#print("22")
#d2.crmCd2Constructor()
#print("====================================================")
#print("23")
#d2.crmCd3Constructor()
#print("====================================================")
#print("24")
#d2.crmCd4Constructor()
#print("====================================================")
#print("25")
#d2.locationConstructor()
#print("====================================================")
#print("26")
#d2.crossStreetConstructor()
#print("====================================================")
#print("27")
#d2.latConstructor()
#print("====================================================")
#print("28")
#d2.lonConstructor()
#print("====================================================")
#d2.missingData()

#example of data vis
'''
d1 = startup.DV.DataVisualization(
    dateRptd = dfLite["Date Rptd"].values,
    dateOcc = dfLite["DATE OCC"].values,
    timeOcc = dfLite["TIME OCC"].values,
    area = dfLite["AREA "].values,
    areaName = dfLite["AREA NAME"].values,
    rptDistNo = dfLite["Rpt Dist No"].values,
    part1or2 = dfLite["Part 1-2"].values,
    crmCd = dfLite["Crm Cd"].values,
    crmCdDesc = dfLite["Crm Cd Desc"].values,
    mocodes = dfLite["Mocodes"].values,
    victAge = dfLite["Vict Age"].values,
    victSex = dfLite["Vict Sex"].values,
    victDescent = dfLite["Vict Descent"].values,
    premisCd = dfLite["Premis Cd"].values,
    premisDesc = dfLite["Premis Desc"].values,
    weaponUsedCd = dfLite["Weapon Used Cd"].values,
    weaponDesc = dfLite["Weapon Desc"].values,
    status = dfLite["Status"].values,
    statusDesc = dfLite["Status Desc"].values,
    crmCd1 = dfLite["Crm Cd 1"].values,
    crmCd2 = dfLite["Crm Cd 2"].values,
    crmCd3 = dfLite["Crm Cd 3"].values,
    crmCd4 = dfLite["Crm Cd 4"].values,
    location = dfLite["LOCATION"].values,
    crossStreet = dfLite["Cross Street"].values,
    locLAT = dfLite["LAT"].values,
    locLON = dfLite["LON"].values
    )

startup.WB.start(d1)
'''
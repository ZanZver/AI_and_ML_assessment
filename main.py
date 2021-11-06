import sys

try:
    import startup as startup
except Exception as e:
    print("Error in main.py - startup.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

from startup import *

#example of data processing
'''
d2 = startup.DP.DataProcessing(startup.mainData)
errorCode, data = d2.getCleanData()
if(int(errorCode) == int(1)):
    print("Error getting the clean data. Program has tried 3 times and failed 3 times. Stopping the program now.")
    sys.exit(1)
print(data)
'''

#example of data vis
'''
dfLite = startup.mainData
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
import sys

try:
    import startup as startup
except Exception as e:
    print("Error in main.py - startup.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

from startup import *

#example of data processing

d2 = startup.DP.DataProcessing(startup.mainData)
errorCode, data = d2.getCleanData()
if(int(errorCode) == int(1)):
    print("Error getting the clean data. Program has tried 3 times and failed 3 times. Stopping the program now.")
    sys.exit(1)
#print(data)


#example of data vis

dfLite = data
#print(dfLite)
#print(dfLite.columns.tolist())
#'Cross Street', 'LAT', 'LON']

d1 = startup.DV.DataVisualization(
    drNo = dfLite["DR_NO"].values,
    dateRptd = dfLite["Date Rptd"].values,
    dateOcc = dfLite["Date OCC"].values,
    timeOcc = dfLite["Time OCC"].values,
    area = dfLite["Area"].values,
    areaName = dfLite["Area name"].values,
    rptDistNo = dfLite["Rpt Dist No"].values,
    part1or2 = dfLite["Part 1-2"].values,
    crmCd = dfLite["Crm Cd"].values,
    crmCdDesc = dfLite["Crm Cd Desc"].values,
    mocodes = dfLite["Mocodes"].values,
    victAge = dfLite["Vict age"].values,
    victSex = dfLite["Vict sex"].values,
    victDescent = dfLite["Vict descent"].values,
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
    location = dfLite["Location"].values,
    crossStreet = dfLite["Cross Street"].values,
    locLAT = dfLite["LAT"].values,
    locLON = dfLite["LON"].values
    )

startup.WB.start(d1)

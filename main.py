import sys

try:
    import startup as startup
except Exception as e:
    print("Error in main.py - startup.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1) 

from startup import *

d2 = startup.DP.DataProcessing(startup.mainData)
errorCode, startup.mainData = d2.getCleanData()
if(int(errorCode) == int(1)):
    print("Error getting the clean data. Program has tried 3 times and failed 3 times. Stopping the program now.")
    sys.exit(1)

d1 = startup.DV.DataVisualization(
    drNo = startup.mainData["DR_NO"].values,
    dateRptd = startup.mainData["Date Rptd"].values,
    dateOcc = startup.mainData["Date OCC"].values,
    timeOcc = startup.mainData["Time OCC"].values,
    area = startup.mainData["Area"].values,
    areaName = startup.mainData["Area name"].values,
    rptDistNo = startup.mainData["Rpt Dist No"].values,
    part1or2 = startup.mainData["Part 1-2"].values,
    crmCd = startup.mainData["Crm Cd"].values,
    crmCdDesc = startup.mainData["Crm Cd Desc"].values,
    mocodes = startup.mainData["Mocodes"].values,
    victAge = startup.mainData["Vict age"].values,
    victSex = startup.mainData["Vict sex"].values,
    victDescent = startup.mainData["Vict descent"].values,
    premisCd = startup.mainData["Premis Cd"].values,
    premisDesc = startup.mainData["Premis Desc"].values,
    weaponUsedCd = startup.mainData["Weapon Used Cd"].values,
    weaponDesc = startup.mainData["Weapon Desc"].values,
    status = startup.mainData["Status"].values,
    statusDesc = startup.mainData["Status Desc"].values,
    crmCd1 = startup.mainData["Crm Cd 1"].values,
    crmCd2 = startup.mainData["Crm Cd 2"].values,
    crmCd3 = startup.mainData["Crm Cd 3"].values,
    crmCd4 = startup.mainData["Crm Cd 4"].values,
    location = startup.mainData["Location"].values,
    crossStreet = startup.mainData["Cross Street"].values,
    locLAT = startup.mainData["LAT"].values,
    locLON = startup.mainData["LON"].values
    )

startup.WB.start(d1)

from os import error
import sys

try:
    import startup as startup
except Exception as e:
    print("Error in data_processing.py -startup.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

from startup import *

globalMap = ""

'''
    Data info:
        DR_NO 
            |-> CSV type: text 
            |-> Description: Division of Records Number: Official file number made up of a 2 digit year, area ID, and 5 digits
            |-> Can be null: not
            |-> Example: 011401303
            |-> Add constrains: make sure it is a positive number
        
        Date Rptd 
            |-> CSV type: MM/DD/YYYY 
            |-> Description: Date of crime reported
            |-> Can be null: not
            |-> Example: 02/20/2010
            |-> Add constrains: make sure it is a valid date (not maybe not in the future)           
        
        DATE OCC 
            |-> CSV type: MM/DD/YYYY 
            |-> Description: Date when crime occurred
            |-> Can be null: not
            |-> Example: 02/20/2010
            |-> Add constrains: make sure it is a valid date (not maybe not in the future)  
        
        TIME OCC 
            |-> CSV type: text 
            |-> Description: Date when crime occurred
            |-> Can be null: not
            |-> Example: 1350
            |-> Add constrains: make sure it is a number between 0000 and 2400
        
        AREA 
            |-> CSV type: text 
            |-> Description: The LAPD has 21 Community Police Stations referred to as Geographic Areas within the department. 
                These Geographic Areas are sequentially numbered from 1-21.
            |-> Can be null: not
            |-> Example: 13
            |-> Add constrains: make sure the numbers are in the range of 1-21
        
        AREA NAME 
            |-> CSV type: text 
            |-> Description: The 21 Geographic Areas or Patrol Divisions are also given a name designation that references 
                a landmark or the surrounding community that it is responsible for. For example 77th Street Division is located 
                at the intersection of South Broadway and 77th Street, serving neighborhoods in South Los Angeles.
            |-> Can be null: not
            |-> Example: Newton
            |-> Add constrains: try to make sure it is a valid destination http://www.lacp.org/C-PAB%20News/BureauDivision.html
        
        Rpt Dist No 
            |-> CSV type: text 
            |-> Description: A four-digit code that represents a sub-area within a Geographic Area. All crime records reference 
                the "RD" that it occurred in for statistical comparisons. Find LAPD Reporting Districts on the LA City GeoHub.
            |-> Can be null: not
            |-> Example: 1385
            |-> Add constrains: make sure it is a positive number and a number from a list https://data.lacounty.gov/GIS-Data/Reporting-Districts/kvwy-dqs6

        
        Part 1-2 
            |-> CSV type: number 
            |-> Description: what type of offense is it (part 1 or part 2)
            |-> Can be null: not
            |-> Example: 2
            |-> Add constrains: make sure it is either 1 or 2
        
        Crm Cd 
            |-> CSV type: text 
            |-> Description: Indicates the crime committed. (Same as Crime Code 1)
            |-> Can be null: not
            |-> Example: 900
            |-> Add constrains: make sure it is a positive number (cannot verify from source)
        
        Crm Cd Desc 
            |-> CSV type: text 
            |-> Description: Defines the Crime Code provided.
            |-> Can be null: not
            |-> Example: VIOLATION OF COURT ORDER
            |-> Add constrains: make sure it is not null (text)
        
        Mocodes 
            |-> CSV type: text 
            |-> Description: Modus Operandi: Activities associated with the suspect in commission of the crime. 
                See attached PDF for list of MO Codes in numerical order.
            |-> Can be null: not
            |-> Example: 0913 1814 2000
            |-> Add constrains: make sure the number is from the list, and then match it up (0913 to str + 1814 to str + 2000 to str)
        
        Vict Age 
            |-> CSV type: text 
            |-> Description: Age of the victim
            |-> Can be null: not
            |-> Example: 48
            |-> Add constrains: make sure the age is at least 10 years or over

        Vict Sex 
            |-> CSV type: text
            |-> Description: 
                F - Female 
                M - Male 
                X - Unknown
            |-> Can be null: not    
            |-> Example: M
            |-> Add constrains: make sure the string (or char) is valid -> don't accept "male" for example

        Vict Descent 
            |-> CSV type: text 
            |-> Description:  
                    Descent Code: 
                        A - Other Asian 
                        B - Black 
                        C - Chinese 
                        D - Cambodian 
                        F - Filipino 
                        G - Guamanian 
                        H - Hispanic/Latin/Mexican 
                        I - American Indian/Alaskan Native 
                        J - Japanese 
                        K - Korean 
                        L - Laotian 
                        O - Other 
                        P - Pacific Islander 
                        S - Samoan 
                        U - Hawaiian 
                        V - Vietnamese 
                        W - White 
                        X - Unknown 
                        Z - Asian Indian
            |-> Can be null: not
            |-> Example: H
            |-> Add constrains: make sure the string (or char) is valid -> don't accept "white" for example
        
        Premis Cd 
            |-> CSV type: text 
            |-> Description: The type of structure, vehicle, or location where the crime took place.
            |-> Can be null: not
            |-> Example: 501
            |-> Add constrains: make sure it is a valid number (positive), cannot find a source
        
        Premis Desc 
            |-> CSV type: text 
            |-> Description: Defines the Premise Code provided.
            |-> Can be null: not
            |-> Example: SINGLE FAMILY DWELLING
            |-> Add constrains: make sure string is valid (not null)
        
        Weapon Used Cd 
            |-> CSV type: text 
            |-> Description: The type of weapon used in the crime.
            |-> Can be null: yes
            |-> Example: " " or 102
            |-> Add constrains: if it is null (empty) replace it with 0 and say "none", otherwise make sure number is valid
        
        Weapon Desc 
            |-> CSV type: text 
            |-> Description: Defines the Weapon Used Code provided.
            |-> Can be null: yes
            |-> Example: HAND GUN
            |-> Add constrains: make sure string is valid (not null)
        
        Status 
            |-> CSV type: text 
            |-> Description: Status of the case. (IC is the default)
            |-> Can be null: not
            |-> Example: AA
            |-> Add constrains: make sure string is valid (not null)
        
        Status Desc 
            |-> CSV type: text 
            |-> Description: Defines the Status Code provided
            |-> Can be null: not
            |-> Example: Adult Arrest
            |-> Add constrains: make sure string is valid (not null)

        Crm Cd 1 
            |-> CSV type: text 
            |-> Description: Indicates the crime committed. Crime Code 1 is the primary and most serious one. 
                Crime Code 2, 3, and 4 are respectively less serious offenses. Lower crime class numbers are more serious.
            |-> Can be null: not
            |-> Example: 900
            |-> Add constrains: make sure the number is in a valid range and that it isn't null

        Crm Cd 2 
            |-> CSV type: text 
            |-> Description: May contain a code for an additional crime, less serious than Crime Code 1.
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: check it is null, if not make sure the number is in valid range
        
        Crm Cd 3 
            |-> CSV type: text 
            |-> Description: May contain a code for an additional crime, less serious than Crime Code 1.
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: check it is null, if not make sure the number is in valid range
        
        Crm Cd 4 
            |-> CSV type: text 
            |-> Description: May contain a code for an additional crime, less serious than Crime Code 1.
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: check it is null, if not make sure the number is in valid range
        
        LOCATION 
            |-> CSV type: text 
            |-> Description: Street address of crime incident rounded to the nearest hundred block to maintain anonymity.
            |-> Can be null: not
            |-> Example: 300 E GAGE AV
            |-> Add constrains: Make sure it is not null or less than 5 characters
        
        Cross Street 
            |-> CSV type: text 
            |-> Description: Cross Street of rounded Address
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: it can be null
        
        LAT 
            |-> CSV type: number 
            |-> Description: Latitude
            |-> Can be null: not
            |-> Example: 33.9825
            |-> Add constrains: make sure it is not null and it starts with 33
        
        LON 
            |-> CSV type: number 
            |-> Description: Longitude
            |-> Can be null: not
            |-> Example: -118.2695
            |-> Add constrains: make sure it is not null and it starts with -118
'''

class DataProcessing:
    def __init__(self, originalDataset):
        self.drNo = originalDataset["DR_NO"].values
        self.dateRptd = originalDataset["Date Rptd"].values
        self.dateOcc = originalDataset["DATE OCC"].values
        self.timeOcc = originalDataset["TIME OCC"].values
        self.area = originalDataset["AREA "].values
        self.areaName = originalDataset["AREA NAME"].values
        self.rptDistNo = originalDataset["Rpt Dist No"].values
        self.part1or2 = originalDataset["Part 1-2"].values
        self.crmCd = originalDataset["Crm Cd"].values
        self.crmCdDesc = originalDataset["Crm Cd Desc"].values
        self.mocodes = originalDataset["Mocodes"].values
        self.victAge = originalDataset["Vict Age"].values
        self.victSex = originalDataset["Vict Sex"].values
        self.victDescent = originalDataset["Vict Descent"].values
        self.premisCd = originalDataset["Premis Cd"].values
        self.premisDesc = originalDataset["Premis Desc"].values
        self.weaponUsedCd = originalDataset["Weapon Used Cd"].values
        self.weaponDesc = originalDataset["Weapon Desc"].values
        self.status = originalDataset["Status"].values
        self.statusDesc = originalDataset["Status Desc"].values
        self.crmCd1 = originalDataset["Crm Cd 1"].values
        self.crmCd2 = originalDataset["Crm Cd 2"].values
        self.crmCd3 = originalDataset["Crm Cd 3"].values
        self.crmCd4 = originalDataset["Crm Cd 4"].values
        self.location = originalDataset["LOCATION"].values
        self.crossStreet = originalDataset["Cross Street"].values
        self.locLat = originalDataset["LAT"].values
        self.locLon = originalDataset["LON"].values
        #self.errorList = []

    def __repr__(self):
        return ("string shown to developers (at REPL)")

    def contains_duplicates(self, X):
        seen = set()
        seen_add = seen.add
        for x in X:
            if (x in seen or seen_add(x)):
                return True
        return False

    def builder(self, tryCount):
        arr = startup.np.stack((
            self.getDrNo(),
            self.getDateRptd(),
            self.getDateOcc(),
            self.getTimeOcc(),
            self.getArea(),
            self.getAreaName(),
            self.getRptDistNo(),
            self.getPart1or2(),
            self.getCrmCd(),
            self.getCrmCdDesc(),
            self.getMocodes(),
            self.getVictAge(),
            self.getVictSex(),
            self.getVictDescent(),
            self.getPremisCd(),
            self.getPremisDesc(),
            self.getWeaponUsedCd(),
            self.getWeaponDesc(),
            self.getStatus(),
            self.getStatusDesc(),
            self.getCrmCd1(),
            self.getCrmCd2(),
            self.getCrmCd3(),
            self.getCrmCd4(),
            self.getLocation(),
            self.getCrossStreet(),
            self.getLat(),
            self.getLon()), axis=1
        )
        
        arr2 = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
        count = int(0)
        itemsRemoved = int(0)
        #print(arr)
        for item in arr:
            errorCount = int(0)

            #item 0
            errno0, drNo = (self.drNoConstructor(item[0]))
            if(errno0 == (int(0))):
                item[0] = int(drNo) #replace type from str to int
            else:
                errorCount += 1
            
            #item 1
            errno1, dateRptd = self.dateRptdConstructor(item[1])
            if(errno1 == (int(0))):
                item[1] = str(dateRptd) #replace type from str to int
            else:
                errorCount += 1
                #print("here: " + item[1])
            #item 2
            errno2, dateOcc = self.dateOccConstructor(item[2])
            if(errno2 == (int(0))):
                item[2] = str(dateOcc) #replace type from str to int
            else:
                errorCount += 1
                #print("here: " + item[2])

            #item 3
            errno3, timeOcc = self.timeOccConstructor(item[3])
            if(errno3 == (int(0))):
                item[3] = timeOcc #replace type from str to int
            else:
                errorCount += 1
                #print("here: " + item[3])

            #item 4
            errno4, area = self.areaConstructor(item[4])
            if(errno4 == (int(0))):
                item[4] = int(area)
            else:
                errorCount += 1
                #print("here: " + item[4])

            #item 5
            errno5, areaName = self.areaNameConstructor(item[5])
            if(errno5 == (int(0))):
                item[5] = str(areaName)
            else:
                errorCount += 1
                #print("here: " + item[5])

            #item 6   
            errno6, rptDistNo = self.rptDistNoConstructor(item[6])
            if(errno6 == (int(0))):
                item[6] = int(rptDistNo)
            else:
                errorCount += 1  
                #print("here: " + item[6])   
            
            #item 7
            errno7, part1or2 = self.part1or2Constructor(item[7])
            if(errno7 == (int(0))):
                item[7] = int(part1or2)
            else:
                errorCount += 1  
                #print("here: " + item[7])

            #item 8
            errno8, crmCd = self.crmCdConstructor(item[8])
            if(errno8 == (int(0))):
                item[8] = int(crmCd)
            else:
                errorCount += 1 
                #print("here: " + item[8])

            #item 9
            errno9, crmCdDesc = self.crmCdDescConstructor(item[9])  
            if(errno9 == (int(0))):
                    item[9] = str(crmCdDesc)
            else:
                errorCount += 1 
                #print("here: " + item[9])

            #item 10
            errno10, mocodes =  self.mocodesConstructor(item[10])
            if(errno10 == (int(0))):
                item[10] = list(mocodes)
            else:
                errorCount += 1 
                #print("here: " + item[10])

            #item 11
            errno11, victAge = self.victAgeConstructor(item[11])
            if(errno11 == (int(0))):
                item[11] = int(victAge)
            else:
                errorCount += 1
                #print("here: " + str(item[11]))

            #item 12
            errno12, victSex = self.victSexConstructor(item[12])
            if(errno12 == (int(0))):
                item[12] = str(victSex)
            else:
                errorCount += 1
                #print("here: " + item[12])

            #item 13
            errno13, victDescent = self.victDescentConstructor(item[13])
            if(errno13 == (int(0))):
                item[13] = str(victDescent)
            else:
                errorCount += 1
                #print("here: " + item[13])

            #item 14
            errno14, remisCd = self.premisCdConstructor(item[14])
            if(errno14 == (int(0))):
                item[14] = int(remisCd)
            else:
                errorCount += 1
                #print("here: " + item[14])

            #item 15
            errno15, premisDesc = self.premisDescConstructor(item[15])
            if(errno15 == (int(0))):
                item[15] = str(premisDesc)
            else:
                errorCount += 1
                #print("here: " + item[15])

            #item 16
            errno16, weaponUsed = self.weaponUsedCdConstructor(item[16])
            if(errno16 == (int(0))):
                item[16] = str(weaponUsed)
            else:
                errorCount += 1
                #print("here: " + item[16])

            #item 17
            errno17, weaponDesc = self.weaponDescConstructor(item[17])
            if(errno17 == (int(0))):
                item[17] = str(weaponDesc)
            else:
                errorCount += 1
                #print("here: " + item[17])

            #item 18
            errno18, status = self.statusConstructor(item[18])
            if(errno18 == (int(0))):
                item[18] = str(status)
            else:
                errorCount += 1
                #print("here: " + item[18])

            #item 19
            errno19, statusDesc = self.statusDescConstructor(item[19])
            if(errno19 == (int(0))):
                item[19] = str(statusDesc)
            else:
                errorCount += 1
                #print("here: " + item[19])

            #item 20
            errno20, crmCd1 = self.crmCd1Constructor(item[20])
            if(errno20 == (int(0))):
                item[20] = str(crmCd1)
            else:
                errorCount += 1
                #print("here: " + item[20])

            #item 21
            errno21, crmCd2 = self.crmCd2Constructor(item[21])
            if(errno21 == (int(0))):
                item[21] = str(crmCd2)
            else:
                errorCount += 1
                #print("here: " + item[21])

            #item 22
            errno22, crmCd3 = self.crmCd3Constructor(item[22])
            if(errno22 == (int(0))):
                item[22] = str(crmCd3)
            else:
                errorCount += 1
                #print("here: " + item[22])
            
            
            #item 23
            errno23, crmCd4 = self.crmCd4Constructor(item[23])
            if(errno23 == (int(0))):
                item[23] = str(crmCd4)
            else:
                errorCount += 1
                #print("here: " + item[23])

            #item 24
            errno24, location = self.locationConstructor(item[24])
            if(errno24 == (int(0))):
                item[24] = str(location)
            else:
                errorCount += 1
                #print("here: " + item[24])

            #item 25
            errno25, crossStreet = self.crossStreetConstructor(item[25])
            if(errno25 == (int(0))):
                item[25] = str(crossStreet)
            else:
                errorCount += 1
                #print("here: " + item[25])

            #item 26
            errno26, lat = self.latConstructor(item[26])
            if(errno26 == (int(0))):
                item[26] = float(lat)
            else:
                errorCount += 1
                #print("here: " + item[26])

            #item 27
            errno27, lon = self.lonConstructor(item[27])
            if(errno27 == (int(0))):
                item[27] = float(lon)
            else:
                errorCount += 1
                #print("here: " + item[27])

            if(errorCount == int(0)):
                count +=1 
                arr2 = startup.np.vstack([arr2, item])
            elif(errorCount != int(0)):
                itemsRemoved +=1
                
        arr2 = startup.np.delete(arr2, (0), axis=0)
        print("Items removed: " + str(itemsRemoved))
        columnNames = [
            "DR_NO",
            "Date Rptd",
            "Date OCC",
            "Time OCC",
            "Area",
            "Area name",
            "Rpt Dist No",
            "Part 1-2",
            "Crm Cd",
            "Crm Cd Desc",
            "Mocodes",
            "Vict age",
            "Vict sex",
            "Vict descent",
            "Premis Cd",
            "Premis Desc",
            "Weapon Used Cd",
            "Weapon Desc",
            "Status",
            "Status Desc",
            "Crm Cd 1",
            "Crm Cd 2",
            "Crm Cd 3",
            "Crm Cd 4",
            "Location",
            "Cross Street",
            "LAT",
            "LON"
        ]

        df = startup.pd.DataFrame() 
        try:
            df = startup.pd.DataFrame(arr2, columns = columnNames)
        except:
            print("Error making clean dataFrame")
            return(int(1), None, tryCount)

        try:
            if df.empty:
                print('Error, dataFrame is empty!')
                return(int(1), None, tryCount)
        except:
            pass

        try:
            df.to_csv("Data/cleanData.csv")
            return(int(0), df, tryCount)
        except:
            print("Error saving cleanData.csv file")
            return(int(1), None, tryCount)
        
    def getCleanData(self, tryCount = 0):
        try:
            cleanDataFrame = startup.pd.read_csv("Data/cleanData.csv", index_col=0)
            print("Clean data have been successfully loaded.")
            return(int(0), cleanDataFrame)
        except FileNotFoundError:
            errorCode, cleanDataFrame, tryCount= self.builder(tryCount)
            if(int(errorCode) == int(0)):
                return(int(0), cleanDataFrame)
            elif(int(errorCode) == int(1)):
                return(int(1), None)
            elif(int(tryCount) >= int(3)):
                return(int(1), None)
        except startup.pd.errors.EmptyDataError: #remove the file, create new one
            if(int(tryCount) >= int(3)):
                return(int(1), None)
            print("File is empty, removing the file and creating new file.")
            startup.os.remove("Data/cleanData.csv")
            tryCount += 1
            return(self.getCleanData(tryCount))
        except startup.pd.errors.ParserError: #remove the file, create new one
            if(int(tryCount) >= int(3)):
                return(int(1), None)
            print("Error parsing the file, removing the file and creating new file.")
            startup.os.remove("Data/cleanData.csv")
            tryCount += 1
            return(self.getCleanData(tryCount))
        except Exception as e:
            print("Exceptrion: " + str(e))
            return(int(1), None)

    def drNoConstructor(self,drNo):
        '''
        DR_NO 
            |-> CSV type: text 
            |-> Description: Division of Records Number: Official file number made up of a 2 digit year, area ID, and 5 digits
            |-> Can be null: not
            |-> Example: 011401303
            |-> Add constrains: make sure it is a positive number
        '''

        try:
            drNo = int(drNo)
            #print(string_int)
        except ValueError:
            # Handle the exception
            return [int(1), None]

        if (drNo > int(0)):
            return [int(0), int(drNo)]
        else:
            return [int(1), None]

        #print("DR NO")
        #print(self.getDrNo())
        #print(type(self.getDrNoConstructor()))
        #print(self.contains_duplicates(self.getDrNoConstructor()))
        #print(startup.np.isnan(self.getDrNoConstructor()).sum())
    
    def getDrNo(self):
        return self.drNo

    def dateRptdConstructor(self, dateRptd):
        '''      
        Date Rptd 
            |-> CSV type: MM/DD/YYYY 
            |-> Description: Date of crime reported
            |-> Can be null: not
            |-> Example: 02/20/2010
            |-> Add constrains: make sure it is a valid date (not maybe not in the future)           
        '''
        try:
            dateOfTime=(dateRptd[:11]).strip()
            hourOfTime=(dateRptd[11:]).strip()
        except:
            return [int(1), None]

        try:
            if hourOfTime[-2:] == "AM" :
                if hourOfTime[:2] == '12':
                    hourOfTime = str('00' + hourOfTime[2:8])
                else:
                    hourOfTime = hourOfTime[:-2]
            else:
                if hourOfTime[:2] == '12':
                    hourOfTime = hourOfTime[:-2]
                else:
                    hourOfTime = str(int(hourOfTime[:2]) + 12) + hourOfTime[2:8]
        except:
            return [int(1), None]

        dateRptd = dateOfTime + " "+ hourOfTime
        
        try:
            dateRptd = startup.datetime.strptime(dateRptd, "%m/%d/%Y %H:%M:%S")
            return [int(0), str(dateRptd)]
        except Exception as e:
            return [int(1), None]

    def getDateRptd(self):
        return self.dateRptd

    def dateOccConstructor(self, dateOcc):
        '''
        DATE OCC 
            |-> CSV type: MM/DD/YYYY 
            |-> Description: Date when crime occurred
            |-> Can be null: not
            |-> Example: 02/20/2010
            |-> Add constrains: make sure it is a valid date (not maybe not in the future)  

        '''
        if not dateOcc:
            return [int(1), None]
        try:
            dateOfTime=(dateOcc[:11]).strip()
            hourOfTime=(dateOcc[11:]).strip()
        except:
            return [int(1), None]

        try:
            if hourOfTime[-2:] == "AM" :
                if hourOfTime[:2] == '12':
                    hourOfTime = str('00' + hourOfTime[2:8])
                else:
                    hourOfTime = hourOfTime[:-2]
            else:
                if hourOfTime[:2] == '12':
                    hourOfTime = hourOfTime[:-2]
                else:
                    hourOfTime = str(int(hourOfTime[:2]) + 12) + hourOfTime[2:8]
        except:
            return [int(1), None]

        dateOcc = dateOfTime + " "+ hourOfTime
        
        try:
            dateOcc = startup.datetime.strptime(dateOcc, "%m/%d/%Y %H:%M:%S")
            return [int(0), str(dateOcc)]
        except Exception as e:
            
            return [int(1), None]

    def getDateOcc(self):
        return self.dateOcc

    def timeOccConstructor(self,timeOcc):
        ''' 
        TIME OCC 
            |-> CSV type: text 
            |-> Description: Date when crime occurred
            |-> Can be null: not
            |-> Example: 1350
            |-> Add constrains: make sure it is a number between 0000 and 2400
        ''' 
        try:
            timeOcc = int(timeOcc)
        except:
            return [int(1), None]

        strLen = int(len(str(timeOcc)))
        if(int(strLen) == int(4)):
            pass
        elif(int(strLen) == int(3)):
            timeOcc = str("0") + str(timeOcc)
        elif(int(strLen) == int(2)):
            timeOcc = str("00") + str(timeOcc)
        elif(int(strLen) == int(1)):
            timeOcc = str("000") + str(timeOcc)
        else:
            return [int(1), None]

        hourOfTime = minuteOfTime = ""
        try:
            hourOfTime=(str(timeOcc)[:2]).strip()
            minuteOfTime=(str(timeOcc)[2:]).strip()
            timeOcc = hourOfTime +":"+minuteOfTime
        except:
            return [int(1), None]

        try:
            timeOcc = startup.datetime.strptime(timeOcc, "%H:%M").time()
            return [int(0), timeOcc]
        except:
            return [int(1), None]
        #print(timeOcc)

    def getTimeOcc(self):
        return self.timeOcc

    def areaConstructor(self,area):
        ''' 
        AREA 
            |-> CSV type: text 
            |-> Description: The LAPD has 21 Community Police Stations referred to as Geographic Areas within the department. 
                These Geographic Areas are sequentially numbered from 1-21.
            |-> Can be null: not
            |-> Example: 13
            |-> Add constrains: make sure the numbers are in the range of 1-21
        ''' 
        try:
            area = int(area)
        except:
            return [int(1), None]

        if 1 <= area <= 21:
            return [int(0), int(area)]
        else:
            return [int(1), None]

    def getArea(self):
        return self.area

    def areaNameConstructor(self, areaName):
        ''' 
        AREA NAME 
            |-> CSV type: text 
            |-> Description: The 21 Geographic Areas or Patrol Divisions are also given a name designation that references 
                a landmark or the surrounding community that it is responsible for. For example 77th Street Division is located 
                at the intersection of South Broadway and 77th Street, serving neighborhoods in South Los Angeles.
            |-> Can be null: not
            |-> Example: Newton
            |-> Add constrains: try to make sure it is a valid destination http://www.lacp.org/C-PAB%20News/BureauDivision.html
        ''' 
        areaNameList = [
            "Devonshire",
            "Foothill",
            "N. Hollywood",
            "Van Nuys",
            "West Valley",
            "Hollywood",
            "Pacific",
            "West LA",
            "Wilshire",
            "Central",
            "Hollenbeck",
            "Newton",
            "Northeast",
            "Rampart",
            "77th Street",
            "Harbor",
            "Southeast",
            "Southwest"]

        try:
            if areaName in areaNameList:
                return [int(0), str(areaName)]
            else:
                return [int(1), None]
        except:
            return [int(1), None]

    def getAreaName(self):
        return self.areaName

    def rptDistNoConstructor(self, rptDistNo):
        ''' 
        Rpt Dist No 
            |-> CSV type: text 
            |-> Description: A four-digit code that represents a sub-area within a Geographic Area. All crime records reference 
                the "RD" that it occurred in for statistical comparisons. Find LAPD Reporting Districts on the LA City GeoHub.
            |-> Can be null: not
            |-> Example: 1385
            |-> Add constrains: make sure it is a positive number and a number from a list https://data.lacounty.gov/GIS-Data/Reporting-Districts/kvwy-dqs6
        ''' 
        try:
            rptDistNo = int(rptDistNo)
        except:
            return [int(1), None]
        
        if rptDistNo in startup.districtData["OBJECTID"].values:
            return [int(0), int(rptDistNo)]
        else:
            return [int(1), None]
   
    def getRptDistNo(self):
        return self.rptDistNo

    def part1or2Constructor(self,part1or2):
        ''' 
        Part 1-2 
            |-> CSV type: number 
            |-> Description: what type of offense is it (part 1 or part 2)
            |-> Can be null: not
            |-> Example: 2
            |-> Add constrains: make sure it is either 1 or 2
        ''' 
        try:
            part1or2 = int(part1or2)
        except:
            return [int(1), None]

        if 1 <= part1or2 <= 2:
            return [int(0), int(part1or2)]
        else:
            return [int(1), None]
    
    def getPart1or2(self):
        return self.part1or2

    def crmCdConstructor(self,crmCd):
        ''' 
        Crm Cd 
            |-> CSV type: text 
            |-> Description: Indicates the crime committed. (Same as Crime Code 1)
            |-> Can be null: not
            |-> Example: 900
            |-> Add constrains: make sure it is a positive number (cannot verify from source)
        ''' 
        
        crmCd = str(crmCd).strip()
        try:
            if(startup.math.isnan(float(crmCd))):
                crmCd = 0
        except:
            pass

        try:
            if(int(len(str(crmCd))) == 0):
                crmCd = 0
        except:
            pass

        try:
            crmCd = int(crmCd)
            return [int(0), int(crmCd)]
        except:
            return [int(1), None]
        
    def getCrmCd(self):
        return self.crmCd

    def crmCdDescConstructor(self,crmCdDesc):
        ''' 
        Crm Cd Desc 
            |-> CSV type: text 
            |-> Description: Defines the Crime Code provided.
            |-> Can be null: not
            |-> Example: VIOLATION OF COURT ORDER
            |-> Add constrains: make sure it is not null (text)
        ''' 
        crmCdDesc = str(crmCdDesc).strip()

        try:
            crmCdDesc = int(crmCdDesc)
            return [int(1), None]
        except:
            pass

        try:
            if(startup.math.isnan(float(crmCdDesc))):
                return [int(1), None]
        except:
            pass

        try:
            if(int(len(str(crmCdDesc))) == 0):
                return [int(1), None]
        except:
            pass

        try:
            crmCdDesc = str(crmCdDesc)
            return [int(0), str(crmCdDesc)]
        except:
            return [int(1), None]

    def getCrmCdDesc(self):
        return self.crmCdDesc

    def mocodesConstructor(self, mocodes):
        ''' 
        Mocodes 
            |-> CSV type: text 
            |-> Description: Modus Operandi: Activities associated with the suspect in commission of the crime. 
                See attached PDF for list of MO Codes in numerical order.
            |-> Can be null: not
            |-> Example: 0913 1814 2000
            |-> Checking is done from the "MO_CODES_Numerical_20191119.pdf" file that was converted to the json
            |-> Add constrains: make sure the number is from the list, and then match it up (0913 to str + 1814 to str + 2000 to str)
        ''' 
        mocodesList = []
        try:
            mocodesList = mocodes.split(' ')
        except:
            pass
        
        for e in (mocodesList):
            try:
                if int(e) in startup.mocodesData.index:
                    pass
                else:
                    mocodesList.remove(e)
            except:
                mocodesList.remove(e)

        if len(mocodesList) != 0:
            return (int(0), list(mocodesList))
        else:
            return (int(1), None)

    def getMocodes(self):
        return self.mocodes

    def victAgeConstructor(self,victAge):
        ''' 
        Vict Age 
            |-> CSV type: text 
            |-> Description: Age of the victim
            |-> Can be null: not
            |-> Example: 48
            |-> Add constrains: make sure the age is at least 10 years or over
        ''' 
        #print(victAge)
        try:
            victAge = int(victAge)
        except:
            return [int(1), None]

        if 10 <= victAge <= 150:
            return [int(0), int(victAge)]
        else:
            return [int(1), None]

    def getVictAge(self):
        return self.victAge

    def victSexConstructor(self, victSex):
        ''' 
        Vict Sex 
            |-> CSV type: text
            |-> Description: 
                F - Female 
                M - Male 
                X - Unknown
            |-> Can be null: not    
            |-> Example: M
            |-> Add constrains: make sure the string (or char) is valid -> don't accept "male" for example
        ''' 
        sexList = [
            "M",
            "F"]
       
        try:       
            if(startup.math.isnan(float(victSex))):                 
                return [int(1), None]         
        except:             
            pass               

        try:
            victSex = victSex.strip()
        except:
            return [int(1), None]

        try:
            if victSex in sexList:
                return [int(0), str(victSex)]
            else:
                return [int(1), None]
        except:
            return [int(1), None]

    def getVictSex(self):
        return self.victSex

    def victDescentConstructor(self, victDescent):
        ''' 
        Vict Descent 
            |-> CSV type: text 
            |-> Description:  
                    Descent Code: 
                        A - Other Asian 
                        B - Black 
                        C - Chinese 
                        D - Cambodian 
                        F - Filipino 
                        G - Guamanian 
                        H - Hispanic/Latin/Mexican 
                        I - American Indian/Alaskan Native 
                        J - Japanese 
                        K - Korean 
                        L - Laotian 
                        O - Other 
                        P - Pacific Islander 
                        S - Samoan 
                        U - Hawaiian 
                        V - Vietnamese 
                        W - White 
                        X - Unknown 
                        Z - Asian Indian
            |-> Can be null: not
            |-> Example: H
            |-> Add constrains: make sure the string (or char) is valid -> don't accept "white" for example
        ''' 
        victDescentList = [
            "M",
            "F",
            "A",
            "B",
            "C",
            "D",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "O",
            "P",
            "S",
            "U",
            "V",
            "W",
            "X",
            "Z"]
        
        try:       
            if(startup.math.isnan(float(victDescent))):                 
                return [int(1), None]         
        except:             
            pass 

        try:
            victDescent = victDescent.strip()
        except:
            return [int(1), None] 

        try:
            if victDescent in victDescentList:
                return [int(0), str(victDescent)]
            else:
                return [int(1), None]
        except:
            return [int(1), None]

    def getVictDescent(self):
        return self.victDescent

    def premisCdConstructor(self, premisCd):
        ''' 
        Premis Cd 
            |-> CSV type: text 
            |-> Description: The type of structure, vehicle, or location where the crime took place.
            |-> Can be null: not
            |-> Example: 501
            |-> Add constrains: make sure it is a valid number (positive), cannot find a source
        ''' 
        try:
            premisCd = int(premisCd)    
        except:
            return [int(1), None]

        if int(premisCd) > 0:
            return [int(0), int(premisCd)]
        else:
            return [int(1), None]

    def getPremisCd(self):
        return self.premisCd

    def premisDescConstructor(self, premisDesc):
        ''' 
        Premis Desc 
            |-> CSV type: text 
            |-> Description: Defines the Premise Code provided.
            |-> Can be null: not
            |-> Example: SINGLE FAMILY DWELLING
            |-> Add constrains: make sure string is valid (not null)
        ''' 
        premisDesc = str(premisDesc).strip()

        try:
            premisDesc = int(premisDesc)
            return [int(1), None]
        except:
            pass

        try:
            if(startup.math.isnan(float(premisDesc))):
                return [int(1), None]
        except:
            pass

        try:
            if(int(len(str(premisDesc))) == 0):
                return [int(1), None]
        except:
            pass

        try:
            premisDesc = str(premisDesc)
            return [int(0), str(premisDesc)]
        except:
            return [int(1), None]

    def getPremisDesc(self):
        return self.premisDesc

    def weaponUsedCdConstructor(self, weaponUsedCd):
        ''' 
        Weapon Used Cd 
            |-> CSV type: text 
            |-> Description: The type of weapon used in the crime.
            |-> Can be null: yes
            |-> Example: " " or 102
            |-> Add constrains: if it is null (empty) replace it with 0 and say "none", otherwise make sure number is valid
        ''' 
        
        weaponUsedCd = str(weaponUsedCd).strip()
        try:
            if(startup.math.isnan(float(weaponUsedCd))):
                weaponUsedCd = 0
        except:
            pass
        
        #print(weaponUsedCd)
        try:
            weaponUsedCd = int(startup.math.trunc(float(weaponUsedCd)))
        except:
            #print(weaponUsedCd)
            return [int(1), None]

        #print(weaponUsedCd)
        try:
            weaponUsedCd = int(weaponUsedCd)
            return [int(0), int(weaponUsedCd)]
        except:
            return [int(1), None]

    def getWeaponUsedCd(self):
        return self.weaponUsedCd

    def weaponDescConstructor(self, weaponDesc):
        ''' 
        Weapon Desc 
            |-> CSV type: text 
            |-> Description: Defines the Weapon Used Code provided.
            |-> Can be null: yes
            |-> Example: HAND GUN
            |-> Add constrains: make sure string is valid (not null)
        ''' 
        try:
            weaponDesc = int(weaponDesc)
            return [int(1), None]
        except:
            pass

        try:
            if(startup.math.isnan(float(weaponDesc))):
                weaponDesc = "None"
        except:
            pass
        
        return [int(0), str(weaponDesc)]

    def getWeaponDesc(self):
        return self.weaponDesc

    def statusConstructor(self,status):
        ''' 
        Status 
            |-> CSV type: text 
            |-> Description: Status of the case. (IC is the default)
            |-> Can be null: not
            |-> Example: AA
            |-> Add constrains: make sure string is valid (not null)
        ''' 
        try:
            if(startup.math.isnan(float(status))):
                return [int(1), None]
        except:
            pass

        status = status.strip()
        try:
            if((len(status)) == int(0)):
                return [int(1), None]
        except:
            pass
        
        return [int(0), str(status)]
        #print(status)

    def getStatus(self):
        return self.status

    def statusDescConstructor(self,statusDesc):
        ''' 
        Status Desc 
            |-> CSV type: text 
            |-> Description: Defines the Status Code provided
            |-> Can be null: not
            |-> Example: Adult Arrest
            |-> Add constrains: make sure string is valid (not null)
        ''' 
        statusDesc = str(statusDesc).strip()

        try:
            statusDesc = int(statusDesc)
            return [int(1), None]
        except:
            pass

        try:
            if(startup.math.isnan(float(statusDesc))):
                return [int(1), None]
        except:
            pass

        try:
            if(int(len(str(statusDesc))) == 0):
                return [int(1), None]
        except:
            pass

        try:
            statusDesc = str(statusDesc)
            return [int(0), str(statusDesc)]
        except:
            return [int(1), None]

    def getStatusDesc(self):
        return self.statusDesc

    def crmCd1Constructor(self,crmCd1):
        ''' 
        Crm Cd 1 
            |-> CSV type: text 
            |-> Description: Indicates the crime committed. Crime Code 1 is the primary and most serious one. 
                Crime Code 2, 3, and 4 are respectively less serious offenses. Lower crime class numbers are more serious.
            |-> Can be null: not
            |-> Example: 900
            |-> Add constrains: make sure the number is in a valid range and that it isn't null
        ''' 

        crmCd1 = str(crmCd1).strip()
        try:
            if(startup.math.isnan(float(crmCd1))):
                return [int(1), None]
        except:
            pass
        
        try:
            crmCd1 = int(startup.math.trunc(float(crmCd1)))
        except:
            return [int(1), None]

        try:
            crmCd1 = int(crmCd1)
            return [int(0), int(crmCd1)]
        except:
            return [int(1), None]

    def getCrmCd1(self):
        return self.crmCd1

    def crmCd2Constructor(self,crmCd2):
        ''' 
        Crm Cd 2 
            |-> CSV type: text 
            |-> Description: May contain a code for an additional crime, less serious than Crime Code 1.
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: check it is null, if not make sure the number is in valid range
        ''' 
        crmCd2 = str(crmCd2).strip()
        try:
            if(startup.math.isnan(float(crmCd2))):
                return [int(0), None]
        except:
            pass
        
        try:
            crmCd2 = int(startup.math.trunc(float(crmCd2)))
        except:
            return [int(1), None]

        try:
            crmCd2 = int(crmCd2)
            return [int(0), int(crmCd2)]
        except:
            return [int(1), None]

    def getCrmCd2(self):
        return self.crmCd2

    def crmCd3Constructor(self,crmCd3):
        ''' 
        Crm Cd 3 
            |-> CSV type: text 
            |-> Description: May contain a code for an additional crime, less serious than Crime Code 1.
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: check it is null, if not make sure the number is in valid range
        ''' 
        crmCd3 = str(crmCd3).strip()
        try:
            if(startup.math.isnan(float(crmCd3))):
                return [int(0), None]
        except:
            pass
        
        try:
            crmCd3 = int(startup.math.trunc(float(crmCd3)))
        except:
            return [int(1), None]

        try:
            crmCd3 = int(crmCd3)
            return [int(0), int(crmCd3)]
        except:
            return [int(1), None]

    def getCrmCd3(self):
        return self.crmCd3

    def crmCd4Constructor(self,crmCd4):
        ''' 
        Crm Cd 4 
            |-> CSV type: text 
            |-> Description: May contain a code for an additional crime, less serious than Crime Code 1.
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: check it is null, if not make sure the number is in valid range
        ''' 
        crmCd4 = str(crmCd4).strip()
        try:
            if(startup.math.isnan(float(crmCd4))):
                return [int(0), None]
        except:
            pass
        
        try:
            crmCd4 = int(startup.math.trunc(float(crmCd4)))
        except:
            return [int(1), None]

        try:
            crmCd4 = int(crmCd4)
            return [int(0), int(crmCd4)]
        except:
            return [int(1), None]

    def getCrmCd4(self):
        return self.crmCd4

    def locationConstructor(self,location):
        ''' 
        LOCATION 
            |-> CSV type: text 
            |-> Description: Street address of crime incident rounded to the nearest hundred block to maintain anonymity.
            |-> Can be null: not
            |-> Example: 300 E GAGE AV
            |-> Add constrains: Make sure it is not null or less than 5 characters
        ''' 
        try:
            location = int(location)
            return [int(1), None]
        except:
            pass

        location = str(location).strip()
        try:
            if(startup.math.isnan(float(location))):
                return [int(1), None]
        except:
            pass

        location = ' '.join(location.split())
        try:
            if(len(str(location)) != int(0)):
                return [int(0), str(location)]
            else:
                return [int(1), None]
        except:
            pass

    def getLocation(self):
        return self.location

    def crossStreetConstructor(self,crossStreet):
        ''' 
        Cross Street 
            |-> CSV type: text 
            |-> Description: Cross Street of rounded Address
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: it can be null
        ''' 
        
        try:
            crossStreet = int(crossStreet)
            return [int(1), None]
        except:
            pass

        crossStreet = str(crossStreet).strip()
        try:
            if(startup.math.isnan(float(crossStreet))):
                return [int(0), None]
        except:
            pass

        crossStreet = ' '.join(crossStreet.split())
        try:
            if(len(str(crossStreet)) != int(0)):
                return [int(0), str(crossStreet)]
            else:
                return [int(0), None]
        except:
            pass

    def getCrossStreet(self):
        return self.crossStreet

    def latConstructor(self,lat):
        ''' 
        LAT 
            |-> CSV type: number 
            |-> Description: Latitude
            |-> Can be null: not
            |-> Example: 33.9825
            |-> Add constrains: make sure it is not null and it starts with 33
        ''' 
        try:
            lat = float(lat)
        except:
            return ([int(1), None])

        try:
            if(startup.math.isnan(float(lat))):
                return ([int(1), None])
        except:
            pass
        
        try:
            if((int((str(lat))[0]) == 3) and 
                (0 <= int((str(lat))[1]) <= 9)):
                return [int(0), float(lat)]
            else:
                return ([int(1), None])
        except:
            return ([int(1), None])

    def getLat(self):
        return self.locLat

    def lonConstructor(self,lon):
        ''' 
        LON 
            |-> CSV type: number 
            |-> Description: Longitude
            |-> Can be null: not
            |-> Example: -118.2695
            |-> Add constrains: make sure it is not null and it starts with -118
        '''
        try:
            lon = float(lon)
        except:
            return ([int(1), None])

        try:
            if(startup.math.isnan(float(lon))):
                return ([int(1), None])
        except:
            pass
        
        try:
            if(((str(lon)[0]) == "-") and 
                (int((str(lon))[1]) == 1) and
                (int((str(lon))[2]) == 1) and
                (0 <= int((str(lon))[3]) <= 9)):
                return [int(0), float(lon)]
            else:
                return ([int(1), None])
        except:
            return ([int(1), None])

    def getLon(self):
        return self.locLon

    def missingData(self):
        print(self.originalData)

    def fixAnomalies():
        pass

    def removeDuplicates():
        pass

    def myfunc(self):
        pass
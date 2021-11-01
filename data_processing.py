import sys
try:
    import startup as startup
except Exception as e:
    print("startup.py not found. Stopping the code, please add it to the directory")
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

    def builder(self):
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

        print(arr)
        count = 0
        for item in arr:
            errorCount = 0
            if((self.drNoConstructor(item[0])) == (int(0))):
                pass
            else:
                errorCount += 1

            if(errorCount > 0):
                arr = startup.np.delete(arr,count,0)
                
            count += 1
        
        print("============")
        print(arr)
        
        '''
            print(x[1])
            print(x[2])
            print(x[3])
            print(x[4])
            print(x[5])
            print(x[6])
            print(x[7])
            print(x[8])
            print(x[9])
            print(x[10])
            print(x[11])
            print(x[12])
            print(x[13])
            print(x[14])
            print(x[15])
            print(x[16])
            print(x[17])
            print(x[18])
            print(x[19])
            print(x[20])
            print(x[21])
            print(x[22])
            print(x[23])
            print(x[24])
            print(x[25])
            print(x[26])
            print(x[27])
        '''    
        
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
            return (int(1))

        if (drNo > int(0)):
            return (int(0))
        else:
            return (int(1))

        #print("DR NO")
        #print(self.getDrNo())
        #print(type(self.getDrNoConstructor()))
        #print(self.contains_duplicates(self.getDrNoConstructor()))
        #print(startup.np.isnan(self.getDrNoConstructor()).sum())
    
    def getDrNo(self):
        return self.drNo

    def dateRptdConstructor(self):
        '''      
        Date Rptd 
            |-> CSV type: MM/DD/YYYY 
            |-> Description: Date of crime reported
            |-> Can be null: not
            |-> Example: 02/20/2010
            |-> Add constrains: make sure it is a valid date (not maybe not in the future)           
        '''
        print("DateRptd")
        print(self.getDateRptd())

    def getDateRptd(self):
        return self.dateRptd

    def dateOccConstructor(self):
        '''
        DATE OCC 
            |-> CSV type: MM/DD/YYYY 
            |-> Description: Date when crime occurred
            |-> Can be null: not
            |-> Example: 02/20/2010
            |-> Add constrains: make sure it is a valid date (not maybe not in the future)  

        '''
        print("OccConstructor")
        #startup.np.set_printoptions(threshold=startup.sys.maxsize)
        print(self.getDateOcc())

    def getDateOcc(self):
        return self.dateOcc

    def timeOccConstructor(self):
        ''' 
        TIME OCC 
            |-> CSV type: text 
            |-> Description: Date when crime occurred
            |-> Can be null: not
            |-> Example: 1350
            |-> Add constrains: make sure it is a number between 0000 and 2400
        ''' 
        print("TimeOccConstructor")
        print(self.getTimeOcc())

    def getTimeOcc(self):
        return self.timeOcc

    def areaConstructor(self):
        ''' 
        AREA 
            |-> CSV type: text 
            |-> Description: The LAPD has 21 Community Police Stations referred to as Geographic Areas within the department. 
                These Geographic Areas are sequentially numbered from 1-21.
            |-> Can be null: not
            |-> Example: 13
            |-> Add constrains: make sure the numbers are in the range of 1-21
        ''' 
        print("Area")
        print(self.getArea())

    def getArea(self):
        return self.area

    def areaNameConstructor(self):
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
        print("AreaName")
        print(self.getAreaName())

    def getAreaName(self):
        return self.areaName

    def rptDistNoConstructor(self):
        ''' 
        Rpt Dist No 
            |-> CSV type: text 
            |-> Description: A four-digit code that represents a sub-area within a Geographic Area. All crime records reference 
                the "RD" that it occurred in for statistical comparisons. Find LAPD Reporting Districts on the LA City GeoHub.
            |-> Can be null: not
            |-> Example: 1385
            |-> Add constrains: make sure it is a positive number and a number from a list https://data.lacounty.gov/GIS-Data/Reporting-Districts/kvwy-dqs6
        ''' 
        print("RptDistNo")
        print(self.getRptDistNo())
   
    def getRptDistNo(self):
        return self.rptDistNo

    def part1or2Constructor(self):
        ''' 
        Part 1-2 
            |-> CSV type: number 
            |-> Description: what type of offense is it (part 1 or part 2)
            |-> Can be null: not
            |-> Example: 2
            |-> Add constrains: make sure it is either 1 or 2
        ''' 
        print("Part1or2")
        print(self.getPart1or2())
    
    def getPart1or2(self):
        return self.part1or2

    def crmCdConstructor(self):
        ''' 
        Crm Cd 
            |-> CSV type: text 
            |-> Description: Indicates the crime committed. (Same as Crime Code 1)
            |-> Can be null: not
            |-> Example: 900
            |-> Add constrains: make sure it is a positive number (cannot verify from source)
        ''' 
        print("CrmCd")
        print(self.getCrmCd())

    def getCrmCd(self):
        return self.crmCd

    def crmCdDescConstructor(self):
        ''' 
        Crm Cd Desc 
            |-> CSV type: text 
            |-> Description: Defines the Crime Code provided.
            |-> Can be null: not
            |-> Example: VIOLATION OF COURT ORDER
            |-> Add constrains: make sure it is not null (text)
        ''' 
        print("CrmCdDesc")
        print(self.getCrmCdDesc())

    def getCrmCdDesc(self):
        return self.crmCdDesc

    def mocodesConstructor(self):
        ''' 
        Mocodes 
            |-> CSV type: text 
            |-> Description: Modus Operandi: Activities associated with the suspect in commission of the crime. 
                See attached PDF for list of MO Codes in numerical order.
            |-> Can be null: not
            |-> Example: 0913 1814 2000
            |-> Add constrains: make sure the number is from the list, and then match it up (0913 to str + 1814 to str + 2000 to str)
        ''' 
        print("Mocodes")
        print(self.getMocodes())

    def getMocodes(self):
        return self.mocodes

    def victAgeConstructor(self):
        ''' 
        Vict Age 
            |-> CSV type: text 
            |-> Description: Age of the victim
            |-> Can be null: not
            |-> Example: 48
            |-> Add constrains: make sure the age is at least 10 years or over
        ''' 
        print("VictAge")
        print(self.getVictAge())

    def getVictAge(self):
        return self.victAge

    def victSexConstructor(self):
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
        print("VictSex")
        print(self.getVictSex())

    def getVictSex(self):
        return self.victSex

    def victDescentConstructor(self):
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
        print("VictDescent")
        print(self.getVictDescent())

    def getVictDescent(self):
        return self.victDescent

    def premisCdConstructor(self):
        ''' 
        Premis Cd 
            |-> CSV type: text 
            |-> Description: The type of structure, vehicle, or location where the crime took place.
            |-> Can be null: not
            |-> Example: 501
            |-> Add constrains: make sure it is a valid number (positive), cannot find a source
        ''' 
        print("premisCd")
        print(self.getPremisCd())

    def getPremisCd(self):
        return self.premisCd

    def premisDescConstructor(self):
        ''' 
        Premis Desc 
            |-> CSV type: text 
            |-> Description: Defines the Premise Code provided.
            |-> Can be null: not
            |-> Example: SINGLE FAMILY DWELLING
            |-> Add constrains: make sure string is valid (not null)
        ''' 
        print("PremisDesc")
        print(self.getPremisDesc())

    def getPremisDesc(self):
        return self.premisDesc

    def weaponUsedCdConstructor(self):
        ''' 
        Weapon Used Cd 
            |-> CSV type: text 
            |-> Description: The type of weapon used in the crime.
            |-> Can be null: yes
            |-> Example: " " or 102
            |-> Add constrains: if it is null (empty) replace it with 0 and say "none", otherwise make sure number is valid
        ''' 
        print("WeaponUsedCd")
        print(self.getWeaponUsedCd())

    def getWeaponUsedCd(self):
        return self.weaponUsedCd

    def weaponDescConstructor(self):
        ''' 
        Weapon Desc 
            |-> CSV type: text 
            |-> Description: Defines the Weapon Used Code provided.
            |-> Can be null: yes
            |-> Example: HAND GUN
            |-> Add constrains: make sure string is valid (not null)
        ''' 
        print("WeaponDesc")
        print(self.getWeaponDesc())

    def getWeaponDesc(self):
        return self.weaponDesc

    def statusConstructor(self):
        ''' 
        Status 
            |-> CSV type: text 
            |-> Description: Status of the case. (IC is the default)
            |-> Can be null: not
            |-> Example: AA
            |-> Add constrains: make sure string is valid (not null)
        ''' 
        print("Status")
        print(self.getStatus())

    def getStatus(self):
        return self.status

    def statusDescConstructor(self):
        ''' 
        Status Desc 
            |-> CSV type: text 
            |-> Description: Defines the Status Code provided
            |-> Can be null: not
            |-> Example: Adult Arrest
            |-> Add constrains: make sure string is valid (not null)
        ''' 
        print("StatusDesc")
        print(self.getStatusDesc())

    def getStatusDesc(self):
        return self.statusDesc

    def crmCd1Constructor(self):
        ''' 
        Crm Cd 1 
            |-> CSV type: text 
            |-> Description: Indicates the crime committed. Crime Code 1 is the primary and most serious one. 
                Crime Code 2, 3, and 4 are respectively less serious offenses. Lower crime class numbers are more serious.
            |-> Can be null: not
            |-> Example: 900
            |-> Add constrains: make sure the number is in a valid range and that it isn't null
        ''' 
        print("CrmCd1")
        print(self.getCrmCd1())

    def getCrmCd1(self):
        return self.crmCd1

    def crmCd2Constructor(self):
        ''' 
        Crm Cd 2 
            |-> CSV type: text 
            |-> Description: May contain a code for an additional crime, less serious than Crime Code 1.
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: check it is null, if not make sure the number is in valid range
        ''' 
        print("CrmCd2")
        print(self.getCrmCd2())

    def getCrmCd2(self):
        return self.crmCd2

    def crmCd3Constructor(self):
        ''' 
        Crm Cd 3 
            |-> CSV type: text 
            |-> Description: May contain a code for an additional crime, less serious than Crime Code 1.
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: check it is null, if not make sure the number is in valid range
        ''' 
        print("CrmCd3")
        print(self.getCrmCd3())

    def getCrmCd3(self):
        return self.crmCd3

    def crmCd4Constructor(self):
        ''' 
        Crm Cd 4 
            |-> CSV type: text 
            |-> Description: May contain a code for an additional crime, less serious than Crime Code 1.
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: check it is null, if not make sure the number is in valid range
        ''' 
        print("CrmCd4")
        print(self.getCrmCd4())

    def getCrmCd4(self):
        return self.crmCd4

    def locationConstructor(self):
        ''' 
        LOCATION 
            |-> CSV type: text 
            |-> Description: Street address of crime incident rounded to the nearest hundred block to maintain anonymity.
            |-> Can be null: not
            |-> Example: 300 E GAGE AV
            |-> Add constrains: Make sure it is not null or less than 5 characters
        ''' 
        print("Location")
        print(self.getLocation())

    def getLocation(self):
        return self.location

    def crossStreetConstructor(self):
        ''' 
        Cross Street 
            |-> CSV type: text 
            |-> Description: Cross Street of rounded Address
            |-> Can be null: yes
            |-> Example:
            |-> Add constrains: it can be null
        ''' 
        print("CrossStreet")
        print(self.getCrossStreet())

    def getCrossStreet(self):
        return self.crossStreet

    def latConstructor(self):
        ''' 
        LAT 
            |-> CSV type: number 
            |-> Description: Latitude
            |-> Can be null: not
            |-> Example: 33.9825
            |-> Add constrains: make sure it is not null and it starts with 33
        ''' 
        print("Lat")
        print(self.getLat())

    def getLat(self):
        return self.locLat

    def lonConstructor(self):
        ''' 
        LON 
            |-> CSV type: number 
            |-> Description: Longitude
            |-> Can be null: not
            |-> Example: -118.2695
            |-> Add constrains: make sure it is not null and it starts with -118
        '''
        print("Lon")
        print(self.getLon())

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
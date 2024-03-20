import mysql.connector as mysql
from PyQt5.QtGui import QPixmap
from unidecode import unidecode

class Database:
    def __init__(self):
        self.connection = mysql.connect(host='localhost', user='root', password='12345678', database='f1')


    def getTracks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tbltrack")
        return cursor.fetchall()
    
    def addRace(self, name, date, trackID, round):
        cursor = self.connection.cursor()
        sql = """
                    call spVoegRaceToe(%s, %s, %s, %s, %s)
                """
        cursor.execute(sql, (trackID, date[:4], date, round, name))
        self.connection.commit()
        cursor.close

    def getDriverPhoto(self, driverName):
        cursor = self.connection.cursor()
        cursor.callproc("spGetDriverFoto", [driverName, ])
        for result in cursor.stored_results():
            data = result.fetchall()
        pixmap = QPixmap()
        pixmap.loadFromData(data[0][0])
        return pixmap
    
    def getCountryFlag(self, driverName):
        cursor = self.connection.cursor()
        cursor.callproc("spGetVlag", [driverName, ])
        for result in cursor.stored_results():
            data = result.fetchall()
        pixmap = QPixmap()
        pixmap.loadFromData(data[0][0])
        return pixmap

    # def updateDriverPhoto(self, driverID, filePath):
    #     cursor = self.connection.cursor()
    #     with open(filePath, 'rb') as file:
    #         blobData = file.read()
    #     sql = "UPDATE tblcoureur SET blFoto = %s WHERE IDCoureur = %s"
    #     cursor.execute(sql, (blobData, driverID))
    #     self.connection.commit()
    #     # cursor.close()

    
    def updateDriverBLOBS(self):
        # name = "Lewis Hamilton"
        # path = f"fotos/Coureurs/{name}.jpg"

        cursor = self.connection.cursor()
        sql = "SELECT strNaam from tblcoureur"
        cursor.execute(sql)
        drivers = cursor.fetchall()
        for driver in drivers:
            driverName = unidecode(driver[0].strip())
            path = f"fotos/Coureurs/{driverName}.jpg"
            with open(path, 'rb') as file:
                blobData = file.read()
            sql = "UPDATE tblcoureur SET blFoto = %s WHERE strNaam = %s"
            test = "blobData"
            cursor.execute(sql, (blobData, driverName))
            self.connection.commit()

    def updateCountryFlagsBLOB(self):
        cursor = self.connection.cursor()
        sql = "SELECT strLand from tblland"
        cursor.execute(sql)
        countries = cursor.fetchall()
        for country in countries:
            countryName = unidecode(country[0].strip())
            path = f"fotos/Landen/{countryName}.png"
            with open(path, 'rb') as file:
                blobData = file.read()
            sql = "UPDATE tblland SET blFoto = %s WHERE strLand = %s"
            cursor.execute(sql, (blobData, countryName))
        self.connection.commit()
    
    def getDriverID(self, driverName):
        cursor = self.connection.cursor()
        cursor.callproc("spGetDriverID", [driverName, ])
        for result in cursor.stored_results():
            return result.fetchall()
    
    def getDrivers(self, year):
        cursor = self.connection.cursor()
        cursor.callproc("spGetCoureurJaar", [year, ])
        for result in cursor.stored_results():
            return result.fetchall()
    
    def getTeams(self, year):
        cursor = self.connection.cursor()
        cursor.callproc("spGetTeamJaar", [year, ])
        for result in cursor.stored_results():
            return result.fetchall()
    
    def getDriversFromTeam(self, teamName, year):
        cursor = self.connection.cursor()
        cursor.callproc("spGetTeamData", [teamName, year])
        for result in cursor.stored_results():
            return result.fetchall()
    
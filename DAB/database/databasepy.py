import mysql.connector as mysql
from PyQt5.QtGui import QPixmap
from unidecode import unidecode
from PyQt5.QtWidgets import QMessageBox

class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connect(host=host, user=user, password=password, database=database)



    def isAdmin(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT USER();")
        data = cursor.fetchall()
        if data[0][0] == "root@localhost":
            return True
        elif data[0][0] == "admin@localhost":
            return True
        else:
            return False

    def sp(self, storedProcedure, argList):
        try:
            cursor = self.connection.cursor()
            cursor.callproc(storedProcedure, argList)
            for result in cursor.stored_results():
                return result.fetchall()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()
        cursor.close

    def sql(self, sql, argList):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, argList)
            return cursor.fetchall()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()
        cursor.close

    def getLogs(self):
        rows = self.sql("SELECT * FROM tbllogdata ORDER BY dtTimeStamp DESC", [])
        return rows
        # return self.sql("SELECT * FROM tbllogdata ORDER BY dtTimeStamp DESC", [])

    def getTracks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tbltrack ORDER BY strNaam ASC")
        return cursor.fetchall()
    
    def addRace(self, name, year, trackID, round, date, laps):
        cursor = self.connection.cursor()
        sql = """
                    call spVoegRaceToe(%s, %s, %s, %s, %s, %s)
                """
        try:
            cursor.execute(sql, (trackID, year, date, round, laps, name))
            self.connection.commit()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()
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
    
    def updateTrackBLOB(self):
        cursor = self.connection.cursor()
        sql = "SELECT strNaam from tbltrack"
        cursor.execute(sql)
        countries = cursor.fetchall()
        for country in countries:
            countryName = (country[0].strip())
            path = f"fotos/Circuits/{countryName}.png"
            try:
                with open(path, 'rb') as file:
                    blobData = file.read()
            except:
                path = f"fotos/Circuits/Geen foto.png"
                with open(path, 'rb') as file:
                    blobData = file.read()
            sql = "UPDATE tbltrack SET blFoto = %s WHERE strNaam = %s"
            cursor.execute(sql, (blobData, countryName))
        self.connection.commit()


    def getDriverID(self, driverName):
        # cursor = self.connection.cursor()
        # cursor.callproc("spGetCoureurID", [driverName, ])
        # for result in cursor.stored_results():
        #     return result.fetchall()
        return self.sp("spGetCoureurID", [driverName, ])
        
    def getRaceID(self, raceName, year):
        # cursor = self.connection.cursor()
        # cursor.callproc("spGetRaceID", [raceName, year])
        # for result in cursor.stored_results():
        #     return result.fetchall()
        return self.sp("spGetRaceID", [raceName, year])

    def getTrackID(self, trackName):
        # cursor = self.connection.cursor()
        # cursor.callproc("spGetTrackID", [trackName, ])
        # for result in cursor.stored_results():
        #     return result.fetchall()
        return self.sp("spGetTrackID", [trackName, ])

    def getDrivers(self, year):
        # cursor = self.connection.cursor()
        # cursor.callproc("spGetCoureurJaar", [year, ])
        # for result in cursor.stored_results():
        #     return result.fetchall()
        return self.sp("spGetCoureurJaar", [year, ])

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
    
    def getRaceInfo(self, year):
        cursor = self.connection.cursor()
        sql = "SELECT intronde, racenaam, tracknaam, intlengte, intbochten, intlaps, strStad, dtdatum, blfoto FROM raceinfo WHERE intSeizoen = %s AND raceNaam LIKE '%%Grand Prix'"
        cursor.execute(sql, (year, ))
        return cursor.fetchall()
    
    def getDriverInfo(self, driverName, year):
        cursor = self.connection.cursor()
        cursor.callproc("spGetCoureurData", [driverName, year,])
        for result in cursor.stored_results():
            return result.fetchall()
        
    def addRaceResult(self, raceID, driverID, position, pole, points):
        cursor = self.connection.cursor()

        print(raceID, driverID, position, pole, points)
        cursor.callproc("spVoegResultaatToe", (raceID, driverID, position, pole, points))
        self.connection.commit()
        cursor.close

    def editRaceResult(self, raceID, driverID, position, pole, points):
        cursor = self.connection.cursor()
        cursor.callproc("spUpdateResultaat", (raceID, driverID, position, pole, points))
        self.connection.commit()
        cursor.close

    def deleteRaceResult(self, raceID, driverID):
        cursor = self.connection.cursor()
        cursor.callproc("spVerwijderResultaat", (raceID, driverID))
        self.connection.commit()
        cursor.close


    def getRaceNames(self, year):
        cursor = self.connection.cursor()
        cursor.callproc("spGetRaceJaar", [year, ])
        for result in cursor.stored_results():
            return result.fetchall()
        
    def getStandings(self, year):
        cursor = self.connection.cursor()
        cursor.callproc("spGetStandings", [year, ])
        for result in cursor.stored_results():
            return result.fetchall()
        
    def getWins(self, driverName, year):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT GetTotalWins('{driverName}', '{year}');")
        return cursor.fetchall()
    
    def getPoints(self, driverName, year):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT GetTotalPoints('{driverName}', '{year}');")
        return cursor.fetchall()
    
    def getPoles(self, driverName, year):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT GetTotalPolPos('{driverName}', '{year}');")
        return cursor.fetchall()
import mysql.connector as mysql

class Database:
    def __init__(self):
        self.connection = mysql.connect(host='localhost', user='root', password='12345678', database='formule1')


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
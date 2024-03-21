from PyQt5.QtWidgets import QMainWindow, QAction, QGridLayout, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem, QMessageBox, QTableView
from PyQt5.uic import loadUi
from PyQt5.QtGui import QKeySequence, QPixmap, QFont, QColor, QPainter, QBrush, QStandardItem, QStandardItemModel
from DAB.gui.menu import menu
from DAB.database.databasepy import Database
from PyQt5.QtCore import Qt, QStringListModel

class MainWindow(QMainWindow):
    
    """
    Main window for the application.

    This class represents the main window of your application.
    It contains methods for initializing the UI.
    """
    
    def __init__(self):
        """
        Initialize the main window.
        """
        super().__init__()
        loadUi("dab2.ui", self)#Load Ui from the Qt Designer


        try:
            self.database = Database(self.leHost.text(), self.leUser.text(), self.lePassword.text(), self.leDatabase.text())
            self.changeAdminValues(self.database.isAdmin())
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()
            self.database = None

        self.defineActions()
        self.tracks = None

        self.btnAddRace.clicked.connect(self.addRace)

        

        self.dateEdit.dateChanged.connect(self.fillDriverCombobox)
        self.dateEdit.dateChanged.connect(self.StandingsView)
        self.comboDriver.currentIndexChanged.connect(self.updateDriverView)
        self.comboTeams.currentIndexChanged.connect(self.displayTeamInfo)
        self.intSeizoen.dateChanged.connect(self.fillComboEditors)
        self.btnAddResult.clicked.connect(lambda: self.RaceResult("add"))
        self.btnAlterResult.clicked.connect(lambda: self.RaceResult("edit"))
        self.btnDeleteResult.clicked.connect(lambda: self.RaceResult("delete"))
        self.tabWidget.currentChanged.connect(self.updateViews)
        self.btnLogin.clicked.connect(self.login)
        self.btnFixImg.clicked.connect(self.fixImg)
        self.btnLogs.clicked.connect(self.updateLogs)
        self.loadTracks()
        self.fillDriverCombobox()
        self.fillTeamsCombobox()
        self.raceListView()
        self.fillComboEditors()
        self.StandingsView()
        self.changeAdminValues(False)

    def updateLogs(self):
        logs = self.database.getLogs()
        model = QStandardItemModel()

        for log in logs:
            items = [QStandardItem(str(item)) for item in log]
            model.appendRow(items)

        column_names = ["ID", "IDResultaat", "intPositie", "strCoureur", "strRace", "dtTimeStamp", "strCurrentUser", "strTypeChange"]  # replace with actual column names
        model.setHorizontalHeaderLabels(column_names)

        self.adminLog.setModel(model)
        self.adminLog.resizeColumnsToContents()

    def changeAdminValues(self, isAdmin):
        self.btnFixImg.setEnabled(isAdmin)
        self.btnAddRace.setEnabled(isAdmin)
        self.btnAddResult.setEnabled(isAdmin)
        self.btnAlterResult.setEnabled(isAdmin)
        self.btnDeleteResult.setEnabled(isAdmin)
        self.btnLogs.setEnabled(isAdmin)

    def login(self):
        self.database = None
        try:
            self.database = Database(self.leHost.text(), self.leUser.text(), self.lePassword.text(), self.leDatabase.text())
            self.changeAdminValues(self.database.isAdmin())
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()
            self.database = None
            return

        self.loadTracks()
        self.fillDriverCombobox()
        self.fillTeamsCombobox()
        self.raceListView()
        self.fillComboEditors()
        self.StandingsView()

    def fixImg(self):
        self.database.updateDriverBLOBS()
        self.database.updateCountryFlagsBLOB()
        self.database.updateTrackBLOB()

    def fillDriverCombobox(self):
        if self.database is None:
            return
        self.comboDriver.clear()
        drivers = self.database.getDrivers(self.dateEdit.date().year())
        for driver in drivers:
            self.comboDriver.addItem(driver[0])
        self.updateDriverView()
        
    def fillTeamsCombobox(self):
        if self.database is None:
            return
        self.comboTeams.clear()
        teams = self.database.getTeams(self.dateEdit.date().year())
        for team in teams:
            self.comboTeams.addItem(team[0])
        self.displayTeamInfo()

    def updateViews(self):
        index = self.tabWidget.currentIndex()
        if index == 0:
            self.raceListView()
        elif index == 1:
            self.StandingsView()
        elif index == 2:
            self.updateDriverView()
        elif index == 3:
            self.displayTeamInfo()

    def updateDriverView(self):
        driverName = self.comboDriver.currentText()
        if driverName == "":
            return
        season = self.dateEdit.date().year()
        driverInfo = self.database.getDriverInfo(driverName, season)
        # pixmap = self.database.getDriverPhoto(driverName)
        # pixmap = pixmap.scaled(300, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.driverPhoto.setPixmap(pixmap)
        driverPhoto = self.database.getDriverPhoto(driverName)
        self.driverPhoto.setFixedSize(210, 400)
        radius = 30
        # create empty pixmap of same size as original 
        rounded = QPixmap(driverPhoto.size())
        rounded.fill(QColor("transparent"))

        # draw rounded rect on new pixmap using original pixmap as brush
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(driverPhoto))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(driverPhoto.rect(), radius, radius)
        painter.end()
        # set pixmap of label
        self.driverPhoto.setPixmap(rounded.scaled(210, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))


        pixmap = self.database.getCountryFlag(driverName)
        pixmap = pixmap.scaled(50, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.countryPhoto.setPixmap(pixmap)


        self.lblDriverName.setText(driverName)
        self.lblRaceNumber.setText("Number: " + str(driverInfo[0][3]))
        self.lblNationality.setText(driverInfo[0][1])
        self.lblTeam.setText("Drivers for: " + driverInfo[0][2])
        self.lblPoints.setText("Points: " + str(self.database.getPoints(driverName, season)[0][0]))
        self.lblWins.setText("Wins: " + str(self.database.getWins(driverName, season)[0][0]))
        self.lblPoles.setText("Poles: " + str(self.database.getPoles(driverName, season)[0][0]))
        
    def loadTracks(self):
        if self.database is None:
            return
        self.tracks = self.database.getTracks()
        for track in self.tracks:
            self.comboTrackNames.addItem(track[2])

    def addRace(self):
        name = self.leRaceName.text()
        year = self.deRaceDate.date().year()
        date = self.deRaceDate.date().toString("yyyy-MM-dd")
        track = self.comboTrackNames.currentText()
        laps = self.spbLaps.value()
        track_id = self.database.getTrackID(track)[0][0]
        round = self.spbRaceRound.value()

        self.database.addRace(name, year, track_id, round, date, laps)

    def RaceResult(self, status):
        race = self.comboRacelist.currentText()
        driver = self.comboDriverList.currentText()
        position = self.spbPosition.value()
        points = self.spbPoints.value()
        if self.checkPole.isChecked():
            pole = 1
        else:
            pole = 0
        year = self.intSeizoen.date().year()
        raceID = self.database.getRaceID(race, year)[0][0]
        driverID = self.database.getDriverID(driver)[0][0]
        # print(raceID, driverID, position, points, pole)
        if status == "add":
            self.database.addRaceResult(raceID, driverID, position, pole, points)
        elif status == "edit":
            self.database.editRaceResult(raceID, driverID, position, pole, points)
        elif status == "delete":
            self.database.deleteRaceResult(raceID, driverID)

    def fullscreen(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showNormal()

    def defineActions(self):
        self.loadConfigAct = QAction("Load config", self)
        # self.loadConfigAct.triggered.connect(self.connectedWindow.loadConfig)

        self.saveConfigAct = QAction("Save config", self)
        # self.saveConfigAct.triggered.connect(self.connectedWindow.saveConfig)
        # self.saveConfigAct.setShortcut(QKeySequence.Save)

    def displayTeamInfo(self):

        self.clearFrameTeamConfig(self.LayoutTeamConfig.layout())
        self.lblTeamName.setText(self.comboTeams.currentText())
        drivers = self.database.getDriversFromTeam(self.comboTeams.currentText(), self.dateEdit.date().year())
        # Drivername, image and country flag
        f = QFont("Orbitron")
        f.setPointSize(20)
        
        for driver in drivers:
            frame = QFrame()
            frame.setStyleSheet("""
                                QFrame{
                                    background-color: #283344;
                                    /*border: 2px solid gray;*/
                                    border-radius: 20px;
                                }
                                """)
            frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout = QHBoxLayout()
            layoutInfo = QVBoxLayout()
            driverName = QLabel(driver[0])
            driverName.setFont(f)
            driverName.setStyleSheet("color: white")

            # driverID = self.database.getDriverID(driver[0])
            driverPhoto = self.database.getDriverPhoto(driver[0])
            lblDriverPhoto = QLabel()
            lblDriverPhoto.setFixedSize(210, 400)
            radius = 30
            # create empty pixmap of same size as original 
            rounded = QPixmap(driverPhoto.size())
            rounded.fill(QColor("transparent"))

            # draw rounded rect on new pixmap using original pixmap as brush
            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(driverPhoto))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(driverPhoto.rect(), radius, radius)
            painter.end()
            # set pixmap of label
            lblDriverPhoto.setPixmap(rounded.scaled(210, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))


            countryFlag = self.database.getCountryFlag(driver[0])
            lblCountryFlag = QLabel()
            lblCountryFlag.setMinimumHeight(100)
            lblCountryFlag.setMinimumWidth(100)
            lblCountryFlag.setPixmap(countryFlag.scaled(50, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layoutInfo.addWidget(driverName)
            layoutInfo.addWidget(lblCountryFlag)
            spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            layout.addLayout(layoutInfo, 1)
            layout.addWidget(lblDriverPhoto, 2)
            layout.addItem(spacer)
            frame.setLayout(layout)
            self.LayoutTeamConfig.addWidget(frame)

    def clearFrameTeamConfig(self, layout):
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget() is not None:
                        child.widget().deleteLater()

    def raceListView(self):
        if self.database is None:
            return
        self.clearFrameTeamConfig(self.LayoutRaceList)
        raceData = self.database.getRaceInfo(self.dateEdit.date().year())
        
        for race in raceData:
            self.raceItem(race[1], race[6], race[2], race[3], race[5], race[0], race[7], race[8], race[4])

    def raceItem(self, raceName, location, track, trackLength, laps, round, date, foto, corners):
        f = QFont("Orbitron")
        f.setPointSize(14)
        fbold = QFont("Orbitron")
        fbold.setBold(True)
        frame = QFrame()
        frame.setStyleSheet("""
                            QFrame{
                                background-color: #f7faff;
                                border: 1px solid #dbdbdb;
                                border-radius: 20px;
                            }
                            QLabel{
                                border:none;
                            }

                            """)
        frame.setFixedSize(460,200)
        
        pixmap = QPixmap()
        pixmap.loadFromData(foto)
        racePhoto = QLabel()
        racePhoto.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))


        frameInfo = QFrame()
        frameInfo.setStyleSheet("""
                                border:none;

                                """)
        frameLayout = QHBoxLayout()

        lblRaceName = QLabel(raceName)
        lblRaceName.setFont(fbold)
        lblLocation = QLabel(location)
        lblLocation.setFont(fbold)
        lblTrack = QLabel(track)
        lblTrack.setFont(f)
        lblTrackLength = QLabel(str(trackLength) + "m")
        lblTrackLength.setFont(f)
        lblLaps = QLabel(str(laps) + " Laps")
        lblLaps.setFont(f)
        lblRound = QLabel("R" + str(round))
        lblRound.setFont(f)
        lblDate = QLabel(str(date))
        lblDate.setFont(f)
        lblCorners = QLabel(str(corners) + " Corners")
        lblCorners.setFont(f)

        layout1 = QHBoxLayout()
        layout1.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout2 = QVBoxLayout()
        layout2.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout3 = QHBoxLayout()
        layout3.setContentsMargins(0, 0, 0, 0)  # Remove margins

        layoutInfo = QVBoxLayout()
        layoutInfo.setContentsMargins(0, 0, 0, 0)  # Remove margins

        layout1.addWidget(lblLocation)
        layout1.addWidget(QVLine())
        layout1.addWidget(lblRaceName)
        layout2.addWidget(lblTrack)
        layout2.addWidget(lblTrackLength)
        layout2.addWidget(lblLaps)
        layout2.addWidget(lblCorners)
        layout3.addWidget(lblRound)
        layout3.addWidget(QVLine())
        layout3.addWidget(lblDate)

        layoutInfo.addLayout(layout1)
        layoutInfo.addLayout(layout2)
        layoutInfo.addLayout(layout3)

        frameInfo.setLayout(layoutInfo)
        frameLayout.addWidget(racePhoto)
        frameLayout.addWidget(frameInfo)
        frame.setLayout(frameLayout)
        self.LayoutRaceList.addWidget(frame)

    def fillComboEditors(self):
        if self.database is None:
            return
        self.comboRacelist.clear()
        self.comboDriverList.clear()
        for race in self.database.getRaceNames(self.intSeizoen.date().year()):
            self.comboRacelist.addItems(race)
        for driver in self.database.getDrivers(self.intSeizoen.date().year()):
            self.comboDriverList.addItems(driver)

    def StandingsView(self):
        if self.database is None:
            return
        self.clearFrameTeamConfig(self.LayoutStandings)
        frame = QFrame()
        frame.setStyleSheet("""
                            QFrame {
                                border-bottom: 1px solid #dbdbdb;
                            }
                            """)
        layoutV = QVBoxLayout()

        f = QFont("Orbitron")
        f.setPointSize(14)
        
        for driver in self.database.getStandings(self.dateEdit.date().year()):
            layout = QHBoxLayout()
            lblName = QLabel(driver[0])
            lblPoints = QLabel(str(int(driver[1])))
            lblName.setFont(f)
            lblPoints.setFont(f)
            layout.addWidget(lblName)
            layout.addWidget(lblPoints)
            layoutV.addLayout(layout)
        frame.setLayout(layoutV)
        self.LayoutStandings.addWidget(frame)




class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet("background-color:black;")
        self.setMaximumHeight(20)
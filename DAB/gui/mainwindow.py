from PyQt5.QtWidgets import QMainWindow, QAction, QGridLayout, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.uic import loadUi
from PyQt5.QtGui import QKeySequence, QPixmap
from DAB.gui.menu import menu
from DAB.database.databasepy import Database
from PyQt5.QtCore import Qt


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

        self.database = Database()

        self.defineActions()
        self.tracks = None

        self.loadTracks()
        self.btnAddRace.clicked.connect(self.addRace)

        # fileMenuNames = [self.loadConfigAct, self.saveConfigAct]
        # fileMenu = menu(self, fileMenuNames, self.fileMenu)
        # self.database.updateDriverPhoto(1, "fotos/Coureurs/Lewis Hamilton.jpg")
        # self.database.updateDriverBLOBS()
        # self.database.updateCountryFlagsBLOB()

        # self.driverPhoto.setPixmap(self.database.getDriverPhoto(1))
        # self.driverPhoto.setPixmap(self.database.getDriverPhoto(1).scaled(self.driverPhoto.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # self.countryPhoto.setPixmap(self.database.getCountryFlag(1).scaled(self.countryPhoto.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # self.driverPhoto.setScaledContents(True)
        # self.spbDriverID.valueChanged.connect(self.updateDriverPhoto)
        print(self.database.getTeams(2021))
        self.fillDriverCombobox()
        self.fillTeamsCombobox()
        self.dateEdit.dateChanged.connect(self.fillDriverCombobox)
        self.comboDriver.currentIndexChanged.connect(self.updateDriverPhoto)
        self.comboTeams.currentIndexChanged.connect(self.displayTeamInfo)

    def fillDriverCombobox(self):
        self.comboDriver.clear()
        drivers = self.database.getDrivers(self.dateEdit.date().year())
        for driver in drivers:
            self.comboDriver.addItem(driver[0])
        self.updateDriverPhoto()
        

    def fillTeamsCombobox(self):
        self.comboTeams.clear()
        teams = self.database.getTeams(self.dateEdit.date().year())
        for team in teams:
            self.comboTeams.addItem(team[0])
        self.displayTeamInfo()

    def updateDriverPhoto(self):
        driverName = self.comboDriver.currentText()
        if driverName == "":
            return
        season = self.dateEdit.date().year()
        print(driverName)

        # driverID = self.database.getDriverID(driverName)

        self.driverPhoto.setPixmap(self.database.getDriverPhoto(driverName).scaled(self.driverPhoto.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.countryPhoto.setPixmap(self.database.getCountryFlag(driverName).scaled(self.countryPhoto.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    def loadTracks(self):
        self.tracks = self.database.getTracks()
        # print(tracks)
        for track in self.tracks:
            # print(track)
            self.comboTrackNames.addItem(track[2])

    def addRace(self):
        name = self.leRaceName.text()
        date = self.deRaceDate.date().toString('yyyy-MM-dd')
        track = self.comboTrackNames.currentText()
        track_id = next((t[0] for t in self.tracks if t[2] == track), None)
        round = self.spbRaceRound.value()
        # print(name, date, track, round)

        self.database.addRace(name, date, track_id, round)
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
        def clearFrameTeamConfig(self):
            layout = self.LayoutTeamConfig.layout()
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget() is not None:
                        child.widget().deleteLater()
            # self.FrameTeamConfig.setLayout(None)
        clearFrameTeamConfig(self)
        self.lblTeamName.setText(self.comboTeams.currentText())
        drivers = self.database.getDriversFromTeam(self.comboTeams.currentText(), self.dateEdit.date().year())
        # Drivername, image and country flag
        for driver in drivers:
            print("NAME MFERRRRRR" ,driver[0])
            frame = QFrame()
            frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout = QHBoxLayout()
            driverName = QLabel(driver[0])

            # driverID = self.database.getDriverID(driver[0])
            driverPhoto = self.database.getDriverPhoto(driver[0])
            lblDriverPhoto = QLabel()
            lblDriverPhoto.setMinimumHeight(100)
            lblDriverPhoto.setMinimumWidth(100)
            lblDriverPhoto.setPixmap(driverPhoto.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            countryFlag = self.database.getCountryFlag(driver[0])
            lblCountryFlag = QLabel()
            lblCountryFlag.setMinimumHeight(100)
            lblCountryFlag.setMinimumWidth(100)
            lblCountryFlag.setPixmap(countryFlag.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(driverName)
            layout.addWidget(lblDriverPhoto)
            layout.addWidget(lblCountryFlag)
            frame.setLayout(layout)
            self.LayoutTeamConfig.addWidget(frame)

from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox 
from PyQt5.uic import loadUi
from PyQt5.QtGui import QKeySequence
from DAB.gui.menu import menu
from DAB.database.databasepy import Database

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

    def loadTracks(self):
        self.tracks = self.database.getTracks()
        # print(tracks)
        for track in self.tracks:
            print(track)
            self.comboTrackNames.addItem(track[2])

    def addRace(self):
        name = self.leRaceName.text()
        date = self.deRaceDate.date().toString('yyyy-MM-dd')
        track = self.comboTrackNames.currentText()
        track_id = next((t[0] for t in self.tracks if t[2] == track), None)
        round = self.spbRaceRound.value()
        print(name, date, track, round)

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
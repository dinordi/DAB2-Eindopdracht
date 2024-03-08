from DAB.gui import mainwindow as mainwindowpy
from PyQt5.QtWidgets import QApplication 
import sys

if __name__ == '__main__': 
    """Startup of application and calling the MainWindow class"""
    app = QApplication(sys.argv) 
    mainWindow = mainwindowpy.MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
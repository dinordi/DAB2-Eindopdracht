from PyQt5.QtWidgets import QMenu


class menu():

    def __init__(self, MainWindow, menuNames, button):
        self.MainWindow = MainWindow
        self.menu = QMenu()
        self.callMenu(self.menu, menuNames)
        button.setMenu(self.menu)
    def callMenu(self, menubar, menuNames):
        for names in menuNames:
            if names == "separator":
                menubar.addSeparator()
                continue
            if type(names) == list:
                openMenu = menubar.addMenu(names[0])
                self.callMenu(openMenu, names[1])
                continue
            menubar.addAction(names)
    
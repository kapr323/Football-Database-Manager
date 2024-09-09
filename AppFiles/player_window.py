from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from players import load_players

class PlayerWindow(QWidget):
    def __init__(self, parent=None):
        super(PlayerWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Vytvoření tabulky pro zobrazení hráčů
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Profile", "Last Name", "First Name", "Short Name", "Nationality", "Born In Season"])

        # Načtení hráčů z JSON souboru
        players = load_players('players.json')
        self.table.setRowCount(len(players))

        for row, player in enumerate(players):
            if player.profile_picture:
                picture_label = QLabel()
                pixmap = QPixmap(player.profile_picture).scaled(50, 50, Qt.KeepAspectRatio)
                picture_label.setPixmap(pixmap)
                self.table.setCellWidget(row, 0, picture_label)
            else:
                self.table.setItem(row, 0, QTableWidgetItem(""))

            self.table.setItem(row, 1, QTableWidgetItem(player.last_name))
            self.table.setItem(row, 2, QTableWidgetItem(player.first_name))
            self.table.setItem(row, 3, QTableWidgetItem(player.short_name))
            self.table.setItem(row, 4, QTableWidgetItem(player.nationality))
            self.table.setItem(row, 5, QTableWidgetItem(player.born_in_season))

        layout.addWidget(self.table)
        self.setLayout(layout)

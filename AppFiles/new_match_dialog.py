from PyQt5.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel, QPushButton, QMessageBox

class NewMatchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('New Match')
        self.layout = QGridLayout(self)
        self.home_team_input = QLineEdit(self)
        self.away_team_input = QLineEdit(self)
        self.result_input = QLineEdit(self)
        self.layout.addWidget(QLabel('Home Team:'), 0, 0)
        self.layout.addWidget(self.home_team_input, 0, 1)
        self.layout.addWidget(QLabel('Away Team:'), 0, 2)
        self.layout.addWidget(self.away_team_input, 0, 3)
        self.layout.addWidget(QLabel('FT Result:'), 0, 4)
        self.layout.addWidget(self.result_input, 0, 5)
        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_match)
        self.layout.addWidget(self.save_button, 1, 0, 1, 6)

    def save_match(self):
        home_team = self.home_team_input.text()
        away_team = self.away_team_input.text()
        result = self.result_input.text()
        if home_team and away_team and result:
            self.match = {
                'home_team': home_team,
                'away_team': away_team,
                'result': result
            }
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields!')

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton,
                             QMessageBox, QComboBox)
import json
import os


class TournamentGenerator:
    def __init__(self, filename, path="../AppFiles/Data"):
        self.path = path
        self.filename = filename if filename.endswith(".json") else filename + ".json"
        self.full_path = os.path.join(self.path, self.filename)
        self.tournament = {
            "type": "League",
            "phase": "Main",
            "season": 1
        }
        self.teams = []
        self.matches = []

    def set_tournament_details(self, tournament_type, phase, season):
        self.tournament["type"] = tournament_type
        self.tournament["phase"] = phase
        self.tournament["season"] = season

    def set_teams(self, team_ids):
        for team_id in team_ids:
            team = {
                "id": team_id,
                "players": []
            }
            self.teams.append(team)

    def generate_matches_placeholder(self):
        self.matches = [{"id": idx + 1, "home_team": None, "away_team": None, "status": "Scheduled"} for idx in
                        range(len(self.teams) // 2)]

    def save_to_json(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        data = {
            "tournament": self.tournament,
            "teams": self.teams,
            "matches": self.matches
        }
        with open(self.full_path, 'w') as f:
            json.dump(data, f, indent=4)
        QMessageBox.information(None, "Success", f"JSON file {self.full_path} has been generated.")


class TournamentApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()

        # Filename
        filename_layout = QHBoxLayout()
        self.filename_label = QLabel("Filename:")
        self.filename_entry = QLineEdit()
        filename_layout.addWidget(self.filename_label)
        filename_layout.addWidget(self.filename_entry)

        # Tournament Type
        type_layout = QHBoxLayout()
        self.type_label = QLabel("Tournament Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["League", "Play-off"])
        type_layout.addWidget(self.type_label)
        type_layout.addWidget(self.type_combo)

        # Phase
        phase_layout = QHBoxLayout()
        self.phase_label = QLabel("Phase:")
        self.phase_combo = QComboBox()
        self.phase_combo.addItems(["Main", "Secondary", "Final Tournament", "Qualification"])
        phase_layout.addWidget(self.phase_label)
        phase_layout.addWidget(self.phase_combo)

        # Season
        season_layout = QHBoxLayout()
        self.season_label = QLabel("Season:")
        self.season_entry = QLineEdit()
        season_layout.addWidget(self.season_label)
        season_layout.addWidget(self.season_entry)

        # Team IDs
        teams_layout = QHBoxLayout()
        self.teams_label = QLabel("Team IDs (comma-separated):")
        self.teams_entry = QLineEdit()
        teams_layout.addWidget(self.teams_label)
        teams_layout.addWidget(self.teams_entry)

        # Button for JSON generation
        self.generate_button = QPushButton("Generate JSON")
        self.generate_button.clicked.connect(self.generate_json)

        # Add widgets to the main layout
        main_layout.addLayout(filename_layout)
        main_layout.addLayout(type_layout)
        main_layout.addLayout(phase_layout)
        main_layout.addLayout(season_layout)
        main_layout.addLayout(teams_layout)
        main_layout.addWidget(self.generate_button)

        self.setLayout(main_layout)
        self.setWindowTitle('Tournament Generator')

    def generate_json(self):
        filename = self.filename_entry.text()
        tournament_type = self.type_combo.currentText()
        phase = self.phase_combo.currentText()
        season = self.season_entry.text()
        teams = self.teams_entry.text()

        # Validation
        if not filename or not season or not teams:
            QMessageBox.critical(self, "Error", "Please fill all fields.")
            return

        try:
            season = int(season)
        except ValueError:
            QMessageBox.critical(self, "Error", "Season must be a number.")
            return

        try:
            team_ids = [int(team_id.strip()) for team_id in teams.split(",")]
        except ValueError:
            QMessageBox.critical(self, "Error", "Team IDs must be numbers separated by commas.")
            return

        # Generate JSON
        generator = TournamentGenerator(filename)
        generator.set_tournament_details(tournament_type, phase, season)
        generator.set_teams(team_ids)
        generator.generate_matches_placeholder()
        generator.save_to_json()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TournamentApp()
    window.show()
    sys.exit(app.exec_())

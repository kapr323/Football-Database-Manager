import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, \
    QLineEdit, QMessageBox, QDialog, QGridLayout, QTableWidget, QTableWidgetItem, QWidget, QTabWidget, QAction, QMenu, QMenuBar
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sports Database Manager')
        self.setGeometry(100, 100, 580, 720)

        # Set the application icon
        self.setWindowIcon(QIcon('AppFiles/pngwing.com.png'))

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.create_home_tab()
        self.create_matches_tab()
        self.create_teams_tab()
        self.create_statistics_tab()
        self.create_menu()

        self.apply_styles()

    def create_home_tab(self):
        self.home_tab = QWidget()
        layout = QVBoxLayout()

        self.add_background_logo(layout)

        self.open_file_button = QPushButton('Open JSON File')
        self.open_file_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.open_file_button)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_file)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button)

        self.home_tab.setLayout(layout)
        self.central_widget.addTab(self.home_tab, "Home")

    def add_background_logo(self, layout):
        background_label = QLabel(self)
        pixmap = QPixmap('AppFiles/pngwing.com.png')
        pixmap_width = pixmap.width()
        pixmap_height = pixmap.height()
        desired_width = int(self.width() * 0.3)
        aspect_ratio = pixmap_height / pixmap_width
        desired_height = int(desired_width * aspect_ratio)
        scaled_pixmap = pixmap.scaled(desired_width, desired_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        background_label.setPixmap(scaled_pixmap)
        background_label.setAlignment(Qt.AlignCenter)
        background_label.setStyleSheet("background: transparent; opacity: 0;")

        logo_layout = QHBoxLayout()
        logo_layout.addStretch()
        logo_layout.addWidget(background_label)
        logo_layout.addStretch()

        layout.addLayout(logo_layout)

    def create_matches_tab(self):
        self.matches_tab = QWidget()
        layout = QVBoxLayout()

        self.matches_table = QTableWidget()
        self.matches_table.setColumnCount(4)
        self.matches_table.setHorizontalHeaderLabels(['Home Team', 'Away Team', 'Result', 'Actions'])
        layout.addWidget(self.matches_table)

        self.new_match_button = QPushButton('New Match')
        self.new_match_button.clicked.connect(self.open_new_match_dialog)
        self.new_match_button.setEnabled(False)
        layout.addWidget(self.new_match_button)

        self.matches_tab.setLayout(layout)
        self.central_widget.addTab(self.matches_tab, "Matches")

    def create_teams_tab(self):
        self.teams_tab = QWidget()
        layout = QVBoxLayout()
        self.teams_table = QTableWidget()
        self.teams_table.setColumnCount(9)
        self.teams_table.setHorizontalHeaderLabels(
            ['Team', 'M', 'W', 'D', 'L', 'G+', 'G-', 'GD', 'Pts'])
        layout.addWidget(self.teams_table)
        self.teams_tab.setLayout(layout)
        self.central_widget.addTab(self.teams_tab, "Teams")

        self.set_default_column_visibility()

    def set_default_column_visibility(self):
        self.teams_table.setColumnHidden(2, True)  # W
        self.teams_table.setColumnHidden(3, True)  # D
        self.teams_table.setColumnHidden(4, True)  # L

    def create_statistics_tab(self):
        self.statistics_tab = QWidget()
        layout = QVBoxLayout()
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(3)
        self.stats_table.setHorizontalHeaderLabels(['Player', 'Team', 'Goals'])
        layout.addWidget(self.stats_table)
        self.statistics_tab.setLayout(layout)
        self.central_widget.addTab(self.statistics_tab, "Statistics")

    def create_menu(self):
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("View")

        self.create_column_visibility_action(view_menu, "Show Wins", 2)
        self.create_column_visibility_action(view_menu, "Show Draws", 3)
        self.create_column_visibility_action(view_menu, "Show Losses", 4)

    def create_column_visibility_action(self, menu, title, column):
        action = QAction(title, self, checkable=True)
        action.setChecked(False)
        action.toggled.connect(lambda checked, col=column: self.toggle_column_visibility(col, checked))
        menu.addAction(action)

    def toggle_column_visibility(self, column, visible):
        self.teams_table.setColumnHidden(column, not visible)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f8ff;
            }
            QPushButton {
                background-color: #87CEFA;
                border: none;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4682B4;
                color: #fff;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #87CEFA;
                padding: 5px;
                font-size: 14px;
            }
        """)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open JSON File', '', 'JSON Files (*.json)', options=options)
        if file_name:
            self.load_file(file_name)

    def load_file(self, file_name):
        self.current_file = file_name
        with open(self.current_file, 'r') as f:
            self.data = json.load(f)
        self.update_tables()
        self.new_match_button.setEnabled(True)
        self.save_button.setEnabled(True)

    def update_tables(self):
        self.update_matches_table()
        self.update_teams_table()
        self.update_stats_table()

    def update_matches_table(self):
        self.matches_table.setRowCount(0)
        matches = self.data.get('matches', [])
        for match in matches:
            row_position = self.matches_table.rowCount()
            self.matches_table.insertRow(row_position)
            self.matches_table.setItem(row_position, 0, QTableWidgetItem(match['home_team']))
            self.matches_table.setItem(row_position, 1, QTableWidgetItem(match['away_team']))
            self.matches_table.setItem(row_position, 2, QTableWidgetItem(match['result']))
            self.matches_table.setItem(row_position, 3, QTableWidgetItem('Edit'))

    def update_teams_table(self):
        teams_stats = self.calculate_team_statistics()
        self.teams_table.setRowCount(0)
        for team, stats in sorted(teams_stats.items(), key=lambda x: (
        -x[1]['points'], -x[1]['goal_difference'], -x[1]['goals_for'], -x[1]['won'], -x[1]['drawn'])):
            row_position = self.teams_table.rowCount()
            self.teams_table.insertRow(row_position)
            self.teams_table.setItem(row_position, 0, QTableWidgetItem(team))
            self.teams_table.setItem(row_position, 1, QTableWidgetItem(str(stats['played'])))
            self.teams_table.setItem(row_position, 2, QTableWidgetItem(str(stats['won'])))
            self.teams_table.setItem(row_position, 3, QTableWidgetItem(str(stats['drawn'])))
            self.teams_table.setItem(row_position, 4, QTableWidgetItem(str(stats['lost'])))
            self.teams_table.setItem(row_position, 5, QTableWidgetItem(str(stats['goals_for'])))
            self.teams_table.setItem(row_position, 6, QTableWidgetItem(str(stats['goals_against'])))
            self.teams_table.setItem(row_position, 7, QTableWidgetItem(str(stats['goal_difference'])))
            points_item = QTableWidgetItem(str(stats['points']))
            points_item.setFont(QFont('Arial', weight=QFont.Bold))
            self.teams_table.setItem(row_position, 8, points_item)

        # Adjust column widths
        self.teams_table.resizeColumnsToContents()
        self.teams_table.setColumnWidth(0, 150)  # Team column wider
        for i in range(1, 9):
            if i != 0:  # Adjust other columns to be smaller
                self.teams_table.setColumnWidth(i, 50)

    def calculate_team_statistics(self):
        teams_stats = {}
        for match in self.data.get('matches', []):
            home_team = match['home_team']
            away_team = match['away_team']
            home_goals, away_goals = map(int, match['result'].split(':'))

            if home_team not in teams_stats:
                teams_stats[home_team] = {'played': 0, 'won': 0, 'drawn': 0, 'lost': 0, 'goals_for': 0,
                                          'goals_against': 0, 'goal_difference': 0, 'points': 0}
            if away_team not in teams_stats:
                teams_stats[away_team] = {'played': 0, 'won': 0, 'drawn': 0, 'lost': 0, 'goals_for': 0,
                                          'goals_against': 0, 'goal_difference': 0, 'points': 0}

            teams_stats[home_team]['played'] += 1
            teams_stats[away_team]['played'] += 1
            teams_stats[home_team]['goals_for'] += home_goals
            teams_stats[home_team]['goals_against'] += away_goals
            teams_stats[away_team]['goals_for'] += away_goals
            teams_stats[away_team]['goals_against'] += home_goals
            teams_stats[home_team]['goal_difference'] = teams_stats[home_team]['goals_for'] - teams_stats[home_team][
                'goals_against']
            teams_stats[away_team]['goal_difference'] = teams_stats[away_team]['goals_for'] - teams_stats[away_team][
                'goals_against']

            if home_goals > away_goals:
                teams_stats[home_team]['won'] += 1
                teams_stats[away_team]['lost'] += 1
                teams_stats[home_team]['points'] += 3
            elif home_goals < away_goals:
                teams_stats[away_team]['won'] += 1
                teams_stats[home_team]['lost'] += 1
                teams_stats[away_team]['points'] += 3
            else:
                teams_stats[home_team]['drawn'] += 1
                teams_stats[away_team]['drawn'] += 1
                teams_stats[home_team]['points'] += 1
                teams_stats[away_team]['points'] += 1

        return teams_stats

    def update_stats_table(self):
        self.stats_table.setRowCount(0)
        stats = self.data.get('stats', [])
        for stat in stats:
            row_position = self.stats_table.rowCount()
            self.stats_table.insertRow(row_position)
            self.stats_table.setItem(row_position, 0, QTableWidgetItem(stat['player']))
            self.stats_table.setItem(row_position, 1, QTableWidgetItem(stat['team']))
            self.stats_table.setItem(row_position, 2, QTableWidgetItem(str(stat['goals'])))

    def open_new_match_dialog(self):
        dialog = NewMatchDialog(self)
        if dialog.exec_():
            if 'matches' not in self.data:
                self.data['matches'] = []
            self.data['matches'].append(dialog.match)
            self.update_matches_table()
            self.update_teams_table()

    def save_file(self):
        with open(self.current_file, 'w') as f:
            json.dump(self.data, f, indent=4)
        QMessageBox.information(self, 'Success', 'File saved successfully!')


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


def main():
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

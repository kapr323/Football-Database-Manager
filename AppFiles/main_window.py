import os
import traceback
import json
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, \
    QTableWidget, QTableWidgetItem, QWidget, QTabWidget, QAction, QMenuBar, QMessageBox, QSizePolicy, \
    QProgressDialog
from PyQt5.QtGui import QPixmap, QFont, QIcon, QMovie
from PyQt5.QtCore import Qt, QTimer
from new_match_dialog import NewMatchDialog
from utils import calculate_team_statistics

class NumericSortItem(QTableWidgetItem):
    def __lt__(self, other):
        # Kontrola, zda je hodnota číslo
        if isinstance(other, QTableWidgetItem):
            try:
                # Pokus o převod na číslo
                return float(self.text()) < float(other.text())
            except ValueError:
                # Pokud převod selže, použije se standardní textové porovnání
                return super().__lt__(other)
        return super().__lt__(other)


class MainApp(QMainWindow):
    def default_geometry(self):
        self.setGeometry(2000, 100, 720, 720)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Football Database Manager')
        self.default_geometry()

        # Set the application icon
        self.setWindowIcon(QIcon('pngwing.com.png'))

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.currentChanged.connect(self.on_tab_change)

        self.create_home_tab()
        self.create_matches_tab()
        self.create_teams_tab()
        self.create_statistics_tab()
        self.create_players_database_tab()
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
        pixmap = QPixmap('pngwing.com.png')
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

    def create_players_database_tab(self):
        self.players_db_tab = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Photo","Last Name", "First Name", "Short Name", "Nationality", "Born in Season"])
        layout.addWidget(self.table)

        self.load_players_data()
        self.table.setSortingEnabled(True)
        self.players_db_tab.setLayout(layout)
        self.central_widget.addTab(self.players_db_tab, "Players DB")

    def load_players_data(self):
        with open('Data/players.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        players = data['players']
        self.table.setRowCount(len(players))

        for row, player in enumerate(players):
            picture_label = QLabel()
            picture_path = None
            for ext in ['jpg', 'png', 'webp']:  # Přidejte další přípony podle potřeby
                potential_path = f'Data/Players/{player["id"]}.{ext}'
                if os.path.exists(potential_path):
                    picture_path = potential_path
                    break

            if picture_path:
                pixmap = QPixmap(picture_path)
                row_height = self.table.rowHeight(row)
                scaled_pixmap = pixmap.scaledToHeight(row_height, Qt.SmoothTransformation)
                picture_label.setPixmap(scaled_pixmap)
                picture_label.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(row, 1, picture_label)
            else:
                self.table.setItem(row, 1, QTableWidgetItem("N/A"))
            self.table.setItem(row, 0, NumericSortItem(str(player['id'])))
            self.table.setItem(row, 2, QTableWidgetItem(player['last_name']))
            self.table.setItem(row, 3, QTableWidgetItem(player['first_name']))
            self.table.setItem(row, 4, QTableWidgetItem(player.get('short_name', '')))

            # Vytvoření widgetu pro kombinaci obrázku a textu
            nationality_widget = QWidget()
            layout = QHBoxLayout()

            # Vytvoření QLabel pro obrázek bez ohraničení
            flag_label = QLabel()
            nationality_pixmap = QPixmap(player['nationality']).scaled(row_height, row_height, Qt.KeepAspectRatio,
                                                                       Qt.SmoothTransformation)
            flag_label.setPixmap(nationality_pixmap)

            # Nastavení fixní výšky pro obrázek
            flag_label.setFixedHeight(row_height)
            flag_label.setMaximumWidth(flag_label.pixmap().width())

            # Extrakce názvu země z cesty
            nationality_path = player['nationality']
            start = nationality_path.rfind('/') + 1
            end = nationality_path.rfind('.')
            country_name = nationality_path[start:end]

            # Vytvoření QLabel pro text vedle obrázku
            text_label = QLabel(country_name)
            text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            # Přidání obrázku a textu do layoutu
            layout.addWidget(flag_label)
            layout.addWidget(text_label)
            layout.addStretch()  # Přidání prostoru na pravé straně

            # Nastavení layoutu na widget
            nationality_widget.setLayout(layout)

            # Zarovnání widgetu poté, co byl přidán do rozložení
            flag_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            # Nastavení widgetu do tabulky
            self.table.setCellWidget(row, 5, nationality_widget)

            # Nastavení textu pro řazení
            sort_item = QTableWidgetItem(country_name)
            sort_item.setFlags(Qt.ItemIsEnabled)  # Zajistí, že text nebude interaktivní
            sort_item.setForeground(Qt.white)  # Skryje text nastavením bílé barvy (nebo barvy pozadí tabulky)
            self.table.setItem(row, 5, sort_item)  # Používáme stejný index sloupce jako pro widget

            # Povolení řazení
            self.table.setSortingEnabled(True)

            self.table.setItem(row, 6, NumericSortItem(str(player['born_in_season'])))
        self.table.resizeColumnToContents(1)
        self.table.setColumnWidth(0, 35)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(6, 35)

    # test
    def on_tab_change(self, index):
        if self.central_widget.tabText(index) == "Players DB":
            QTimer.singleShot(200, self.load_players_data)
            self.resize(800, 720)
        else:
            self.resize(720, 720)

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
        with open("styles.qss", "r") as f:
            self.setStyleSheet(f.read())

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open JSON File', '', 'JSON Files (*.json)', options=options)
        if file_name:
            self.load_file(file_name)

    def load_file(self, file_name):
        self.current_file = file_name
        try:
            with open(self.current_file, 'r') as f:
                self.data = json.load(f)
            print("File loaded successfully:", file_name)  # Pro ladění
            self.update_tables()
            self.new_match_button.setEnabled(True)
            self.save_button.setEnabled(True)
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, 'Error', f'Failed to load JSON file:\n{e}')
            print("JSON decode error:", e)  # Pro ladění
            traceback.print_exc()  # Zobrazí podrobnosti o chybě
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An unexpected error occurred:\n{e}')
            print("Unexpected error:", e)  # Pro ladění
            traceback.print_exc()  # Zobrazí podrobnosti o chybě

    def update_tables(self):
        self.update_matches_table()
        self.update_teams_table()
        self.update_stats_table()

    def update_matches_table(self):
        try:
            self.matches_table.setRowCount(0)
            matches = self.data.get('matches', [])
            teams = self.data.get('teams', [])  # Načtení seznamu týmů

            for match in matches:
                row_position = self.matches_table.rowCount()
                self.matches_table.insertRow(row_position)

                # Získání domácího a hostujícího týmu podle indexu
                home_team = teams[match['home_team']]['full_name'] if 0 <= match['home_team'] < len(
                    teams) else 'Unknown'
                away_team = teams[match['away_team']]['full_name'] if 0 <= match['away_team'] < len(
                    teams) else 'Unknown'

                # Získání výsledku: spojení status + home_goals + ":" + away_goals
                status = match.get('status', 'N/A')
                home_goals = match.get('home_goals', 0)
                away_goals = match.get('away_goals', 0)
                result = f"{status} {home_goals}:{away_goals}"

                # Vložení týmů a výsledku do tabulky
                self.matches_table.setItem(row_position, 0, QTableWidgetItem(home_team))
                self.matches_table.setItem(row_position, 1, QTableWidgetItem(away_team))
                self.matches_table.setItem(row_position, 2, QTableWidgetItem(result))
                self.matches_table.setItem(row_position, 3, QTableWidgetItem('Edit'))
        except Exception as e:
            print(f"Unexpected error: {e}")
            traceback.print_exc()  # Zobrazí podrobnosti o chybě

    def update_teams_table(self):
        teams_stats = calculate_team_statistics(self.data)
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

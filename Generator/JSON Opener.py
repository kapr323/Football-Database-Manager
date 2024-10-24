import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, \
    QTableWidgetItem, QWidget


class JsonTableViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('JSON Table Viewer')
        self.setGeometry(100, 100, 1000, 600)

        # Create main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Button to load JSON
        self.load_button = QPushButton('Load JSON', self)
        self.load_button.clicked.connect(self.load_json)
        self.layout.addWidget(self.load_button)

        # Table to display JSON data
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

    def load_json(self):
        # Open file dialog to select JSON file
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open JSON file', '', 'JSON files (*.json)')

        if file_name:
            with open(file_name, 'r') as file:
                data = json.load(file)
                self.display_json(data)

    def display_json(self, data):
        # Clear the table before displaying new data
        self.table.clear()

        # Flatten the JSON data to create a list of dictionaries
        flattened_data = self.flatten_json(data)

        # Extract unique keys for columns
        columns = set()
        for item in flattened_data:
            columns.update(item.keys())
        columns = sorted(list(columns))

        # Set table size based on data
        self.table.setColumnCount(len(columns))
        self.table.setRowCount(len(flattened_data))
        self.table.setHorizontalHeaderLabels(columns)

        # Fill table with data
        for row, item in enumerate(flattened_data):
            for col, key in enumerate(columns):
                value = item.get(key, "null")  # Show "null" if the key doesn't exist
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def flatten_json(self, nested_json):
        """Convert a nested JSON object into a flat list of dictionaries."""
        flat_data = []
        if isinstance(nested_json, dict):
            for key, value in nested_json.items():
                if key == "teams":  # Ignore common key like "teams"
                    if isinstance(value, list):
                        for item in value:
                            flat_data.append(self.flatten_dict(item))
        return flat_data

    def flatten_dict(self, d, parent_key='', sep='.'):
        """Flatten a nested dictionary."""
        items = {}
        for k, v in d.items():
            if k == "teams":  # Ignore the "teams" key
                continue
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self.flatten_dict(v, new_key, sep=sep))
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    list_key = f"{new_key}[{i}]"
                    if isinstance(item, dict):
                        items.update(self.flatten_dict(item, list_key, sep=sep))
                    else:
                        items[list_key] = item
            else:
                items[new_key] = v
        return items


# Main application loop
if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = JsonTableViewer()
    viewer.show()
    sys.exit(app.exec_())

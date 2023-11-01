import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QListWidget, QTabWidget, QFormLayout, QSpinBox, QComboBox, QHBoxLayout)
from PyQt5.QtGui import QColor

# Database setup
def setup_database():
    conn = sqlite3.connect('macbook_parts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Parts (
        part_id INTEGER PRIMARY KEY,
        part_name TEXT NOT NULL,
        part_type TEXT NOT NULL,
        stock_amount INTEGER NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Compatibility (
        compatibility_id INTEGER PRIMARY KEY,
        part_id INTEGER,
        model_number TEXT NOT NULL,
        FOREIGN KEY (part_id) REFERENCES Parts(part_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProcessedDevices (
        date DATE PRIMARY KEY,
        manifests INTEGER DEFAULT 0,
        recycles INTEGER DEFAULT 0,
        repairs INTEGER DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close()

# GUI setup
class MacBookRepairApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Inventory Management Tab
        self.inventory_tab = QWidget()
        self.inventory_layout = QVBoxLayout()

        # Initialize parts_listbox
        self.parts_listbox = QListWidget(self)
        self.inventory_layout.addWidget(self.parts_listbox)

        # Part Name
        part_name_layout = QHBoxLayout()
        part_name_layout.setSpacing(10)
        part_name_layout.addWidget(QLabel('Part Name:'), 1)
        self.part_name_entry = QLineEdit(self)
        part_name_layout.addWidget(self.part_name_entry, 4)
        self.inventory_layout.addLayout(part_name_layout)

        # Part Type
        part_type_layout = QHBoxLayout()
        part_type_layout.setSpacing(10)
        part_type_layout.addWidget(QLabel('Part Type:'), 1)
        self.part_type_combobox = QComboBox(self)
        self.part_type_combobox.addItems(["Screen", "Battery", "Trackpad", "Feet", "HDD", "SSD", "Logic Board", "Glass Bezel", "RAM", "Other"])
        part_type_layout.addWidget(self.part_type_combobox, 4)
        self.inventory_layout.addLayout(part_type_layout)

        # Change Amount
        change_amount_layout = QHBoxLayout()
        change_amount_layout.setSpacing(10)
        change_amount_layout.addWidget(QLabel('Change Amount:'), 1)
        self.change_amount_spinbox = QSpinBox(self)
        self.change_amount_spinbox.setRange(0, 9999)
        change_amount_layout.addWidget(self.change_amount_spinbox, 4)
        self.inventory_layout.addLayout(change_amount_layout)

        # Add and Subtract Buttons
        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton('Add Amount', self)
        self.add_button.clicked.connect(self.add_stock_amount)
        buttons_layout.addWidget(self.add_button)
        self.subtract_button = QPushButton('Subtract Amount', self)
        self.subtract_button.clicked.connect(self.subtract_stock_amount)
        buttons_layout.addWidget(self.subtract_button)
        self.inventory_layout.addLayout(buttons_layout)

        # Set Amount
        set_amount_layout = QHBoxLayout()
        set_amount_layout.setSpacing(10)
        set_amount_layout.addWidget(QLabel('Set Amount:'), 1)
        self.set_amount_spinbox = QSpinBox(self)
        self.set_amount_spinbox.setRange(0, 9999)
        set_amount_layout.addWidget(self.set_amount_spinbox, 4)
        self.inventory_layout.addLayout(set_amount_layout)

        # Set Button
        self.set_button = QPushButton('Set Amount', self)
        self.set_button.clicked.connect(self.set_stock_amount)
        self.inventory_layout.addWidget(self.set_button)

        self.inventory_tab.setLayout(self.inventory_layout)
        self.tabs.addTab(self.inventory_tab, "Inventory Management")

        # Stock Look-up Tab
        self.lookup_tab = QWidget()
        self.lookup_layout = QVBoxLayout()

        self.model_number_label = QLabel('Model Number:')
        self.model_number_entry = QLineEdit(self)
        self.lookup_button = QPushButton('Look Up', self)
        self.lookup_button.clicked.connect(self.lookup_parts)
        self.lookup_listbox = QListWidget(self)

        self.lookup_layout.addWidget(self.model_number_label)
        self.lookup_layout.addWidget(self.model_number_entry)
        self.lookup_layout.addWidget(self.lookup_button)
        self.lookup_layout.addWidget(self.lookup_listbox)

        self.lookup_tab.setLayout(self.lookup_layout)
        self.tabs.addTab(self.lookup_tab, "Stock Look-up")

        # Part Configurator Tab
        self.configurator_tab = QWidget()
        self.configurator_layout = QVBoxLayout()

        self.part_lookup_label = QLabel('Part Name:')
        self.part_lookup_entry = QLineEdit(self)
        self.part_lookup_button = QPushButton('Look Up Models', self)
        self.part_lookup_button.clicked.connect(self.lookup_models)
        self.models_listbox = QListWidget(self)

        self.model_association_label = QLabel('Model Number:')
        self.model_association_entry = QLineEdit(self)
        self.associate_button = QPushButton('Associate with Part', self)
        self.associate_button.clicked.connect(self.associate_model)
        self.remove_association_button = QPushButton('Remove Association', self)
        self.remove_association_button.clicked.connect(self.remove_association)

        self.configurator_layout.addWidget(self.part_lookup_label)
        self.configurator_layout.addWidget(self.part_lookup_entry)
        self.configurator_layout.addWidget(self.part_lookup_button)
        self.configurator_layout.addWidget(self.models_listbox)
        self.configurator_layout.addWidget(self.model_association_label)
        self.configurator_layout.addWidget(self.model_association_entry)
        self.configurator_layout.addWidget(self.associate_button)
        self.configurator_layout.addWidget(self.remove_association_button)

        self.configurator_tab.setLayout(self.configurator_layout)
        self.tabs.addTab(self.configurator_tab, "Part Configurator")

        self.init_settings_tab()
        self.init_reporting_tab()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.setWindowTitle('MacBook Repair App')
        self.show()

    def update_parts_listbox(self):
        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()
        cursor.execute('SELECT part_name, part_type, stock_amount FROM Parts')
        parts = cursor.fetchall()
        conn.close()

        self.parts_listbox.clear()
        for part in parts:
            self.parts_listbox.addItem(f"{part[0]} ({part[1]}) - {part[2]} in stock")

    def add_stock_amount(self):
        part_name = self.part_name_entry.text()
        part_type = self.part_type_combobox.currentText()
        add_amount = self.change_amount_spinbox.value()

        if not part_name:
            print("Please enter a part name.")
            return

        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()

        cursor.execute('SELECT stock_amount FROM Parts WHERE part_name = ?', (part_name,))
        result = cursor.fetchone()

        if result:
            new_amount = result[0] + add_amount
            cursor.execute('UPDATE Parts SET stock_amount = ? WHERE part_name = ?', (new_amount, part_name))
        else:
            cursor.execute('INSERT INTO Parts (part_name, part_type, stock_amount) VALUES (?, ?, ?)', (part_name, part_type, add_amount))

        conn.commit()
        conn.close()

        self.update_parts_listbox()

    def subtract_stock_amount(self):
        part_name = self.part_name_entry.text()
        subtract_amount = self.change_amount_spinbox.value()

        if not part_name:
            print("Please enter a part name.")
            return

        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()

        cursor.execute('SELECT stock_amount FROM Parts WHERE part_name = ?', (part_name,))
        result = cursor.fetchone()

        if result:
            new_amount = max(0, result[0] - subtract_amount)  # Ensure stock doesn't go negative
            cursor.execute('UPDATE Parts SET stock_amount = ? WHERE part_name = ?', (new_amount, part_name))

        conn.commit()
        conn.close()

        self.update_parts_listbox()

    def set_stock_amount(self):
        part_name = self.part_name_entry.text()
        set_amount = self.set_amount_spinbox.value()

        if not part_name:
            print("Please enter a part name.")
            return

        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE Parts SET stock_amount = ? WHERE part_name = ?', (set_amount, part_name))

        conn.commit()
        conn.close()

        self.update_parts_listbox()

    def lookup_parts(self):
        model_number = self.model_number_entry.text()
        if not model_number:
            print("Please enter a model number.")
            return

        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT part_name, part_type FROM Parts
        INNER JOIN Compatibility ON Parts.part_id = Compatibility.part_id
        WHERE model_number = ?
        ''', (model_number,))

        parts = cursor.fetchall()
        conn.close()

        self.lookup_listbox.clear()
        for part in parts:
            self.lookup_listbox.addItem(f"{part[0]} ({part[1]})")

    def lookup_models(self):
        part_name = self.part_lookup_entry.text()
        if not part_name:
            print("Please enter a part name.")
            return

        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT model_number FROM Compatibility
        INNER JOIN Parts ON Compatibility.part_id = Parts.part_id
        WHERE part_name = ?
        ''', (part_name,))

        models = cursor.fetchall()
        conn.close()

        self.models_listbox.clear()
        for model in models:
            self.models_listbox.addItem(model[0])

    def associate_model(self):
        part_name = self.part_lookup_entry.text()
        model_number = self.model_association_entry.text()

        if not part_name or not model_number:
            print("Please enter both part name and model number.")
            return

        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()

        cursor.execute('SELECT part_id FROM Parts WHERE part_name = ?', (part_name,))
        part_id = cursor.fetchone()

        if part_id:
            cursor.execute('SELECT * FROM Compatibility WHERE part_id = ? AND model_number = ?', (part_id[0], model_number))
            existing_association = cursor.fetchone()
            if not existing_association:
                cursor.execute('INSERT INTO Compatibility (part_id, model_number) VALUES (?, ?)', (part_id[0], model_number))
        else:
            print("This association already exists.")

        conn.commit()
        conn.close()

        self.lookup_models()

    def remove_association(self):
        part_name = self.part_lookup_entry.text()
        model_number = self.model_association_entry.text()

        if not part_name or not model_number:
            print("Please enter both part name and model number.")
            return

        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()

        cursor.execute('SELECT part_id FROM Parts WHERE part_name = ?', (part_name,))
        part_id = cursor.fetchone()

        if part_id:
            cursor.execute('DELETE FROM Compatibility WHERE part_id = ? AND model_number = ?', (part_id[0], model_number))

        conn.commit()
        conn.close()

        self.lookup_models()

    def init_settings_tab(self):
        self.settings_tab = QWidget()
        settings_layout = QVBoxLayout()

        # Delete and Re-create a new database
        self.reset_db_button = QPushButton('Delete and Re-create Database', self)
        self.reset_db_button.clicked.connect(self.reset_database)
        settings_layout.addWidget(self.reset_db_button)

        # Delete a part from the database
        self.delete_part_combobox = QComboBox(self)
        # Populate the combobox with parts from the database (you can update this list whenever parts are added/removed)
        settings_layout.addWidget(QLabel('Select Part to Delete:'))
        settings_layout.addWidget(self.delete_part_combobox)
        self.delete_part_button = QPushButton('Delete Part', self)
        self.delete_part_button.clicked.connect(self.delete_part)
        settings_layout.addWidget(self.delete_part_button)

        # Delete a model from the database
        self.delete_model_combobox = QComboBox(self)
        # Populate the combobox with models from the database (you can update this list whenever models are added/removed)
        settings_layout.addWidget(QLabel('Select Model to Delete:'))
        settings_layout.addWidget(self.delete_model_combobox)
        self.delete_model_button = QPushButton('Delete Model and Associated Parts', self)
        self.delete_model_button.clicked.connect(self.delete_model)
        settings_layout.addWidget(self.delete_model_button)

        self.settings_tab.setLayout(settings_layout)
        self.tabs.addTab(self.settings_tab, "Settings")

    def reset_database(self):
        # Prompt the user for confirmation
        confirmation = input("Are you sure you want to delete and re-create the database? (yes/no): ")
        if confirmation.lower() == 'yes':
            # Delete the database
            # Note: You might need to close the database connection before deleting it
            # os.remove('macbook_parts.db')
            # Create a new database
            setup_database()

    def delete_part(self):
        part_name = self.delete_part_combobox.currentText()
        # Delete the part from the database
        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Parts WHERE part_name = ?', (part_name,))
        conn.commit()
        conn.close()

    def delete_model(self):
        model_number = self.delete_model_combobox.currentText()
        # Delete the model and its associated parts from the database
        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Compatibility WHERE model_number = ?', (model_number,))
        cursor.execute('DELETE FROM Parts WHERE part_name IN (SELECT part_name FROM Compatibility WHERE model_number = ?)', (model_number,))
        conn.commit()
        conn.close()

    def init_reporting_tab(self):
        self.reporting_tab = QWidget()
        reporting_layout = QVBoxLayout()

        # User Input
        input_layout = QFormLayout()
        self.category_combobox = QComboBox(self)
        self.category_combobox.addItems(["Manifests", "Recycles", "Repairs"])
        input_layout.addRow('Category:', self.category_combobox)
        reporting_layout.addLayout(input_layout)

        # Increment/Decrement Buttons
        increments_layout = QHBoxLayout()
        self.increment_1_button = QPushButton('+1', self)
        self.increment_1_button.clicked.connect(lambda: self.update_counts(1))
        self.decrement_1_button = QPushButton('-1', self)
        self.decrement_1_button.clicked.connect(lambda: self.update_counts(-1))
        self.increment_10_button = QPushButton('+10', self)
        self.increment_10_button.clicked.connect(lambda: self.update_counts(10))
        self.decrement_10_button = QPushButton('-10', self)
        self.decrement_10_button.clicked.connect(lambda: self.update_counts(-10))
        self.increment_100_button = QPushButton('+100', self)
        self.increment_100_button.clicked.connect(lambda: self.update_counts(100))
        self.decrement_100_button = QPushButton('-100', self)
        self.decrement_100_button.clicked.connect(lambda: self.update_counts(-100))
        increments_layout.addWidget(self.increment_1_button)
        increments_layout.addWidget(self.decrement_1_button)
        increments_layout.addWidget(self.increment_10_button)
        increments_layout.addWidget(self.decrement_10_button)
        increments_layout.addWidget(self.increment_100_button)
        increments_layout.addWidget(self.decrement_100_button)
        reporting_layout.addLayout(increments_layout)

        # Statistics Timeframe
        stats_layout = QHBoxLayout()
        self.stats_label = QLabel('Timeframe For Reports:')
        self.stats_combobox = QComboBox(self)
        self.stats_combobox.addItems(["Today", "Last Week", "Last Month", "Last Year"])
        stats_layout.addWidget(self.stats_label)
        stats_layout.addWidget(self.stats_combobox)
        reporting_layout.addLayout(stats_layout)

        self.reporting_tab.setLayout(reporting_layout)
        self.tabs.addTab(self.reporting_tab, "Reporting")

    
    def update_counts(self, increment):
        category = self.category_combobox.currentText().lower()
        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()

        # Check if there's an entry for today
        cursor.execute('SELECT * FROM ProcessedDevices WHERE date = DATE("now")')
        entry = cursor.fetchone()

        if entry:
            # Update the existing entry
            cursor.execute(f'UPDATE ProcessedDevices SET {category} = {category} + ? WHERE date = DATE("now")', (increment,))
        else:
            # Insert a new entry for today
            cursor.execute(f'INSERT INTO ProcessedDevices (date, {category}) VALUES (DATE("now"), ?)', (increment,))

        conn.commit()
        conn.close()

        # Update the statistics display
        self.update_statistics()

    def update_statistics(self):
        period = self.stats_combobox.currentText().lower()
        conn = sqlite3.connect('macbook_parts.db')
        cursor = conn.cursor()

        if period == "day":
            cursor.execute('SELECT SUM(manifests), SUM(recycles), SUM(repairs) FROM ProcessedDevices WHERE date = DATE("now")')
        elif period == "week":
            cursor.execute('SELECT SUM(manifests), SUM(recycles), SUM(repairs) FROM ProcessedDevices WHERE date BETWEEN DATE("now", "-6 days") AND DATE("now")')
        else:  # month
            cursor.execute('SELECT SUM(manifests), SUM(recycles), SUM(repairs) FROM ProcessedDevices WHERE date BETWEEN DATE("now", "start of month") AND DATE("now")')

        stats = cursor.fetchone()
        conn.close()

        self.stats_label.setText(f'Statistics for {period.capitalize()}: Manifests: {stats[0]}, Recycles: {stats[1]}, Repairs: {stats[2]}')

if __name__ == "__main__":
    setup_database()
    app = QApplication(sys.argv)
    ex = MacBookRepairApp()
    sys.exit(app.exec_())


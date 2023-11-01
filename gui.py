import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QListWidget, QTabWidget, QHBoxLayout, QComboBox, QSpinBox, QFormLayout)
from PyQt5.QtGui import QColor
# Import the database functions
import database
from database import (add_stock_amount, subtract_stock_amount, set_stock_amount, lookup_parts, lookup_models, associate_model, 
                      remove_association, reset_database, delete_model, delete_part)

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
        self.add_button.clicked.connect(lambda: add_stock_amount(self))

        buttons_layout.addWidget(self.add_button)
        self.subtract_button = QPushButton('Subtract Amount', self)
        self.subtract_button.clicked.connect(lambda: subtract_stock_amount(self))

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
        self.set_button.clicked.connect(lambda: set_stock_amount(self))

        self.inventory_layout.addWidget(self.set_button)

        self.inventory_tab.setLayout(self.inventory_layout)
        self.tabs.addTab(self.inventory_tab, "Inventory Management")

        # Stock Look-up Tab
        self.lookup_tab = QWidget()
        self.lookup_layout = QVBoxLayout()

        self.model_number_label = QLabel('Model Number:')
        self.model_number_entry = QLineEdit(self)
        self.lookup_button = QPushButton('Look Up', self)
        self.lookup_button.clicked.connect(lambda: lookup_parts(self))
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
        self.part_lookup_button.clicked.connect(lambda: lookup_models(self))

        self.models_listbox = QListWidget(self)

        self.model_association_label = QLabel('Model Number:')
        self.model_association_entry = QLineEdit(self)
        self.associate_button = QPushButton('Associate with Part', self)
        self.associate_button.clicked.connect(lambda: associate_model(self))
        self.remove_association_button = QPushButton('Remove Association', self)
        self.remove_association_button.clicked.connect(lambda: remove_association(self))

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

    def init_settings_tab(self):
        self.settings_tab = QWidget()
        settings_layout = QVBoxLayout()

        # Delete and Re-create a new database
        self.reset_db_button = QPushButton('Delete and Re-create Database', self)
        self.reset_db_button.clicked.connect(lambda: reset_database(self))
        settings_layout.addWidget(self.reset_db_button)

        # Delete a part from the database
        self.delete_part_combobox = QComboBox(self)
        # Populate the combobox with parts from the database (you can update this list whenever parts are added/removed)
        settings_layout.addWidget(QLabel('Select Part to Delete:'))
        settings_layout.addWidget(self.delete_part_combobox)
        self.delete_part_button = QPushButton('Delete Part', self)
        self.delete_part_button.clicked.connect(lambda: delete_part(self))
        settings_layout.addWidget(self.delete_part_button)

        # Delete a model from the database
        self.delete_model_combobox = QComboBox(self)
        # Populate the combobox with models from the database (you can update this list whenever models are added/removed)
        settings_layout.addWidget(QLabel('Select Model to Delete:'))
        settings_layout.addWidget(self.delete_model_combobox)
        self.delete_model_button = QPushButton('Delete Model and Associated Parts', self)
        self.delete_model_button.clicked.connect(lambda: delete_model(self))
        settings_layout.addWidget(self.delete_model_button)

        self.settings_tab.setLayout(settings_layout)
        self.tabs.addTab(self.settings_tab, "Settings")

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

if __name__ == "__main__":
    app = QApplication([])
    ex = MacBookRepairApp()
    app.exec_()

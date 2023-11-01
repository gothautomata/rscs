import sys
from gui import MacBookRepairApp
from PyQt5.QtWidgets import QApplication
import database

if __name__ == "__main__":
    database.setup_database()
    app = QApplication(sys.argv)
    ex = MacBookRepairApp()
    sys.exit(app.exec_())

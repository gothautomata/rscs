# Repair Station Convinience Service (RSCS)

RSCS is a comprehensive inventory management system designed for tracking MacBook parts. Built with PyQt5 and SQLite, it offers a user-friendly interface for managing stock levels, part compatibility, and processing device repairs, recycles, and manifests.

## Features

- **Inventory Management**: Add, subtract, and set stock amounts for parts.
- **Stock Lookup**: Search for parts by MacBook model number.
- **Part Compatibility**: Associate parts with specific MacBook models and remove associations as needed.
- **Settings**: Manage database settings, including part and model deletion.
- **Reporting**: Keep track of processed devices with increment and decrement controls for manifests, recycles, and repairs.

## Installation

Before running the application, ensure you have Python and PyQt5 installed on your system. If you don't have PyQt5, you can install it using pip:

```bash
pip install PyQt5
```

## Usage
To start the application, run the following command in your terminal:

```bash
python macbook_repair_app.py
```
## Database Setup
The application uses SQLite to manage data. The database is automatically set up with the necessary tables when you start the application for the first time.

## Application Structure
- setup_database(): Sets up the SQLite database with the required tables.
- MacBookRepairApp: The main class for the application, containing all the UI elements and logic.

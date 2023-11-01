import sqlite3

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
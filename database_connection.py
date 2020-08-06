import sqlite3
import exception_utility as excep

class Database:

    def __init__(self, db_file):
        self.db_file = db_file
        self.acursor = None

        self.db = None
        self.create_connection(db_file)

    def create_connection(self, db_file):
        try:
            self.db = sqlite3.connect(db_file)
            self.acursor = self.db.cursor()
            self.create_tables()
            self.db.commit()
        except sqlite3.Error as e:
            print(e)

    def create_tables(self):
        if self.acursor:
            self.acursor.execute(
                'CREATE TABLE IF NOT EXISTS employee (emp_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,'
                ' name TEXT NOT NULL)')
            self.acursor.execute(
                'CREATE TABLE IF NOT EXISTS timestamp (clock_on TEXT, clock_off TEXT, emp_id INTEGER NOT NULL,'
                ' date TEXT, record_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE)')

    # BACKEND FUNCTIONS
    def get_name_by_id(self, _id):
        emp_name = self.acursor.execute('SELECT name FROM employee WHERE emp_id = ?', (_id,)).fetchone()
        if emp_name:
            return emp_name[0]
        else:
            return None

    def get_id_by_name(self, _name):
        emp_id = self.acursor.execute('SELECT emp_id FROM employee WHERE name = ?', (_name,)).fetchone()
        if emp_id:
            return emp_id[0]
        else:
            return None

    def get_time(self, time_type, _id, _date):
        """
        time_type: The column of time you wish to retrieve - clock_on/clock_off
        _id: emp_id
        _date: The date in the format %Y-%m-%d
        """

        sql = f'SELECT {time_type} FROM timestamp WHERE (emp_id = ? AND date = ?)'
        _time = self.acursor.execute(sql, (_id, _date)).fetchone()
        if _time:
            return _time[0]
        else:
            return None

    def get_last_clock_in_date(self, _id):
        latest_date = self.acursor.execute('SELECT MAX(date) FROM timestamp WHERE emp_id=?', (_id,)).fetchone()
        return latest_date[0]

    def get_num_of_emp(self):
        return len(self.acursor.execute('SELECT name FROM employee').fetchall())

    def get_all_emp(self):
        return [emp[0] for emp in self.acursor.execute('SELECT name FROM employee').fetchall() if emp[0]]

    def insert_new_employee(self, _name):
        self.acursor.execute('INSERT INTO employee (name) VALUES (?)', (_name, ))
        self.db.commit()

    def insert_time_record(self, time_type, _id: int, _date, time_value: str):
        # If record exists, raise insert error
        record_sql = self.acursor.execute('SELECT emp_id FROM timestamp WHERE (emp_id=? AND date=?)',
                                          (_id, _date)).fetchone()

        if record_sql:
            raise excep.RecordAlreadyExists(f'Record existing for employeeID: {_id} for this date: {_date}')
        else:
            self.acursor.execute(
                f'INSERT INTO timestamp ({time_type}, emp_id, date) VALUES (?,?,?)', (time_value, _id, _date))
            self.db.commit()

    # Update only if record exists.
    def update_time_record(self, time_type, _id: int, _date, time_value: str):
        # SQL TO CHECK IF RECORD EXISTS FOR SPECIFIC USER+DATE
        record_sql = self.acursor.execute('SELECT emp_id FROM timestamp WHERE (emp_id = ? AND date = ?)', (_id, _date)).fetchone()
        # RETURNS CLOCK ON/OFF VALUE FOR SPECIFIC USER+DATE
        if record_sql:
            self.acursor.execute(f'UPDATE timestamp SET {time_type} = ? WHERE (emp_id=? AND date=?)',
                                 (time_value, _id, _date))
            self.db.commit()
        else:
            raise excep.RecordNotFound(f'Record for employeeID: {_id} for this date: {_date} does not exist')

if __name__ == '__main__':
    database = Database('timesheet.db')

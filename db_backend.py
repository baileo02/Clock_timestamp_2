import mysql.connector as con
import exception_utility as excep
import os

class Database:
    def __init__(self):
        try:
            self.mydb = con.connect(
                host=os.getenv('db_host'),
                user=os.getenv('db_user'),
                password=os.getenv('db_pass'),
                database=os.getenv('database'))

            self.myCursor = self.mydb.cursor()
            self.create_tables()
        except con.errors.DatabaseError:
            print('Check host connection or credientials')

    # INITIALIZES THE DATABASE IF IT DOESN'T EXIST
    def create_tables(self):
        self.myCursor.execute(
            'CREATE TABLE IF NOT EXISTS employee (emp_id INT AUTO_INCREMENT UNIQUE PRIMARY KEY ,'
            ' name TEXT NOT NULL)')
        self.myCursor.execute(
            'CREATE TABLE IF NOT EXISTS timestamp (clock_on TEXT, clock_off TEXT, emp_id INTEGER NOT NULL,'
            ' date DATE, record_id INT PRIMARY KEY AUTO_INCREMENT UNIQUE)')
        self.mydb.commit()

    # INSERTS NEW EMPLOYEE WITH AUTO-INCREMENTED EMP_ID
    def insert_new_employee(self, _name):
        self.myCursor.execute("INSERT INTO employee (name) VALUES (%s)", (_name,))
        self.mydb.commit()

    # RETURN EMPLOYEE NAME GIVEN ID
    def get_name_by_id(self, _id):
        self.myCursor.execute('SELECT name FROM employee WHERE emp_id = %s', (_id,))
        emp_name = self.myCursor.fetchone()
        if emp_name:
            return emp_name[0]
        else:
            return None

    # GET EMPLOYEE ID GIVEN NAME
    def get_id_by_name(self, _name):
        self.myCursor.execute('SELECT emp_id FROM employee WHERE name = %s', (_name,))
        emp_id = self.myCursor.fetchone()
        if emp_id:
            return emp_id[0]
        else:
            return None

    # INSERTS TIME RECORD FOR CLOCK ON OR CLOCK OFF
    def insert_time_record(self, time_type, _id: int, _date, time_value: str):
        # If record exists, raise insert error
        self.myCursor.execute('SELECT emp_id FROM timestamp WHERE (emp_id = %s AND date = %s)',
                                          (_id, _date))
        record_sql = self.myCursor.fetchone()
        if record_sql:
            raise excep.RecordAlreadyExists(f'Record existing for employeeID: {_id} for this date: {_date}')
        else:
            self.myCursor.execute(
                f'INSERT INTO timestamp ({time_type}, emp_id, date) VALUES (%s, %s, %s)', (time_value, _id, _date))
            self.mydb.commit()

        # Update only if record exists.
    def update_time_record(self, time_type, _id: int, _date, time_value: str):
        # SQL TO CHECK IF RECORD EXISTS FOR SPECIFIC USER+DATE
        self.myCursor.execute('SELECT emp_id FROM timestamp WHERE (emp_id = %s AND date = %s)', (_id, _date))
        record_sql = self.myCursor.fetchone()
        # RETURNS CLOCK ON/OFF VALUE FOR SPECIFIC USER+DATE
        if record_sql:
            self.myCursor.execute(f'UPDATE timestamp SET {time_type} = %s WHERE (emp_id = %s AND date = %s)',
                                 (time_value, _id, _date))
            self.mydb.commit()
        else:
            raise excep.RecordNotFound(f'Record for employeeID: {_id} for this date: {_date} does not exist')

    # GET EMPLOYEE CLOCK ON OR OFF.
    def get_time(self, time_type, _id, _date):
        """
        time_type: The column of time you wish to retrieve - clock_on/clock_off
        _id: emp_id in the database column
        _date: The date in the format %Y-%m-%d
        """

        sql = f'SELECT {time_type} FROM timestamp WHERE (emp_id = %s AND date = %s)'
        self.myCursor.execute(sql, (_id, _date))
        _time = self.myCursor.fetchone()
        if _time:
            return _time[0]
        else:
            return None

    def get_all_emp(self):
        self.myCursor.execute('SELECT name FROM employee')
        return [row[0] for row in self.myCursor if row[0]]



if __name__ == '__main__':

    db = Database()

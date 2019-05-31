# Creating a pattern of Employee
class Employee(object):
    def __init__(self, userid, first_name, last_name, age, phone):
        self.userid = userid
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.phone = phone

    # function for user input
    def from_input():
        user_prompt = True
        while user_prompt:
            userid = input('userid ')
            if (len(userid) < 9) or (not userid.isdigit()):
                print("ID should include 9 digits (make sure not to type letters!)")
            else:
                user_prompt = False
        user_prompt = True
        while user_prompt:
            First_name = input('First_name: ')
            if (First_name == "") or (not First_name.isalpha()):
                print("Invalid data, make sure to type in a valid name")
            else:
                user_prompt = False
        user_prompt = True
        while user_prompt:
            Last_name = input("Last_name: ")
            if (Last_name == "") or (not Last_name.isalpha()):
                print("Invalid data, make sure to type in a valid name")
            else:
                user_prompt = False
        user_prompt = True
        while user_prompt:
            Age = input("Age: ")
            if (len(Age) != 2) or (not Age.isdigit()):
                    print("Invalid data, make sure to type in a valid Age")
            else:
                user_prompt = False
        user_prompt = True
        while user_prompt:
            Phone_number = input("Phone_Numbr: ")
            if (len(Phone_number) != 10) or (not Phone_number.isdigit()):
                print("Invalid data, make sure to type in a valid phone number (at least 10 digits number)")
            else:
                user_prompt = False
        return(str(userid),First_name,Last_name, Age, Phone_number )

    # representing instanced
    def __repr__(self):
        return " First Name : " + self.first_name + "\n Last Name: " + self.last_name + "\n ID number : " + str(
            self.ID) + "\n Age : " + str(self.age) + "\n Phone # : " + str(self.phone)

import csv
import sqlite3
import datetime

sql = sqlite3.connect('employees.db')
cur = sql.cursor()
UID_check = []
UID_delete_check = []

def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS employees_manually
               (Userid integer PRIMARY KEY,First_Name text,Last_Name text,Age integer,Phone_Number integer)""")
    sql.commit()
create_table()

def create_employee_manually():
    user_choice = input("Do you want to create a new record?(press 1 for yes or 2 for no): ")
    if user_choice == "1":
        user = Employee.from_input()
        cur.execute("INSERT INTO employees_manually VALUES (?,?,?,?,?)",
                    (user[0], user[1], user[2], user[3], user[4]))
        sql.commit()
    elif user_choice == "2":
        print ("Thank you, see you next time")
    else:
        print("oops, you must have typed invalid data. please try again")
create_employee_manually()
def load_from_file():
    f = open('emp_external.csv', 'r')
    next(f, None)  # skip header row
    reader = csv.reader(f)
    for row in reader:
        UID_check.append(row)
    for lst in UID_check:
        for i in lst:
            check_point = cur.execute("SELECT Userid FROM employees_manually").fetchall()
    if not (i[0]) in check_point:
        cur.execute("INSERT INTO employees_manually VALUES (?,?,?,?,?)", (row[0], row[1], row[2], row[3], row[4]))
    f.close()
    sql.commit()

def delete_employee_manually():
    delete_employee = input("Please enter userid: ")
    cur.execute('DELETE FROM employees_manually WHERE Userid=?', (delete_employee,))
    sql.commit()


def delete_employee_from_file():
    list = []
    f = open('delete_empl_external.csv', 'r')
    next(f, None)  # skip header row
    reader = csv.reader(f)
    for row in reader:
        UID_delete_check.append(row[0])
    print(UID_delete_check)
    check_point_delete = cur.execute("SELECT Userid FROM employees_manually").fetchall()
    for tuple in check_point_delete:
        for x in tuple:
            list.append(x)
    print(list)
    for i in UID_delete_check:
        if i in list:
            print("yes")
            query = 'DELETE FROM employees WHERE Userid IN({})'.format(",".join("?" * len(UID_delete_check)))
            cur.execute(query, UID_delete_check)
    f.close()
    sql.commit()

def alter_table():
    try:
        cur.execute('ALTER TABLE employees ADD COLUMN Time;')
    except:
        "duplicate column name"
    try:
        cur.execute('ALTER TABLE employees ADD COLUMN Year int;')
    except:
        "duplicate column name"
    try:
        cur.execute('ALTER TABLE employees ADD COLUMN Month;')
    except:
        "duplicate column name"
    try:
        cur.execute('ALTER TABLE employees ADD COLUMN Day;')
    except:
        "duplicate column name"
    try:
        cur.execute('ALTER TABLE employees ADD COLUMN Hour;')
    except:
        "duplicate column name"
    try:
        cur.execute('ALTER TABLE employees ADD COLUMN Minute;')
    except:
        "duplicate column name"
sql.commit()

def mark_attendance():
    list2 = []
    time = datetime.datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    empid = int(input("please enter your id number: "))
    check_point_attendance = cur.execute("SELECT Userid FROM employees_manually").fetchall()
    for tuple in check_point_attendance:
        for x in tuple:
            list2.append(x)
    print(list2)
    if empid in list2:
        existing = cur.execute("SELECT Year FROM employees_manually Where Userid=?", (empid,)).fetchone()
        if existing == (None,):
            cur.execute(
                "UPDATE employees SET Time = ?, Year = ?, Month = ?, Day = ?, Hour = ?, Minute = ? WHERE Userid = ?",
                (time, year, month, day, hour, minute, empid))
            sql.commit()
        else:
            cur.execute("INSERT INTO employees_manually(Userid,Year,Month,Day, Hour, Minute) VALUES (?, ?, ?, ?,?,?)",
                        (empid, year, month, day, hour, minute))
            sql.commit()

def create_attendance_report():
    UID = input("Please enter your id number: ")
    report = cur.execute("SELECT * FROM employees_manually Where Userid=?", (UID,)).fetchall()
    with open('attendance.csv', 'w') as f:
        for row in report:
            y = "".join(str(row) + "\n")
            f.write(y)

def monthly_attendance_report():
    Month = int(input("Please enter the required month number: "))
    with open('monthly_report.csv', 'w') as f:
        for row in cur.execute("SELECT * FROM employees_manually Where Month=?", (Month,)).fetchall():
            y = "".join(str(row) + "\n")
            f.write(y)

def late_employees_report():
    with open('late_employee_report.csv', 'w') as f:
        for row in cur.execute("SELECT * FROM employees_manually Where Hour>=11, Minute>30 ").fetchall():
            y = "".join(str(row) + "\n")
            f.write(y)

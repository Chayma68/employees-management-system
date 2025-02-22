import sqlite3


#Function for the connection to the dataBase
def connection():
    return sqlite3.connect("employees.db")


#Add Employee Function (CRUD)

def add_employee(name, department, salary, hire_date):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO employees(name, department, salary, hire_date)
        VALUES (?,?,?,?)
    ''', (name, department, salary, hire_date))
    conn.commit()
    conn.close()


#Function to retrieve All employees from the database

def get_employees():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM employees 
     ''')
    employees = cursor.fetchall()
    conn.close()
    return employees


#Funtion to edit employee

def edit_employee(employee_id, name, department, salary, hire_date):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE employees 
        SET name=?, department=?, salary=?, hire_date=? 
        WHERE id=? 
    ''', (name, department, salary, hire_date, employee_id))
    conn.commit()
    conn.close()


#Function to delete employee

def delete_employee(employee_id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    conn.commit()
    conn.close()


#Funtion to search employee by name
def search_employee(name):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE name LIKE ?", ('%' + name + '%',))
    employees = cursor.fetchall()
    conn.close()
    return employees


def search_user_email(email):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email LIKE ?", (email,))
    employees = cursor.fetchall()
    conn.close()
    return employees


def user_password(email):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def user_role_byemail(email):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

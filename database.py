import sqlite3

conn = sqlite3.connect("employees.db")
cursor = conn.cursor()
cursor.execute('''
  CREATE TABLE IF NOT EXISTS employees(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL, 
      department TEXT NOT NULL,
      salary REAL NOT NULL,
      hire_date TEXT NOT NULL,
      leave_balance INTEGER DEFAULT 30
      )             
                    
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK ( role IN ('admin', 'employee') NOT  NULL )
    )
    
''')
conn.commit()
conn.close()

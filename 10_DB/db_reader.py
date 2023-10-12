import pyodbc

# Querying using pyodbc
connection = pyodbc.connect("DRIVER={SQLite3 ODBC Driver};"
                            "DIRECT=True;"
                            "DATABASE=full_db.db;"
                            "String Types=Unicode")
cursor = connection.cursor()
# cursor.execute('SELECT * FROM news')
# cursor.execute('SELECT * FROM private_ad')
cursor.execute('SELECT * FROM personal_blog')
result = cursor.fetchall()

print(result)
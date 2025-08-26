import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="pallavidb"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM hello;")
rows = cursor.fetchall()

for row in rows:
    print(row)



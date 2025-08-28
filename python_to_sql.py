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


  # while True:
    #     q = input("Ask a question (or type 'exit'): ")
    #     if q.lower() == "exit":
    #         break

    #     sql = get_sql_from_llm(q,schema_text)
    #     print("Generated SQL:", sql)

    #     rows=run_query(sql)
    #     final_answer=natural_answer(q,rows)
    #     print("answer:",final_answer)

        # try:
        #     rows = run_query(sql)
        #     rows=natural_answer(question, rows)
        #     print("Answer:", rows)
        # except Exception as e:
        #     print("Error:", e)
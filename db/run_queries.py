import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

with open("sql/exploratory_queries.sql") as f:
    sql = f.read()

queries = sql.split(";")

for i, query in enumerate(queries):

    query = query.strip()

    if query:

        print("="*60)
        print("Query", i+1)
        print("="*60)

        rows = cursor.execute(query).fetchall()

        for row in rows:
            print(row)

conn.close()
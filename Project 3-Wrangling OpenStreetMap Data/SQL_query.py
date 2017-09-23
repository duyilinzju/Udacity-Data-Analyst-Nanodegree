import sqlite3
import pprint

conn = sqlite3.connect('mydb.db')

cursor = conn.cursor()

query = "SELECT value, COUNT(*) AS num FROM ways_tags WHERE key = 'building' GROUP BY value ORDER BY num DESC LIMIT 10"




cursor.execute(query)

results = cursor.fetchall()

pprint.pprint(results)

conn.close
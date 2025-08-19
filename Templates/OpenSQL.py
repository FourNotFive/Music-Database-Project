import sqlite3

import pandas as pd

# Connect to your database
conn = sqlite3.connect('music_database.db')

# Count unique songs
query = """
SELECT COUNT(DISTINCT song || ' - ' || performer) as unique_songs
FROM billboard_hot100;
"""

result = pd.read_sql_query(query, conn)
print(f"Unique songs: {result['unique_songs'].iloc[0]}")

conn.close()
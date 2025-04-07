import sqlite3

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# Inspect the current schema for the ragdoc table
schema_info = cursor.execute("PRAGMA table_info(ragdoc)").fetchall()
conn.close()

print("Table schema:", schema_info)

import sqlite3

conn = sqlite3.connect('music_database.db')
cursor = conn.cursor()

# Add a new search route for exploring chord patterns
print("Adding indexes for the new chord data...")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_basic_chords ON chordonomicon_data(basic_chords)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_genre ON chordonomicon_data(main_genre)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_decade ON chordonomicon_data(decade)")

conn.commit()
conn.close()

print("Indexes added! Now let's update the web app...")
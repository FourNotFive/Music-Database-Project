import sqlite3
import pandas as pd

def create_unique_songs_table():
    """
    Creates a unique_songs table with aggregated Billboard data
    Each song-artist combination gets one record with chart performance stats
    """
    
    # Connect to database
    conn = sqlite3.connect('music_database.db')
    cursor = conn.cursor()
    
    print("Creating unique_songs table...")
    
    # Drop existing table if it exists (for clean rebuild)
    cursor.execute("DROP TABLE IF EXISTS unique_songs;")
    
    # Create the unique songs table
    create_table_query = """
    CREATE TABLE unique_songs (
        song_id INTEGER PRIMARY KEY AUTOINCREMENT,
        song_title TEXT NOT NULL,
        artist TEXT NOT NULL,
        first_chart_date DATE,
        last_chart_date DATE,
        peak_position INTEGER,
        peak_date DATE,
        weeks_on_chart INTEGER,
        total_chart_entries INTEGER,
        UNIQUE(song_title, artist)
    );
    """
    
    cursor.execute(create_table_query)
    print("✓ Table structure created")
    
    # Populate with aggregated Billboard data
    print("Aggregating Billboard data...")
    
    # First, create a temporary view to get peak positions
    cursor.execute("""
    CREATE TEMP VIEW song_peaks AS
    SELECT 
        song,
        performer,
        MIN(chart_position) as peak_position
    FROM billboard_hot100
    GROUP BY song, performer;
    """)
    
    # Now insert the data with a simpler peak_date lookup
    insert_query = """
    INSERT INTO unique_songs 
    (song_title, artist, first_chart_date, last_chart_date, peak_position, peak_date, weeks_on_chart, total_chart_entries)
    SELECT 
        b.song as song_title,
        b.performer as artist,
        MIN(b.chart_date) as first_chart_date,
        MAX(b.chart_date) as last_chart_date,
        sp.peak_position,
        MIN(CASE WHEN b.chart_position = sp.peak_position THEN b.chart_date END) as peak_date,
        COUNT(DISTINCT b.chart_date) as weeks_on_chart,
        COUNT(*) as total_chart_entries
    FROM billboard_hot100 b
    JOIN song_peaks sp ON b.song = sp.song AND b.performer = sp.performer
    GROUP BY b.song, b.performer, sp.peak_position
    ORDER BY sp.peak_position ASC, COUNT(DISTINCT b.chart_date) DESC;
    """
    
    cursor.execute(insert_query)
    conn.commit()
    print("✓ Data inserted and aggregated")
    
    # Create indexes for better performance
    print("Creating indexes...")
    
    indexes = [
        "CREATE INDEX idx_unique_songs_artist ON unique_songs(artist);",
        "CREATE INDEX idx_unique_songs_title ON unique_songs(song_title);",
        "CREATE INDEX idx_unique_songs_peak ON unique_songs(peak_position);",
        "CREATE INDEX idx_unique_songs_date ON unique_songs(first_chart_date);"
    ]
    
    for index_query in indexes:
        cursor.execute(index_query)
    
    conn.commit()
    print("✓ Indexes created")
    
    # Verify results
    verification_queries = [
        "SELECT COUNT(*) as total_unique_songs FROM unique_songs;",
        "SELECT COUNT(*) as number_ones FROM unique_songs WHERE peak_position = 1;",
        "SELECT COUNT(*) as top_ten FROM unique_songs WHERE peak_position <= 10;",
        """SELECT song_title, artist, peak_position, weeks_on_chart 
           FROM unique_songs 
           ORDER BY weeks_on_chart DESC 
           LIMIT 5;"""
    ]
    
    print("\n=== VERIFICATION RESULTS ===")
    
    for i, query in enumerate(verification_queries):
        result = pd.read_sql_query(query, conn)
        
        if i == 0:
            print(f"Total unique songs: {result.iloc[0, 0]}")
        elif i == 1:
            print(f"Number 1 hits: {result.iloc[0, 0]}")
        elif i == 2:
            print(f"Top 10 hits: {result.iloc[0, 0]}")
        elif i == 3:
            print("\nLongest charting songs:")
            print(result.to_string(index=False))
    
    # Sample of the data
    sample_query = """
    SELECT song_title, artist, peak_position, peak_date, weeks_on_chart
    FROM unique_songs 
    WHERE peak_position = 1
    ORDER BY weeks_on_chart DESC 
    LIMIT 10;
    """
    
    sample = pd.read_sql_query(sample_query, conn)
    print("\nSample - Top #1 hits by weeks on chart:")
    print(sample.to_string(index=False))
    
    conn.close()
    print("\n✓ unique_songs table created successfully!")
    print(f"✓ Ready for linking with chord progressions and building song detail pages")

if __name__ == "__main__":
    create_unique_songs_table()
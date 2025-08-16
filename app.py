from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/patterns')
def chord_patterns():
    return render_template('chord_patterns.html')

@app.route('/search_patterns', methods=['POST'])
def search_patterns():
    pattern_type = request.form['pattern_type']
    
    conn = sqlite3.connect('music_database.db')
    
    if pattern_type == 'common':
        # Find most common chord progressions
        query = """
        SELECT basic_chords, COUNT(*) as count, main_genre, decade
        FROM chordonomicon_data 
        WHERE basic_chords IS NOT NULL
        GROUP BY basic_chords
        ORDER BY count DESC
        LIMIT 20
        """
        results = pd.read_sql_query(query, conn)
        
    elif pattern_type == 'genre':
        genre = request.form['genre']
        query = """
        SELECT basic_chords, main_genre, decade, COUNT(*) as count
        FROM chordonomicon_data 
        WHERE main_genre LIKE ? AND basic_chords IS NOT NULL
        GROUP BY basic_chords
        ORDER BY count DESC
        LIMIT 20
        """
        results = pd.read_sql_query(query, conn, params=[f'%{genre}%'])
    
    conn.close()
    
    return render_template('pattern_results.html', pattern_type=pattern_type, results=results)

@app.route('/search', methods=['POST'])
def search():
    search_type = request.form['search_type']
    
    conn = sqlite3.connect('music_database.db')
    
    if search_type == 'artist':
        search_term = request.form['search_term']
        query = """
        SELECT DISTINCT b.song, b.performer, b.peak_position, 
               (SELECT chart_date FROM billboard_hot100 b2 
                WHERE b2.song = b.song AND b2.performer = b.performer 
                AND b2.chart_position = b.peak_position LIMIT 1) as peak_date,
               COALESCE(m.chord_progression, c.chord_progression) as chord_progression,
               COALESCE(m.genre, 'Unknown') as genre,
               c.key_signature, c.nashville_notation,
               m.match_confidence
        FROM billboard_hot100 b 
        LEFT JOIN song_chords c ON b.song = c.song AND b.performer = c.performer
        LEFT JOIN matched_billboard_chords m ON b.song = m.billboard_song AND b.performer = m.billboard_performer
        WHERE b.performer LIKE ? 
        ORDER BY b.peak_position
        """
        results = pd.read_sql_query(query, conn, params=[f'%{search_term}%'])
        
    elif search_type == 'song':
        search_term = request.form['search_term']
        query = """
        SELECT DISTINCT b.song, b.performer, b.peak_position,
               (SELECT chart_date FROM billboard_hot100 b2 
                WHERE b2.song = b.song AND b2.performer = b.performer 
                AND b2.chart_position = b.peak_position LIMIT 1) as peak_date,
               COALESCE(m.chord_progression, c.chord_progression) as chord_progression,
               COALESCE(m.genre, 'Unknown') as genre,
               c.key_signature, c.nashville_notation,
               m.match_confidence
        FROM billboard_hot100 b
        LEFT JOIN song_chords c ON b.song = c.song AND b.performer = c.performer
        LEFT JOIN matched_billboard_chords m ON b.song = m.billboard_song AND b.performer = m.billboard_performer
        WHERE b.song LIKE ? 
        ORDER BY b.peak_position
        """
        results = pd.read_sql_query(query, conn, params=[f'%{search_term}%'])
        
    else:  # date search
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        search_term = f"{start_date} to {end_date}"
        query = """
        SELECT b.song, b.performer, b.chart_date, b.chart_position,
               COALESCE(m.chord_progression, c.chord_progression) as chord_progression,
               COALESCE(m.genre, 'Unknown') as genre,
               c.key_signature, c.nashville_notation,
               m.match_confidence
        FROM billboard_hot100 b
        LEFT JOIN song_chords c ON b.song = c.song AND b.performer = c.performer
        LEFT JOIN matched_billboard_chords m ON b.song = m.billboard_song AND b.performer = m.billboard_performer
        WHERE b.chart_date BETWEEN ? AND ? 
        ORDER BY b.chart_date, b.chart_position
        """
        results = pd.read_sql_query(query, conn, params=[start_date, end_date])
    
    conn.close()
    
    return render_template('search_results.html', search_type=search_type, search_term=search_term, results=results)

if __name__ == '__main__':
    app.run(debug=True)
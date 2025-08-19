import os
from pathlib import Path
import sqlite3

def examine_cocopops_files():
    """Examine actual CoCoPops chord files to understand their format"""
    
    cocopops_path = Path('CoCoPops-Billboard-legacy')
    
    if not cocopops_path.exists():
        print("CoCoPops-Billboard-legacy directory not found")
        return
    
    print("=== EXAMINING COCOPOPS CHORD FILES ===\n")
    
    # Find different types of files
    file_types = {}
    all_files = list(cocopops_path.rglob('*'))
    
    for file_path in all_files:
        if file_path.is_file() and file_path.stat().st_size > 0:
            ext = file_path.suffix.lower()
            if ext not in file_types:
                file_types[ext] = []
            file_types[ext].append(file_path)
    
    # Show what we found
    print("File types and counts:")
    for ext, files in sorted(file_types.items()):
        print(f"  {ext or '(no ext)'}: {len(files)} files")
    
    # Examine key file types that likely contain chord data
    key_extensions = ['.lab', '.txt', '.hum', '.krn', '.csv']
    
    for ext in key_extensions:
        if ext in file_types:
            print(f"\n=== EXAMINING {ext.upper()} FILES ===")
            
            # Look at first few files of this type
            for i, file_path in enumerate(file_types[ext][:3]):
                print(f"\nFile {i+1}: {file_path.name}")
                print(f"Path: {file_path.relative_to(cocopops_path)}")
                print(f"Size: {file_path.stat().st_size} bytes")
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    lines = content.split('\n')
                    print(f"Lines: {len(lines)}")
                    
                    # Show first 10 lines
                    print("Content preview:")
                    for j, line in enumerate(lines[:10]):
                        if line.strip():
                            print(f"  {j+1:2d}: {line[:80]}")
                    
                    if len(lines) > 10:
                        print(f"  ... ({len(lines)-10} more lines)")
                        
                except Exception as e:
                    print(f"Error reading file: {e}")
                
                print("-" * 60)

def examine_database_chord_content():
    """Look at what we currently have in the database"""
    
    conn = sqlite3.connect('music_database.db')
    cursor = conn.cursor()
    
    print("\n=== CURRENT DATABASE CONTENT ===\n")
    
    # Check mcgill_chord_data content
    print("McGill chord data samples:")
    cursor.execute("""
        SELECT artist, song_title, 
               SUBSTR(chord_progression, 1, 200) as chord_preview,
               file_type
        FROM mcgill_chord_data 
        WHERE chord_progression IS NOT NULL 
        AND LENGTH(chord_progression) > 10
        LIMIT 5
    """)
    
    results = cursor.fetchall()
    for i, (artist, title, chords, file_type) in enumerate(results, 1):
        print(f"\n{i}. {artist} - {title} ({file_type})")
        print(f"   Chords: {chords}")
    
    print("\n" + "="*60)
    
    # Check cocopops_chord_data content  
    print("CoCoPops chord data samples:")
    cursor.execute("""
        SELECT song_title, artist,
               SUBSTR(full_content, 1, 300) as content_previewpython check_chord_data.py
        FROM cocopops_chord_data
        WHERE song_title != 'Unknown'
        LIMIT 5
    """)
    
    results = cursor.fetchall()
    for i, (title, artist, content) in enumerate(results, 1):
        print(f"\n{i}. {artist} - {title}")
        print(f"   Content: {content[:200]}...")
    
    conn.close()

if __name__ == "__main__":
    examine_cocopops_files()
    examine_database_chord_content()
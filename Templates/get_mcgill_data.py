import sqlite3
import pandas as pd
import os
import zipfile
from pathlib import Path

def setup_mcgill_data():
    """
    Helper script to integrate CoCoPops-Billboard chord data
    Focuses on the GitHub CoCoPops dataset
    """
    
    print("CoCoPops-Billboard Dataset Integration")
    print("=" * 40)
    
    # Check for CoCoPops directory
    cocopops_path = Path('CoCoPops-Billboard-legacy')
    
    if not cocopops_path.exists():
        print("❌ CoCoPops-Billboard-legacy directory not found")
        print("\n🎯 TO GET THE DATA:")
        print("Option A - Git Clone:")
        print("  git clone https://github.com/Computational-Cognitive-Musicology-Lab/CoCoPops-Billboard-legacy")
        print("\nOption B - Download ZIP:")
        print("  1. Go to: https://github.com/Computational-Cognitive-Musicology-Lab/CoCoPops-Billboard-legacy")
        print("  2. Click 'Code' → 'Download ZIP'")
        print("  3. Extract here as 'CoCoPops-Billboard-legacy'")
        print("  4. Run this script again")
        return False
    
    print("✓ Found CoCoPops-Billboard-legacy directory")
    
    # Explore the directory structure
    print("\n📁 Directory contents:")
    for item in cocopops_path.iterdir():
        if item.is_dir():
            print(f"  📂 {item.name}/")
        else:
            print(f"  📄 {item.name}")
    
    return process_cocopops_data(cocopops_path)

def load_with_mirdata():
    """Load McGill Billboard data using mirdata library"""
    try:
        import mirdata
        
        # Initialize the billboard dataset
        dataset = mirdata.initialize('billboard')
        print(f"Dataset info: {dataset}")
        
        # Load the dataset (this might download it automatically)
        # Note: mirdata might require additional setup
        
        print("✓ mirdata approach needs additional configuration")
        print("Continuing with manual download approach...")
        return False
        
    except Exception as e:
        print(f"❌ mirdata approach failed: {e}")
        return False

def process_kaggle_zip(zip_filename):
    """Process downloaded Kaggle ZIP file"""
    print(f"Processing Kaggle ZIP: {zip_filename}")
    
    # Extract ZIP
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall('mcgill_data')
    
    # Look for the chord files
    mcgill_path = Path('mcgill_data')
    chord_files = list(mcgill_path.glob('**/*.txt')) + list(mcgill_path.glob('**/*.csv'))
    
    print(f"Found {len(chord_files)} potential chord files")
    for file in chord_files[:5]:  # Show first 5
        print(f"  📄 {file}")
    
    return process_chord_files(chord_files)

def process_cocopops_data(cocopops_path):
    """Process CoCoPops GitHub data and analyze structure"""
    
    print(f"\n🔍 Analyzing CoCoPops data structure...")
    
    # Look for different types of files
    all_files = list(cocopops_path.rglob('*'))
    
    file_types = {}
    for file_path in all_files:
        if file_path.is_file():
            ext = file_path.suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
    
    print("File types found:")
    for ext, count in sorted(file_types.items()):
        print(f"  {ext or '(no extension)'}: {count} files")
    
    # Look for chord annotation files
    potential_chord_files = []
    potential_metadata_files = []
    
    for file_path in all_files:
        if file_path.is_file():
            name_lower = file_path.name.lower()
            
            # Common patterns for chord files
            if any(pattern in name_lower for pattern in ['chord', '.txt', '.lab', '.csv']):
                if file_path.stat().st_size > 0:  # Non-empty files
                    potential_chord_files.append(file_path)
            
            # Look for metadata files
            if any(pattern in name_lower for pattern in ['meta', 'index', 'list', 'catalog']):
                potential_metadata_files.append(file_path)
    
    print(f"\n📊 Found {len(potential_chord_files)} potential chord files")
    print(f"📊 Found {len(potential_metadata_files)} potential metadata files")
    
    # Sample some files to understand format
    print("\n🔍 SAMPLING FILES:")
    
    # Look at metadata first
    if potential_metadata_files:
        print("\nMetadata files:")
        for meta_file in potential_metadata_files[:3]:
            print(f"  📄 {meta_file.relative_to(cocopops_path)}")
            try:
                with open(meta_file, 'r', encoding='utf-8', errors='ignore') as f:
                    sample_content = f.read(200)  # First 200 characters
                    print(f"    Preview: {sample_content[:100]}...")
            except Exception as e:
                print(f"    Error reading: {e}")
    
    # Look at chord files
    if potential_chord_files:
        print("\nChord annotation files:")
        for chord_file in potential_chord_files[:5]:
            print(f"  📄 {chord_file.relative_to(cocopops_path)} ({chord_file.stat().st_size} bytes)")
            try:
                with open(chord_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()[:10]  # First 10 lines
                    print(f"    Lines: {len(lines)}")
                    for i, line in enumerate(lines[:3]):
                        print(f"    L{i+1}: {line.strip()}")
                    if len(lines) > 3:
                        print(f"    ... ({len(lines)-3} more lines)")
            except Exception as e:
                print(f"    Error reading: {e}")
            print()
    
    # Now try to create the database
    return create_cocopops_database(cocopops_path, potential_chord_files, potential_metadata_files)

def create_cocopops_database(cocopops_path, chord_files, metadata_files):
    """Create database table from CoCoPops data"""
    
    print("\n📊 CREATING COCOPOPS DATABASE TABLE...")
    
    # Connect to database
    conn = sqlite3.connect('music_database.db')
    cursor = conn.cursor()
    
    # Create CoCoPops chord table
    cursor.execute("DROP TABLE IF EXISTS cocopops_chord_data;")
    
    create_table = """
    CREATE TABLE cocopops_chord_data (
        cocopops_id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT,
        song_title TEXT,
        artist TEXT,
        year TEXT,
        chart_info TEXT,
        chord_progression TEXT,
        full_content TEXT,
        file_size INTEGER,
        data_source TEXT DEFAULT 'cocopops_billboard'
    );
    """
    
    cursor.execute(create_table)
    print("✓ Created cocopops_chord_data table")
    
    processed_count = 0
    
    # Process chord files
    for chord_file in chord_files[:50]:  # Start with first 50 files
        try:
            with open(chord_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Basic parsing - extract what we can
            file_name = chord_file.name
            relative_path = str(chord_file.relative_to(cocopops_path))
            file_size = chord_file.stat().st_size
            
            # Try to extract song info from filename or content
            song_title = "Unknown"
            artist = "Unknown"
            year = "Unknown"
            
            # Simple filename parsing (adapt based on actual format)
            if "_" in file_name:
                parts = file_name.replace('.txt', '').replace('.lab', '').split('_')
                if len(parts) >= 2:
                    artist = parts[0].replace('-', ' ').title()
                    song_title = parts[1].replace('-', ' ').title()
            
            # Insert into database
            cursor.execute("""
                INSERT INTO cocopops_chord_data 
                (file_path, song_title, artist, year, chord_progression, full_content, file_size)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                relative_path,
                song_title,
                artist,
                year,
                content[:500],  # First 500 chars as chord progression sample
                content,        # Full content for later analysis
                file_size
            ))
            
            processed_count += 1
            
            if processed_count % 10 == 0:
                print(f"  ✓ Processed {processed_count} files...")
                
        except Exception as e:
            print(f"❌ Error processing {chord_file.name}: {e}")
            continue
    
    conn.commit()
    
    # Show results
    result = pd.read_sql_query("SELECT COUNT(*) as count FROM cocopops_chord_data", conn)
    print(f"\n✅ PROCESSED {result.iloc[0, 0]} CHORD FILES")
    
    # Sample data analysis
    sample_query = """
    SELECT song_title, artist, file_path, 
           SUBSTR(chord_progression, 1, 100) as chord_sample,
           file_size
    FROM cocopops_chord_data 
    ORDER BY file_size DESC
    LIMIT 10
    """
    
    sample = pd.read_sql_query(sample_query, conn)
    print("\n📊 SAMPLE DATA (largest files):")
    print(sample.to_string(index=False))
    
    # File size distribution
    sizes_query = """
    SELECT 
        COUNT(*) as total_files,
        AVG(file_size) as avg_size,
        MIN(file_size) as min_size,
        MAX(file_size) as max_size
    FROM cocopops_chord_data
    """
    
    sizes = pd.read_sql_query(sizes_query, conn)
    print(f"\n📏 FILE STATISTICS:")
    print(f"Total files: {sizes.iloc[0, 0]}")
    print(f"Average size: {sizes.iloc[0, 1]:.1f} bytes")
    print(f"Size range: {sizes.iloc[0, 2]} - {sizes.iloc[0, 3]} bytes")
    
    conn.close()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Examine the actual chord file formats")
    print("2. Parse song titles and artists more accurately") 
    print("3. Extract proper chord progressions")
    print("4. Link to your Billboard unique_songs table")
    print("5. Build accurate chord database!")
    
    return True

if __name__ == "__main__":
    setup_mcgill_data()
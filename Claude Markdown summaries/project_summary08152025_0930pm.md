# Music Database Project Summary

## Project Overview
A comprehensive music database web application that combines Billboard Hot 100 chart data with chord progression analysis. The system allows users to search through 349,000+ Billboard records and explore 679,000+ chord progressions, with intelligent linking between chart performance and musical theory data.

## 🚀 GitHub Repository
**Live on GitHub**: https://github.com/FourNotFive/Music-Database-Project

## Current Status: ✅ FULLY FUNCTIONAL
- **Billboard Search**: Artist, song, and date range searches with peak positions
- **Chord Pattern Explorer**: Analysis of 679k+ songs from CHORDONOMICON dataset
- **Linked Data**: Billboard songs now show associated chord progressions
- **Web Interface**: Flask-based with navigation between search modes
- **Version Control**: Complete project backed up on GitHub

## Project Structure
```
Music-Database-Project/
├── app.py                           # Main Flask application
├── Templates/                       # HTML templates
│   ├── Index.html                   # Main search interface
│   ├── search_results.html          # Billboard search results
│   ├── Chord_patterns.html          # Chord pattern explorer
│   └── Pattern_results.html         # Chord pattern results
├── Create_database.py               # Database creation script
├── add_indexes.py                   # Database optimization
├── import_chordonomicon.py          # Chord data import
├── link_billboard_chords.py         # Links Billboard + chord data
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── .gitignore                       # Git ignore rules
└── [various utility scripts]

# Local files (not on GitHub due to size):
├── music_database.db                # SQLite database (92MB)
├── Hot 100.csv                      # Original Billboard dataset (54MB)  
└── archive/chordonomicon.csv        # Chord dataset (225MB)
```

## Database Schema

### Tables:
1. **billboard_hot100** (349,388 records)
   - song, performer, chart_date, chart_position, peak_position
   - Indexed for fast searching

2. **song_chords** (manual chord data)
   - song, performer, key_signature, chord_progression, nashville_notation

3. **chordonomicon_data** (679,807 records)
   - chords, basic_chords, release_date, genres, decade, main_genre
   - From CHORDONOMICON research dataset

4. **matched_billboard_chords** (linked data)
   - billboard_song, billboard_performer, chord_progression, genre, match_confidence
   - Links Billboard hits with chord progressions

## Key Features Implemented

### 1. Billboard Search
- **Artist Search**: Find all songs by specific artists with peak positions
- **Song Search**: Search for specific song titles across all performers  
- **Date Range Search**: Find all charting songs within date ranges
- **Results show**: Peak position, peak date, and chord progressions (when available)

### 2. Chord Pattern Explorer
- **Common Progressions**: Most frequently used chord progressions across all 679k songs
- **Genre Analysis**: Characteristic chord patterns by musical genre (pop, rock, metal, jazz, blues, country, folk, hip hop, electronic)
- **Statistical Analysis**: Shows usage count and genre/decade distribution

### 3. Intelligent Data Linking
- **High Confidence Matches**: Manually verified chord progressions for popular songs (Beatles, Elvis, etc.)
- **Estimated Matches**: Algorithm-based chord progression estimates using genre/era heuristics
- **Confidence Indicators**: Visual coding (green=verified, yellow=estimated, blue=no data)

### 4. Web Interface
- **Navigation**: Seamless switching between Billboard search and chord analysis
- **Responsive Design**: Clean, modern interface with hover effects
- **Results Formatting**: Color-coded results with confidence indicators
- **Search Options**: Multiple search types with dynamic form elements

## Technical Implementation

### Backend (Python/Flask)
- **Flask**: Web framework with route handling
- **SQLite**: Database with optimized indexes
- **Pandas**: Data processing and analysis
- **SQL Queries**: Complex joins between Billboard and chord data

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Modern CSS with gradients and hover effects
- **Dynamic Forms**: JavaScript for search type switching
- **Visual Indicators**: Color-coded confidence levels
- **Navigation**: Intuitive user interface

### Data Processing
- **CHORDONOMICON Integration**: 666k song chord progression dataset
- **String Matching**: Song title and artist name normalization
- **Pattern Extraction**: Chord progression simplification and analysis
- **Genre Classification**: Automated genre assignment based on patterns

### Version Control
- **Git**: Local version control with GitHub remote
- **Repository**: Public repository with clean commit history
- **File Management**: Large data files excluded from GitHub, scripts provided for rebuilding

## Current Capabilities

### Search Examples:
- Search "Beatles" → See "Let It Be", "Hey Jude", etc. with chord progressions
- Search "Elvis" → See "Hound Dog", "Love Me Tender" with musical data
- Date search "1965-01-01" to "1965-12-31" → All 1965 hits with available chords
- Chord patterns → Find most common progressions like "C Am F G" (I-vi-IV-V)

### Data Quality:
- **High confidence**: Manual matches for major artists (Beatles, Elvis, etc.)
- **Medium confidence**: Genre-based estimates for 1960s-2000s hits
- **Coverage**: Chord data available for subset of Billboard songs with expansion potential

## Setup Instructions

### For New Users:
1. **Clone repository**:
   ```bash
   git clone https://github.com/FourNotFive/Music-Database-Project.git
   cd Music-Database-Project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create database** (large files not included in repo):
   ```bash
   python Create_database.py      # Creates Billboard database
   python import_chordonomicon.py # Imports chord data  
   python add_indexes.py          # Optimizes performance
   python link_billboard_chords.py # Links datasets
   ```

4. **Run application**:
   ```bash
   python app.py
   ```

5. **Open browser**: http://127.0.0.1:5000

### For Project Owner (Continuing Development):
- **Database files already exist locally** (music_database.db, etc.)
- **Just run**: `python app.py` to start
- **For updates**: Use git add/commit/push workflow

## Next Development Opportunities

### 1. Guitar Chord Diagrams
- Generate visual chord diagrams for progressions
- Show finger positions and fretboard patterns
- Integration with chord progression display

### 2. Music Theory Analysis
- Nashville notation converter (Roman numeral analysis)
- Key transposition tools
- Circle of fifths integration
- Chord function analysis (tonic, dominant, subdominant)

### 3. Enhanced Data Linking
- **Spotify API**: Get audio features and additional metadata
- **MusicBrainz**: Improve artist/song matching accuracy
- **Hooktheory API**: Professional chord progression database
- **Last.fm**: User listening data and tags

### 4. Advanced Search Features
- Find Billboard songs by chord progression
- Genre-based filtering of search results
- Decade-based analysis tools
- Similar chord progression finder

### 5. Data Visualization
- Chart position over time graphs
- Chord progression popularity trends
- Genre evolution analysis
- Interactive music theory visualizations

### 6. Export/Sharing Features
- Export search results to CSV
- Generate chord sheets
- Share search URLs
- Save favorite progressions

## Dependencies
```python
flask==3.1.1
pandas==2.3.1
datasets==4.0.0
requests==2.32.4
# (See requirements.txt for complete list)
```

## Installation Notes
- **Python 3.x required**
- **All dependencies installed via pip**
- **Database files must be rebuilt locally** (scripts provided)
- **Git and GitHub setup complete**

## Performance
- **Database Size**: ~200MB with all data (local only)
- **Repository Size**: ~35MB (code and templates only)
- **Query Speed**: Sub-second search with proper indexes
- **Memory Usage**: Efficient pandas operations
- **Web Performance**: Fast page loads with cached queries

## File Management
- **On GitHub**: Source code, templates, documentation, setup scripts
- **Local Only**: Large data files (database, CSV files)
- **Rebuild Process**: Automated scripts recreate full database from source data
- **Git Workflow**: Standard add/commit/push for code changes

## Project Links
- **GitHub Repository**: https://github.com/FourNotFive/Music-Database-Project
- **Live Application**: http://127.0.0.1:5000 (when running locally)
- **Documentation**: README.md in repository

This project successfully combines music industry data (Billboard charts) with music theory analysis (chord progressions) in an interactive web application. The foundation is solid for expanding into advanced music analysis tools, and the complete codebase is now safely backed up and shareable on GitHub.

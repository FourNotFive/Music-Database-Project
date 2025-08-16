import pandas as pd
import sqlite3

print("Let's try the Hugging Face dataset...")

# Try to install datasets library first
try:
    from datasets import load_dataset
    print("Loading CHORDONOMICON from Hugging Face...")
    
    # Load the dataset
    dataset = load_dataset("ailsntua/Chordonomicon")
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(dataset['train'])
    
    print(f"Dataset loaded! Contains {len(df)} songs")
    print("\nFirst few rows:")
    print(df.head())
    print("\nColumn names:")
    print(df.columns.tolist())
    
except ImportError:
    print("Need to install datasets library.")
    print("Run: python -m pip install datasets")
except Exception as e:
    print(f"Error loading from Hugging Face: {e}")
    print("Let's download from Kaggle instead...")
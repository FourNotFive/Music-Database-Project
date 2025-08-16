import pandas as pd

df = pd.read_csv(r'C:\Users\Arjan\Desktop\Music_Project\Hot 100.csv')

# Find Elvis entries
elvis = df[df['performer'].str.contains('Elvis', case=False, na=False)]

print(f"Elvis entries found: {len(elvis)}")
print("\nFirst few Elvis songs:")
print(elvis[['song', 'performer', 'chart_date', 'peak_position']].head(10))
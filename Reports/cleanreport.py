import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load CSV
file_path = "/Users/jainam/Downloads/Class_Fall_25/FDS/RentVisionNYC/Airbnb_Dataset/rawdata/Airbnb_Open_Data.csv"
df = pd.read_csv(file_path, low_memory=False)

# Work on a copy to avoid modifying original
df_clean = df.copy()

# Clean 'price' column
df_clean['price'] = df_clean['price'].replace(r'[\$,]', '', regex=True)
df_clean['price'] = pd.to_numeric(df_clean['price'], errors='coerce')

# -------------------------------
# 1. Listings per Borough
# -------------------------------
plt.figure(figsize=(8,5))
sns.countplot(
    data=df_clean.dropna(subset=['neighbourhood group']),
    x='neighbourhood group',
    order=df_clean['neighbourhood group'].value_counts().index
)
plt.title('Airbnb Listings by Borough')
plt.xlabel('Borough')
plt.ylabel('Number of Listings')
plt.tight_layout()
plt.show()

# -------------------------------
# 2. Top 20 Neighborhoods by Listings
# -------------------------------
top_neigh = df_clean['neighbourhood'].value_counts().head(20).reset_index()
top_neigh.columns = ['neighbourhood', 'count']

plt.figure(figsize=(12,6))
sns.barplot(data=top_neigh, y='neighbourhood', x='count', palette='viridis')
plt.title('Top 20 NYC Neighborhoods by Airbnb Listings')
plt.xlabel('Number of Listings')
plt.ylabel('Neighborhood')
plt.tight_layout()
plt.show()

# -------------------------------
# 3. Room Type Distribution
# -------------------------------
plt.figure(figsize=(8,5))
sns.countplot(
    data=df_clean.dropna(subset=['room type']),
    x='room type',
    order=df_clean['room type'].value_counts().index
)
plt.title('Airbnb Listings by Room Type')
plt.xlabel('Room Type')
plt.ylabel('Number of Listings')
plt.tight_layout()
plt.show()

# -------------------------------
# 4. Price Distribution
# -------------------------------
df_filtered = df_clean[df_clean['price'] < 2000].copy()  # filter unrealistic prices

plt.figure(figsize=(10,5))
sns.histplot(df_filtered['price'].dropna(), bins=50, kde=True, color='skyblue')
plt.title('Distribution of Airbnb Prices in NYC')
plt.xlabel('Price ($)')
plt.ylabel('Number of Listings')
plt.tight_layout()
plt.show()

# -------------------------------
# 5. Listings vs Average Price by Neighborhood
# -------------------------------
neigh_stats = df_filtered.groupby('neighbourhood').agg({
    'price':'mean',
    'id':'count'
}).reset_index().rename(columns={'id':'listing_count'})

plt.figure(figsize=(10,6))
sns.scatterplot(data=neigh_stats, x='listing_count', y='price', alpha=0.7)
plt.title('Listings vs Average Price by Neighborhood')
plt.xlabel('Number of Listings')
plt.ylabel('Average Price ($)')
plt.tight_layout()
plt.show()

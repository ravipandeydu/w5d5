# db/populate_data.py

import sqlite3
import pandas as pd
import os
import re
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
DB_FILE = os.getenv("DB_FILE_PATH", "quick_commerce.db")

PLATFORM_FILES = {
    # "Blinkit": "data/blinkit_data.csv",
    "Zepto": "data/zepto_data.csv",
    # "Instamart": "data/instamart_data.csv"
}

# ** THE FIX IS HERE **
# Updated mapping to match your actual CSV column names.
COLUMN_MAPPINGS = {
    'product_name': 'name',
    'category': 'Category',
    'price': 'discountedSellingPrice',
    'unit': 'quantity'
    # 'brand' is removed as it's not in your column list.
}

# --- Data Cleaning Function ---
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Performs cleaning operations on the raw DataFrame."""
    print("    - Starting cleaning...")

    # 1. Standardize column names to lowercase for easier access
    df.columns = [col.lower().strip() for col in df.columns]

    # Remap our user-friendly names to the new lowercase names
    mapped_cols = {k: v.lower().strip() for k, v in COLUMN_MAPPINGS.items()}
    
    # 2. Handle Missing Values
    # Drop rows where essential information like product name or price is missing
    df.dropna(subset=[mapped_cols['product_name'], mapped_cols['price']], inplace=True)
    if mapped_cols.get('category') in df.columns:
        df[mapped_cols['category']].fillna('Uncategorized', inplace=True)

    # 3. Clean and Standardize Text Data
    for col_key in ['product_name', 'category']:
        col_name = mapped_cols.get(col_key)
        if col_name and col_name in df.columns:
            df[col_name] = df[col_name].astype(str).str.lower().str.strip()

    # 4. Clean and Convert Price Column
    price_col = mapped_cols['price']
    df[price_col] = df[price_col].apply(lambda x: re.sub(r'[^\d.]', '', str(x)))
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    df.dropna(subset=[price_col], inplace=True)

    # 5. Remove Duplicates
    df.drop_duplicates(subset=[mapped_cols['product_name']], keep='first', inplace=True)
    
    print(f"    - Cleaning complete. Found {len(df)} valid records.")
    return df, mapped_cols


# --- Database Setup (same as before) ---
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
with open('db/schema.sql', 'r') as f:
    cur.executescript(f.read())
print("✅ Database schema created.")

# --- Data Loading Logic ---
category_cache = {}
product_cache = {}
platform_ids = {}

def get_or_create_id(cursor, cache, table, column, value):
    if not value or pd.isna(value): return None
    if value in cache: return cache[value]
    cursor.execute(f"SELECT {column}_id FROM {table} WHERE name = ?", (value,))
    result = cursor.fetchone()
    if result:
        id = result[0]
    else:
        cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (value,))
        id = cursor.lastrowid
    cache[value] = id
    return id

try:
    for name in PLATFORM_FILES.keys():
        cur.execute("INSERT INTO platforms (name) VALUES (?)", (name,))
        platform_ids[name] = cur.lastrowid
    print(f"✅ Platforms inserted: {list(platform_ids.keys())}")

    for platform_name, file_path in PLATFORM_FILES.items():
        if not os.path.exists(file_path):
            print(f"⚠️ WARNING: File not found at '{file_path}'. Skipping.")
            continue

        platform_id = platform_ids[platform_name]
        raw_df = pd.read_csv(file_path, encoding='latin1')
        print(f"\n🔄 Processing {file_path}...")
        
        cleaned_df, mapped_cols = clean_dataframe(raw_df)

        for _, row in cleaned_df.iterrows():
            product_name = row.get(mapped_cols['product_name'])
            category_name = row.get(mapped_cols['category'])
            price = row.get(mapped_cols['price'])
            unit = row.get(mapped_cols['unit'])

            category_id = get_or_create_id(cur, category_cache, 'categories', 'category', category_name)
            product_id = get_or_create_id(cur, product_cache, 'products', 'product', product_name)
            
            cur.execute(
                "INSERT INTO product_listings (product_id, platform_id, current_price, unit) VALUES (?, ?, ?, ?)",
                (product_id, platform_id, price, str(unit))
            )

    conn.commit()
    print("\n🎉 All cleaned data loaded successfully!")

except KeyError as e:
    print(f"❌ A KeyError occurred! This means a column in your mapping was not found in the CSV. Missing column: {e}")
except Exception as e:
    conn.rollback()
    print(f"❌ An error occurred: {e}")

finally:
    cur.close()
    conn.close()
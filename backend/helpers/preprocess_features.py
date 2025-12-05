import os
import ast
import gc
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler

script_dir = os.path.dirname(os.path.abspath(__file__))
movies_path = os.path.join(script_dir, "..", "data", "movies.csv")
preprocessed_movies_path = os.path.join(script_dir, "..", "data", "preprocessed_movies.csv")

def efficient_multi_hot_encode(df: pd.DataFrame, col: str, k: int) -> pd.DataFrame:
    """
    Applies Multi-Hot Encoding, retaining only the Top K most frequent items,
    and converts the resulting DataFrame to a sparse format for memory efficiency.
    """
    print(f"  -> Processing '{col}' with Top K={k} filter...")
    
    # 1. Identify Top K most frequent items
    # df[col].explode() expands the list column into individual rows
    item_counts = df[col].explode().value_counts()
    top_k_items = set(item_counts.head(k).index)
    
    # 2. Filter the lists in the DataFrame to only keep Top K items
    # Items not in the Top K set are discarded.
    df[col] = df[col].apply(lambda x: [item for item in x if item in top_k_items])
    
    # 3. Perform Multi-Hot Encoding
    mlb = MultiLabelBinarizer()
    encoded_data = mlb.fit_transform(df[col]) 
    
    # 4. Create DataFrame and convert to Sparse Data Type (Crucial for memory)
    encoded_df = pd.DataFrame(
        encoded_data, 
        columns=[f"{col}_{c}" for c in mlb.classes_]
    ).astype(pd.SparseDtype("uint8", 0))

    # 5. Concatenate
    df = pd.concat([df.drop(columns=[col]), encoded_df], axis=1)
    
    del encoded_data, encoded_df, item_counts, top_k_items # Cleanup
    gc.collect()
    
    return df

def preprocess_movie_dataset(input_path: str, output_path: str) -> None:
    """
    Reads the initial movies CSV, processes all features, and saves the final CSV.
    Uses explicit memory cleanup (del and gc.collect) to try and prevent OOM errors.
    """
    print("Starting feature numerization and scaling for movie dataset...")
    df = pd.read_csv(input_path)
    
    # Drop irrelevant columns and reset index
    df.drop(columns=["original_title", "poster_url", "Unnamed: 0"], inplace=True, errors='ignore')
    df.reset_index(drop=True, inplace=True)

    # This reduces the base memory footprint of the main DataFrame
    for col in ["release_year", "runtime_seconds"]:
         df[col] = pd.to_numeric(df[col], errors='coerce').astype(np.float32)
    

    # --- A. Multi-Hot Encoding for List Features (MODIFIED FOR EFFICIENCY) ---
    list_cols_k = {
        "genres": 50,      # Typically low cardinality, but cap it just in case
        "directors": 500,  # Focus on most influential/frequent directors
        "writers": 500,    # Focus on most frequent writers
        "actors": 1000,    # Large potential size, cap at 1,000 top actors
        "companies": 500   # Focus on major production companies
    }
    
    # Prepare list columns outside the loop
    for col in list_cols_k:
        df[col] = df[col].fillna('[]').apply(ast.literal_eval)

    for col, k in list_cols_k.items():
        # Use the memory-efficient function
        df = efficient_multi_hot_encode(df, col, k)
        
    print("Multi-Hot Encoding complete using Top K filter and Sparse Data.")
    

    # --- B. One-Hot Encoding for Categorical Feature ---
    df['certificate_rating'] = df['certificate_rating'].fillna('Unknown')
    # Set sparse=True to use SparseDtype, saving memory
    df = pd.get_dummies(df, columns=['certificate_rating'], prefix='cert', sparse=True)


    # --- C. TF-IDF Vectorization for Text Feature ---
    # Use direct assignment to avoid FutureWarning/chained assignment
    df['plot'] = df['plot'].fillna('')
    
    tfidf = TfidfVectorizer(stop_words='english', min_df=50, max_features=2000)
    tfidf_matrix = tfidf.fit_transform(df['plot'])

    # This keeps the resulting DataFrame columns sparse and memory-efficient.
    tfidf_df = pd.DataFrame.sparse.from_spmatrix(tfidf_matrix, columns=tfidf.get_feature_names_out())
    tfidf_df.columns = [f"plot_tfidf_{col}" for col in tfidf_df.columns]
    
    df = df.drop(columns=['plot']).reset_index(drop=True)
    tfidf_df = tfidf_df.reset_index(drop=True)
    df = pd.concat([df, tfidf_df], axis=1)
    
    # Cleanup
    del tfidf_matrix, tfidf_df
    gc.collect()


    # --- D. Scaling Numeric Features ---
    numeric_cols = ["release_year", "runtime_seconds"]
    
    for col in numeric_cols:
         df[col] = pd.to_numeric(df[col], errors='coerce')
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    
    # --- E. Save Final Numerized Dataset ---
    df.to_csv(output_path, index=False)
    print(f"Numerized and processed dataset saved to: {output_path}")

if __name__ == "__main__":
    preprocess_movie_dataset(input_path=movies_path, output_path=preprocessed_movies_path)
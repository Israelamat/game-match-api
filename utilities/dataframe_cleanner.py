import pandas as pd

def _drop_invalid_name_genres_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with null values in 'Name' and 'Genres' columns."""
    df = df.dropna(subset=['Name', 'Genres'])
    df = df[df['Name'].str.strip() != ""]
    df = df[df['Genres'].str.strip() != ""]
    return df

def _fill_text_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Fill null values in text columns with empty strings."""
    text_cols = ['About the game', 'Tags', 'Detailed description', 'Reviews']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")
    return df

def _fill_numeric_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Fill null values in numeric columns with 0."""
    numeric_cols = ['Price', 'Metacritic score']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    return df

def _create_metadata_column(df: pd.DataFrame) -> pd.DataFrame:
    """Create new column 'metadata' as a combination of text columns for Tf-IDF vectorization."""
    df['metadata'] = (
    df['Name'].astype(str) + " " + 
    df['Genres'].astype(str) + " " + 
    df['Tags'].astype(str) + " " + 
    df['About the game'].astype(str)
    ).str.lower()
    
    df['metadata'] = df['metadata'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
    return df

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Main function to clean and save the DataFrame."""
    df = _drop_invalid_name_genres_rows(df)
    df = _fill_text_nulls(df)
    df = _fill_numeric_nulls(df)
    df = _create_metadata_column(df)
    return df

import pandas as pd

def _fix_release_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Replace '0 - 0' release dates with empty strings."""
    if 'Release date' in df.columns:
        df['Release date'] = df['Release date'].replace("0 - 0", "")
    return df

def _convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert numeric columns from strings to numbers, fill NaN with 0."""
    numeric_columns = [
        'Estimated owners', 'Peak CCU', 'Required age', 'Price',
        'DiscountDLC count', 'Metacritic score', 'User score',
        'Positive', 'Negative', 'Achievements', 'Recommendations',
        'Average playtime forever', 'Average playtime two weeks',
        'Median playtime forever', 'Median playtime two weeks'
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

def _convert_boolean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert boolean columns from strings to actual bool types."""
    boolean_columns = ['Windows', 'Mac', 'Linux']
    for col in boolean_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().map({'true': True, 'false': False}).fillna(False)
    return df

def _fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Fill remaining NaN values with empty strings."""
    return df.fillna("")


def format_games_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main function to clean and format the games DataFrame for JSON/API use.
    Calls smaller helper functions for modularity.
    """
    df_clean = df.copy()
    df_clean = _fix_release_dates(df_clean)
    df_clean = _convert_numeric_columns(df_clean)
    df_clean = _convert_boolean_columns(df_clean)
    df_clean = _fill_missing(df_clean)
    return df_clean

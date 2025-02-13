def explore_data(df):
    """Print dataset size and available features."""
    print(f"Number of entries: {df.shape[0]}")
    print(f"Number of features: {df.shape[1]}")
    print("Available features:", df.columns.tolist())

def top_zipcodes(df, top_n=5):
    """Return the top N zip codes for 911 calls."""
    return df['zip'].value_counts().head(top_n)

def top_townships(df, top_n=5):
    """Return the top N townships for 911 calls."""
    return df['twp'].value_counts().head(top_n)

def unique_title_codes(df):
    """Return the number of unique title codes."""
    return df['title'].nunique()
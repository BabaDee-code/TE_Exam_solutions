def explore_data(df):
    """
    Print dataset size and available features.
    
    Parameters:
    df (DataFrame): The DataFrame containing the dataset.
    
    Returns:
    None
    """
    print(f"Number of entries: {df.shape[0]}")
    print(f"Number of features: {df.shape[1]}")
    print("Available features:", df.columns.tolist())

def top_zipcodes(df, top_n=5):
    """
    Return the top N zip codes for 911 calls.
    
    Parameters:
    df (DataFrame): The DataFrame containing the dataset.
    top_n (int): The number of top zip codes to return. Default is 5.
    
    Returns:
    Series: A Series containing the top N zip codes and their counts.
    """
    return df['zip'].value_counts().head(top_n)

def top_townships(df, top_n=5):
    """
    Return the top N townships for 911 calls.
    
    Parameters:
    df (DataFrame): The DataFrame containing the dataset.
    top_n (int): The number of top townships to return. Default is 5.
    
    Returns:
    Series: A Series containing the top N townships and their counts.
    """
    return df['twp'].value_counts().head(top_n)

def unique_title_codes(df):
    """
    Return the number of unique title codes.
    
    Parameters:
    df (DataFrame): The DataFrame containing the dataset.
    
    Returns:
    int: The number of unique title codes.
    """
    return df['title'].nunique()
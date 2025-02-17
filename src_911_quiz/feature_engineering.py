import pandas as pd

def extract_reason(df):
    """Creates a new column 'Reason' from the 'title' column."""
    df['Reason'] = df['title'].apply(lambda x: x.split(':')[0])
    return df

def extract_time_features(df):
    """Extract hour, month, and day of the week from timestamp."""
    df['timeStamp'] = pd.to_datetime(df['timeStamp'])
    df['Hour'] = df['timeStamp'].dt.hour
    df['Month'] = df['timeStamp'].dt.month
    df['Day of Week'] = df['timeStamp'].dt.day_name()
    return df

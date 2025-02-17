import pandas as pd

def load_data(file_path):
    """Load 911 call data from a CSV file."""
    return pd.read_csv(file_path)


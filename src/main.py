from data_loader import load_data
from data_exploration import explore_data, top_zipcodes, top_townships, unique_title_codes
from feature_engineering import extract_reason, extract_time_features
from visualization import plot_calls_by_reason, plot_calls_by_day, plot_calls_per_month, plot_heatmap

def main():
    """Main function to execute data analysis."""
    file_path = '../data/911.csv'
    df = load_data(file_path)
    
    explore_data(df)
    print("Top 5 Zip Codes:", top_zipcodes(df))
    print("Top 5 Townships:", top_townships(df))
    print("Number of Unique Title Codes:", unique_title_codes(df))
    
    df = extract_reason(df)
    plot_calls_by_reason(df)
    
    df = extract_time_features(df)
    plot_calls_by_day(df)
    plot_calls_per_month(df)
    plot_heatmap(df)

if __name__ == "__main__":
    main()
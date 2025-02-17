import pandas as pd
import os
import glob

def read_sample_data(sample_dir, sample_id):
    """
    Reads SDD11.csv, SDD21.csv, SDD22.csv, SCD21.csv from one sample folder,
    converts them from wide to long format, and returns a single DataFrame.
    """
    param_files = ["SCD21 Full Data.csv", "SDD21 Full Data.csv", "SDD22 Full Data.csv", "SCD21 Full Data.csv"]
    df_list = []

    for filename in param_files:
        filepath = os.path.join(sample_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found. Skipping.")
            continue
        
        # Identify parameter from filename (e.g., "SDD11.csv" -> "SDD11")
        param = filename.replace(".csv", "")

        # Read wide CSV
        df_wide = pd.read_csv(filepath)
        # Rename the frequency column for convenience
        if "Freq (MHz)" in df_wide.columns:
            df_wide = df_wide.rename(columns={"Freq (MHz)": "Freq_MHz"})

        # Melt from wide to long format
        # - "Freq_MHz" stays as an identifier
        # - The measurement columns (e.g., "P1_TX1_P2_RX1 SDD11") get melted into "Measurement" + "dB_Value"
        melt_cols = [c for c in df_wide.columns if c != "Freq_MHz"]
        df_long = df_wide.melt(
            id_vars=["Freq_MHz"],
            value_vars=melt_cols,
            var_name="Measurement",
            value_name="dB_Value"
        )

        # Some columns may look like "P1_TX1_P2_RX1 SDD11". Strip out the trailing " SDD11" (or " SDD21", etc.)
        df_long["Pair_Direction"] = df_long["Measurement"].str.replace(f" {param}", "", regex=False)

        # Add parameter and sample info
        df_long["Parameter"] = param
        df_long["SampleID"] = sample_id

        # Keep the essential columns
        df_long = df_long[["SampleID", "Parameter", "Freq_MHz", "Pair_Direction", "dB_Value"]]
        df_list.append(df_long)

    # Combine this sample’s 4 parameter files into one DataFrame
    sample_df = pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()
    return sample_df



def gather_all_samples(data_root="/workspaces/911_quiz/TE_SI_Basics"):
    """
    Iterates through each 'sample_x' folder under data_root, reads the four parameter CSVs,
    and concatenates everything into a single DataFrame.
    """
    all_samples = []

    # Suppose folders are named sample1, sample2, ... sample25
    sample_dirs = glob.glob(os.path.join(data_root, "Sample_*"))

    for sdir in sample_dirs:
        sample_id = os.path.basename(sdir)  # e.g. "sample1"
        sample_df = read_sample_data(sdir, sample_id)
        if not sample_df.empty:
            all_samples.append(sample_df)

    # Combine all samples into one large DataFrame
    if all_samples:
        master_df = pd.concat(all_samples, ignore_index=True)
    else:
        master_df = pd.DataFrame()
    
    return master_df

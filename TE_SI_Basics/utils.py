import pandas as pd
import os
import glob


# First, I will write functions to read and aggregate the data by Measurement Type from the 4 parameter files in each sample folder
# and convert them from wide to long format, then combine them into a single DataFrame.
# I will then iterate through all 25 samples and combine everything into a single DataFrame.
# I will also write a function to gather the 8 curves across 25 samples ie for each freq there might be up to 25*8 = 200 data points.
# I will compute mean & std of SCD21, SDD22, SDD21 and SDD11 across all 25 samples & 8 directions, by frequency.

def read_sample_data(sample_dir, sample_id):
    """
    Reads SDD11.csv, SDD21.csv, SDD22.csv, SCD21.csv from one sample folder,
    converts them from wide to long format, and returns a single DataFrame.
    """
    param_files = ["SCD21 Full Data.csv", "SDD11 Full Data.csv", "SDD21 Full Data.csv", "SDD22 Full Data.csv"]
    df_list = []

    for filename in param_files:
        filepath = os.path.join(sample_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found. Skipping.")
            continue
        
        # Identifying parameter from filename (e.g., "SDD11 Full Data.csv" -> "SDD11")
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

        #Strip out the trailing " SDD11" (or " SDD21", etc.)
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
        sample_id = os.path.basename(sdir)
        sample_df = read_sample_data(sdir, sample_id)
        if not sample_df.empty:
            all_samples.append(sample_df)

    # Combine all samples into one large DataFrame
    if all_samples:
        master_df = pd.concat(all_samples, ignore_index=True)
    else:
        master_df = pd.DataFrame()
    
    return master_df


if __name__ == "__main__":
    # First, I want to Gather data from all 25 samples
    data_root = "/workspaces/911_quiz/TE_SI_Basics" 
    all_data = gather_all_samples(data_root=data_root)

    print("All data shape:", all_data.shape)
    print("Columns:", all_data.columns.tolist())
    print(all_data.head())
    all_data.to_csv("all_data.csv", index=False)

    # Secondly, I will gather the 8 curves across 25 samples ie for each freq there might be up to 25*8 = 200 data points.

    # Example: for Insertion Loss (SCD21), we expect 200 data points per frequency
    scd21_data = all_data[all_data["Parameter"] == "SCD21 Full Data"]

    # to confirm if there is actually 200 points per frequency (to handle missing data)
    group_scd21 = scd21_data.groupby("Freq_MHz").size().reset_index(name="Count")
    print("Counts per frequency for SCD21:")
    print(group_scd21)

    # Similarly for (SDD11, SDD21, SDD22)
    sdd11_data = all_data[all_data["Parameter"] == "SDD11 Full Data"]
    group_sdd11 = sdd11_data.groupby("Freq_MHz").size().reset_index(name="Count")
    print("Counts per frequency for SDD11:")
    print(group_scd21)

    sdd21_data = all_data[all_data["Parameter"] == "SDD21 Full Data"]
    group_scd21 = scd21_data.groupby("Freq_MHz").size().reset_index(name="Count")
    print("Counts per frequency for SDD21:")
    print(group_scd21)

    sdd22_data = all_data[all_data["Parameter"] == "SDD22 Full Data"]
    group_sdd22 = sdd22_data.groupby("Freq_MHz").size().reset_index(name="Count")
    print("Counts per frequency for SDD22:")
    print(group_scd21)

    print(scd21_data)
    print(sdd11_data)
    print(sdd21_data)
    print(sdd22_data)


    # for further data aggregation, I computed mean & std of SDD21, SDD22 and SDD11 across all 25 samples & 8 directions, by frequency
    scd21_stats = (
        scd21_data
        .groupby("Freq_MHz")["dB_Value"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    sdd11_stats = (
        sdd11_data
        .groupby("Freq_MHz")["dB_Value"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    sdd21_stats = (
        sdd21_data
        .groupby("Freq_MHz")["dB_Value"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    sdd22_stats = (
        sdd22_data
        .groupby("Freq_MHz")["dB_Value"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )

    print("SCD21 stats by frequency:")
    print(scd21_stats.head(5))

    print("SDD11 stats by frequency:")
    print(sdd11_stats.head(5))

    print("SDD21 stats by frequency:")
    print(sdd21_stats.head(5))

    print("SDD22 stats by frequency:")
    print(sdd22_stats.head(5))

    # write out any aggregated data to CSV
    scd21_stats.to_csv("scd21_aggregated.csv", index=False)
    sdd11_stats.to_csv("sdd11_aggregated.csv", index=False)
    sdd21_stats.to_csv("sdd21_aggregated.csv", index=False)
    sdd22_stats.to_csv("sdd22_aggregated.csv", index=False)
    print("Done.")

# Secondly, I will write a function to plot the mean and standard deviation of SCD21, SDD22, SDD21 and SDD11 across all 25 samples & 8 directions, by frequency.
# I will use the aggregated data from the previous step to plot the data.

def plot_aggregated_data(aggregated_data, parameter):
    """
    Plots the mean and standard deviation of a parameter across all samples and directions by frequency.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.errorbar(
        aggregated_data["Freq_MHz"],
        aggregated_data["mean"],
        yerr=aggregated_data["std"],
        fmt="o-",
        label=f"{parameter} Mean",
        color="blue"
    )
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("dB Value")
    ax.set_title(f"{parameter} Mean and Standard Deviation by Frequency")
    ax.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_aggregated_data(scd21_stats, "SCD21")
    plot_aggregated_data(sdd11_stats, "SDD11")
    plot_aggregated_data(sdd21_stats, "SDD21")
    plot_aggregated_data(sdd22_stats, "SDD22")
    print("Done.")


    
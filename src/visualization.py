import matplotlib.pyplot as plt
import seaborn as sns

def plot_calls_by_reason(df):
    """Plot count of 911 calls by Reason."""
    sns.countplot(x='Reason', data=df, palette='viridis')
    plt.title('911 Calls by Reason')
    plt.show()

def plot_calls_by_day(df):
    """Plot emergency calls by Day of Week grouped by Reason."""
    sns.countplot(x='Day of Week', data=df, hue='Reason', palette='coolwarm')
    plt.xticks(rotation=45)
    plt.title('911 Calls by Day of the Week')
    plt.legend(title='Reason')
    plt.show()

def plot_calls_per_month(df):
    """Plot a linear regression fit for calls per month."""
    by_month = df.groupby('Month').count()
    sns.lmplot(x='Month', y='twp', data=by_month.reset_index())
    plt.title('Linear Fit of Calls per Month')
    plt.show()

def plot_heatmap(df):
    """Create a heatmap of calls by Hour vs. Day of the Week."""
    heatmap_data = df.groupby(['Day of Week', 'Hour']).count()['twp'].unstack()
    plt.figure(figsize=(12,6))
    sns.heatmap(heatmap_data, cmap='coolwarm')
    plt.title('Heatmap of Calls by Hour vs. Day of the Week')
    plt.show()
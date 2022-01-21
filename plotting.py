import pandas as pd
ncpus = range(1, 11)
subsampled_benchmark_time = []
for ncpu in ncpus:
    df = pd.read_csv("10_cells/benchmark_time_ncpu_{ncpu}.csv".format(ncpu=ncpu))
    df['ncpu'] = ncpu
    subsampled_benchmark_time.append(df)
subsampled_time_df = pd.concat(subsampled_benchmark_time)
subsampled_time_df
subsampled_time_df['type'] = '1M_subsampled_reads'
subsampled_time_df
full_benchmark_time = []
# Don't have the data for all cpus just yet
ncpus = [1, 3, 4, 5, 6]
for ncpu in ncpus:
    df = pd.read_csv("200_cells/benchmark_time_ncpu_{ncpu}.csv".format(ncpu=ncpu))
    df['ncpu'] = ncpu
    full_benchmark_time.append(df)
full_time_df = pd.concat(full_benchmark_time)
full_time_df
full_time_df['type'] = 'all_reads'
all_time_df = pd.concat([subsampled_time_df, full_time_df], ignore_index=True)
all_time_df
all_time_df.drop('unit', axis=1, inplace=True)
all_time_df
all_time_df.groupby(['ncpu', 'type']).mean()
mean_duration = all_time_df.groupby(['ncpu', 'type']).mean()['Duration']
mean_duration
mean_duration.columns = ['ncpu', 'type', 'duration']
mean_duration
mean_duration.reset_index()
mean_duration
mean_duration.reset_index(inplace=True)
mean_duration = mean_duration.reset_index()
mean_duration
import seaborn as sns
import matplotlib.pyplot as plt
ax = sns.lineplot(data=all_time_df, x='ncpu', y='Duration', hue='type')
ax.set_title("HTSeq time benchmark")
ax.set(xlabel='Number of CPU cores', ylabel = 'Duration (seconds)')
ax.set(xticks=np.arange(1, 11, 1))
import numpy as np
ax.set(xticks=np.arange(1, 11, 1))
plt.show()
ax = sns.lineplot(data=mean_duration, x='ncpu', y='Duration', hue='type')
ax.set_title("HTSeq mean time benchmark")
ax.set(xticks=np.arange(1, 11, 1))
ax.set(xlabel='Number of CPU cores', ylabel = 'Duration (seconds)')
plt.show()
history -f plotting.py

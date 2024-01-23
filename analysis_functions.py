import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from datetime import datetime, timezone


def benchmarkHistogram(pd_data, num_bins, figsize, max_latency, xlabel='Latency [ms]', ylabel='Measurements', save_fig=False):

    latency = pd_data.loc[pd_data["latency_seconds"] < max_latency, "latency_seconds"].values

    print(f"Mean Latency = {latency.mean()} ms")
    print(f"Root Mean Square Latency = {np.sqrt((latency**2).mean())} ms")
    print(f"Latency Standard Deviation = {latency.std()} ms")

    # Prepare the plot
    fig = plt.figure(layout="constrained", figsize=figsize)
    gs = GridSpec(3, 3, figure=fig)
    hist_ax = fig.add_subplot(gs[0:3, 0:3])
    axs = (hist_ax,)

    # Seaborn KDE histogram plot
    sns.histplot(data=latency, bins=num_bins, ax=hist_ax, linewidth=0, color="xkcd:baby blue")
    hist_ax.set_xlim((1, max_latency))
    ax2 = hist_ax.twinx()
    sns.kdeplot(data=latency, ax=ax2, label="Density", color="xkcd:black", linewidth=1, linestyle='--')

    hist_ax.axvline(x=latency.mean(), color='xkcd:red', label="Mean")

    # Trick to get the legend unified between the TwinX plots
    hist_ax.plot([], [], color="xkcd:black", linestyle='--', label='Density')

    xticks_locs = np.linspace(0, max_latency, 9)
    hist_ax.set_xticks(xticks_locs)

    for ax in axs:
        ax.legend()

    hist_ax.set_xlabel(xlabel)
    hist_ax.set_ylabel(ylabel)

    if save_fig:
        plt.savefig('abaddie24qrkey-fig-latency_histogram.pdf')

    plt.show()

def findClustersOverThreshold(delays, times, max_latency_threshold):
    exceeding_indices = np.where(delays > max_latency_threshold)[0]

    if len(exceeding_indices) == 0:
        return 0, []

    # Indices when consecutive sequences of exceeding threshold are broken + 1
    clusters = np.split(exceeding_indices, np.where(np.diff(exceeding_indices) != 1)[0] + 1)
    clusters = [cluster for cluster in clusters if len(cluster) > 1]
    for cluster in clusters:
        for id in range(len(cluster)):
            cluster[id] = delays[cluster[id]]

    percentage_exceeding = (len(exceeding_indices) / len(delays)) * 100

    # Extract times corresponding to the first index of each cluster
    cluster_times = [times[cluster[0]] for cluster in clusters]

    return percentage_exceeding, clusters, cluster_times
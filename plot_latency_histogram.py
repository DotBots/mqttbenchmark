import pandas as pd
from datetime import datetime
from dateutil import parser
import numpy as np
import json

# Fix to avoid Type 3 fonts on the figures
# http://phyletica.org/matplotlib-fonts/
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cv2


import seaborn as sns

# Define dataset file
data_file = "benchmarking_results.csv"
# Define Max latency threshold
max_lat = 0.2

# Import data
df=pd.read_csv(data_file)

# Use values below 200ms
latency = df.loc[df["latency_seconds"] < max_lat, "latency_seconds"].values * 1000 # Convert Latency from secondsto miliseconds
# Use all values.
latency_all = df["latency_seconds"].values * 1000 # Convert Latency from secondsto miliseconds

print(f"Mean Latency = {latency_all.mean()} mm")
print(f"Root Mean Square Latency = {np.sqrt((latency_all**2).mean())} mm")
print(f"Latency Standard Deviation = {latency_all.std()} mm")

# prepare the plot
fig = plt.figure(layout="constrained", figsize=(5,4))
gs = GridSpec(3, 3, figure = fig)
hist_ax    = fig.add_subplot(gs[0:3, 0:3])
axs = (hist_ax,)


# Sea-born KDE histogram plot
sns.histplot(data=latency,  bins=50, ax=hist_ax, linewidth=0, color="xkcd:baby blue")
hist_ax.set_xlim((1, max_lat*1e3))
ax2 = hist_ax.twinx()
sns.kdeplot(data=latency, ax=ax2, label="density", color="xkcd:black", linewidth=1, linestyle='--')

hist_ax.axvline(x=latency_all.mean(), color='xkcd:red', label="Mean")
# Trick to get the legend  unified between the TwinX plots
hist_ax.plot([], [], color="xkcd:black", linestyle='--', label = 'density')

xticks_locs = np.linspace(0, max_lat*1e3, 9)  # 10 x-ticks from 0 to 200
hist_ax.set_xticks(xticks_locs)

for ax in axs:
    # ax.grid()
    ax.legend()

# hist_ax.set_title('twoLH-2D Accuracy Analysis')
hist_ax.set_xlabel('Latency [ms]')
hist_ax.set_ylabel('Measurements')

plt.savefig('abaddie24qrkey-fig-latency_histogram.pdf')

plt.show()


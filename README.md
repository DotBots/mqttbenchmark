# mqttbenchmark

This Python code creates a topic in HiveMQ server.

A transmitter thread is used to publish a timestamp every 0.5 seconds together with a counter to identify lost packets.

A receiver thread is used to subscribe to the same topic and read the sent times, compare them with the received times, and write them in a `.csv` file in the following format:

```Received time - Sent time - Counter - Time difference ```

## Plotting results

- `plot_latency_histogram.py` reads the dataset `benchmarking_results.csv` and plots a histogram of packet latencies. All latencies above `200ms` are ignored. The resulting figure is saved at `abaddie24qrkey-fig-latency_histogram.pdf`
- `results_analysis.ipynb` plots a histogram of packets latencies, and determines the clusters where packet latencies exceed a given threshold of `200ms`. Starting times for these clusters are displayed.

# mqttbenchmark

This Python code creates a topic in HiveMQ server.

A transmitter thread is used to publish a timestamp every 0.5 seconds together with a counter to identify lost packets.

A receiver thread is used to subscribe to the same topic and read the sent times, compare them with the received times, and write them in a `.csv` file in the following format:

```Received time - Sent time - Counter - Time difference ```

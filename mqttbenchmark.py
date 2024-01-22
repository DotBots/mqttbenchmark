import time
import threading
import csv
import paho.mqtt.client as mqtt
import random
import string

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

broker = 'broker.hivemq.com'
TCP_port = 1883
topic = generate_random_string(20)
csv_file_path = 'benchmarking_results.csv'

def on_publish(client, userdata, mid):
    pass

def on_message(client, userdata, msg):
    received_time = time.time()  # Use time.time() for better precision
    message = msg.payload.decode('utf-8')
    print(f"Received message: {message}")
    message = message.split(',')
    sent_time = message[0]
    counter_column = message[1]
    # print(time_column, value_column)
    time_diff = float(received_time) - float(sent_time)

    # Save the received message, publishing time, and timestamp to a CSV file
    with open(csv_file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([received_time, sent_time, counter_column, time_diff])

class MQTTThread(threading.Thread):
    def run(self):
        client = mqtt.Client('delay_benchmarking_subscriber')
        client.on_publish = on_publish
        client.on_message = on_message

        client.connect(broker, TCP_port)
        client.subscribe(topic)
        client.loop_forever()

# Start the RX thread
rx_thread = MQTTThread()
rx_thread.start()

# Main thread for publishing
tx_thread = mqtt.Client('delay_benchmarking_publisher')
tx_thread.connect(broker, TCP_port)

counter = 0
while True:
    current_time = time.time()
    message = str(str(current_time) + ',' + str(counter)).encode('utf-8')
    tx_thread.publish(topic, payload=message, qos=0)
    print(f"Published message: {message}")
    counter += 1

    time.sleep(0.5)

#! python3

from confluent_kafka import Consumer, KafkaException, KafkaError
import json

# Kafka consumer configuration
conf = {
    'bootstrap.servers': '127.0.0.1:9094',  # Replace with your Kafka broker(s)
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False  # Important for manual batch processing and committing
}

# Create Consumer instance
consumer = Consumer(conf)

# Subscribe to a topic
topic = 'my_topic'  # Replace with your topic name
consumer.subscribe([topic])

# Define a deserializer function (e.g., for JSON)
def json_deserializer(msg_value):
    if msg_value is None:
        return None
    try:
        return json.loads(msg_value.decode('utf-8'))
    except json.JSONDecodeError as e:
        print(f"Error deserializing JSON: {e}")
        return None

batch_size = 10
timeout_ms = 1000  # Timeout in milliseconds for polling

try:
    while True:
        # Poll for a batch of messages
        messages = consumer.consume(num_messages=batch_size, timeout=timeout_ms / 1000.0)

        if not messages:
            # No messages received within the timeout
            continue

        processed_count = 0
        for msg in messages:
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f"%% {msg.topic()} [{msg.partition()}] reached end offset {msg.offset()}")
                else:
                    print(f"Error consuming message: {msg.error()}")
            else:
                # Deserialize and process the message
                deserialized_value = json_deserializer(msg.value())
                if deserialized_value is not None:
                    print(f"Received message: Key={msg.key()}, Value={deserialized_value}, Offset={msg.offset()}")
                    processed_count += 1
                # You can add your batch processing logic here
                # e.g., append to a list, then process the list once it reaches batch_size

        if processed_count > 0:
            # Commit offsets after processing the batch
            consumer.commit(asynchronous=False) # Use asynchronous=True for non-blocking commit
            print(f"Committed offset after processing {processed_count} messages.")

except KeyboardInterrupt:
    print("Consumer stopped by user.")
finally:
    # Close down consumer to commit final offsets.
    consumer.close()

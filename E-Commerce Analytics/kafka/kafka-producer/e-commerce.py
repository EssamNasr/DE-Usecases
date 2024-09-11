from kafka import KafkaProducer
import json
import random
import time

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulate Event Data
def simulate_ecommerce_events(num_users=1000):
    user_segments = ['new', 'returning']
    devices = ['desktop', 'mobile']

    for user_id in range(num_users):
        user_segment = random.choice(user_segments)
        device = random.choice(devices)

        # Visit Event
        visit_event = {
            'event_type': 'visit',
            'user_id': user_id,
            'user_segment': user_segment,
            'device': device,
            'timestamp': time.time()
        }
        yield visit_event

        # Simulate cart addition
        if random.random() > 0.3:  # 70% of users add to cart
            cart_event = {
                'event_type': 'add_to_cart',
                'user_id': user_id,
                'user_segment': user_segment,
                'device': device,
                'timestamp': time.time()
            }
            yield cart_event

            # Simulate purchase or abandonment
            if random.random() > 0.5:  # 50% of users who add to cart make a purchase
                purchase_event = {
                    'event_type': 'purchase',
                    'user_id': user_id,
                    'user_segment': user_segment,
                    'device': device,
                    'amount': random.uniform(20, 200),
                    'timestamp': time.time()
                }
                yield purchase_event
            else:
                abandon_event = {
                    'event_type': 'cart_abandonment',
                    'user_id': user_id,
                    'user_segment': user_segment,
                    'device': device,
                    'timestamp': time.time()
                }
                yield abandon_event

# Produce events to Kafka topic
def produce_events_to_kafka(topic, num_events=1000):
    for event in simulate_ecommerce_events(num_events):
        producer.send(topic, value=event)
        print(f"Produced event to Kafka: {event}")
        time.sleep(60)  # Simulate real-time events

if __name__ == "__main__":
    kafka_topic = 'ecommerce_events'
    produce_events_to_kafka(kafka_topic, num_events=10)
    producer.flush()

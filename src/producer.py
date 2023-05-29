import logging
import json
import requests
from datetime import datetime
from kafka import KafkaProducer
from time import sleep
import signal
import sys
import configparser

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Configuration
KAFKA_SERVER = config.get('Kafka', 'bootstrap_servers')
TOPIC = config.get('Kafka', 'topic')
REQUEST_TIMEOUT_MS = 40000
MAX_BLOCK_MS = 480000
API_URL = 'https://api.coincap.io/v2/assets?limit=20'

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    request_timeout_ms=REQUEST_TIMEOUT_MS,
    max_block_ms=MAX_BLOCK_MS
)

# Global variable to track if the script should continue running
running = True

def get_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an exception for non-successful responses
        data = response.json()
        if data['data']:
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            for item in data['data']:
                item['timestamp'] = timestamp
        return data['data']
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to retrieve data: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Failed to parse data: {e}")
        return None

def send_data_to_kafka(data):
    if data is not None:
        try:
            json_data = json.dumps(data).encode('utf-8')
            producer.send(TOPIC, value=json_data)
            logger.info("Data sent to Kafka successfully")
        except Exception as e:
            logger.error(f"Failed to send data to Kafka: {e}")

def stop(signal, frame):
    global running
    logger.info("Stopping the script...")
    running = False

def main():
    # Register the signal handler for graceful shutdown
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    
    logger.info("Starting the script...")
    
    while running:
        data = get_data()
        send_data_to_kafka(data)

    logger.info("Script stopped.")

if __name__ == "__main__":
    main()

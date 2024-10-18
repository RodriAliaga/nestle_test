####### This code reads OPCua tags from a JSON and publish to an MQTT broker 

import json
from opcua import Client
import time
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

os.environ.clear()
load_dotenv()

class OPCUAMQTTClient:
    def __init__(self, opcua_url, json_file_path, mqtt_broker, polling_interval, mqtt_port=1883):
        # OPC UA setup
        self.client = Client(opcua_url)
        self.json_file_path = json_file_path
        self.polling_interval = polling_interval  # Frequency to poll OPC UA values in seconds
        self.tags = []
        self.data_dict = {}

        # MQTT setup
        self.mqtt_client = mqtt.Client()
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_disconnect = self.on_mqtt_disconnect

    def load_tags_from_json(self):
        try:
            with open(self.json_file_path, 'r') as f:
                self.tags = json.load(f)
            print(f"Tags loaded successfully from JSON: {self.tags}")
        except Exception as e:
            print(f"Error loading JSON file: {e}")

    def read_opcua_values(self):
        for tag in self.tags:
            node_id = f"ns={tag['ns']};s={tag['s']}"
            try:
                node = self.client.get_node(node_id)
                value = node.get_value()
                self.data_dict[tag['Description']] = value
            except Exception as e:
                print(f"Error reading node {node_id}: {e}")

    def publish_to_mqtt(self):
        json_output = json.dumps(self.data_dict, indent=4)
        print(os.getenv('MQTT_PUBLISH_TOPIC'))
        mqtt_topic = os.getenv('MQTT_PUBLISH_TOPIC')
        try:
            self.mqtt_client.publish(mqtt_topic, json_output)
            print(f"Published to MQTT topic '{mqtt_topic}' with data:\n{json_output}")
        except Exception as e:
            print(f"Error publishing to MQTT: {e}")

    def on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print(f"Failed to connect to MQTT Broker, return code {rc}")

    def on_mqtt_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT Broker")

    def connect_mqtt(self):
        try:
            print(f"Connecting to MQTT broker at {self.mqtt_broker}:{self.mqtt_port}...")
            self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port)
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")

    def disconnect_mqtt(self):
        try:
            print("Disconnecting from MQTT broker...")
            self.mqtt_client.disconnect()
        except Exception as e:
            print(f"Error disconnecting from MQTT broker: {e}")

    def run(self):
        try:
            # Connect to OPC UA server
            print("Connecting to OPC UA server...")
            self.client.connect()
            print("OPC UA Client connected")

            # Connect to MQTT broker
            self.connect_mqtt()

            # Start MQTT loop in the background
            self.mqtt_client.loop_start()

            # Load tags from JSON file
            self.load_tags_from_json()

            # Poll OPC UA values and publish to MQTT at regular intervals
            while True:
                self.read_opcua_values()
                self.publish_to_mqtt()
                time.sleep(self.polling_interval)  # Wait for the specified polling interval

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Disconnect from OPC UA server
            try:
                self.client.disconnect()
                print("OPC UA Client disconnected")
            except Exception as e:
                print(f"Error disconnecting OPC UA client: {e}")

            # Stop the MQTT loop and disconnect from the broker
            try:
                self.mqtt_client.loop_stop()
                self.disconnect_mqtt() 

            except Exception as e:
                print(f"Error stopping MQTT loop or disconnecting MQTT: {e}")

# Example usage
if __name__ == "__main__":
    opcua_url = os.getenv('SERVER_URL')  # Change to your OPC UA server URL
    json_file_path = os.getenv('NESTLE_JSON_MAPPING')  # Change to your JSON file path
    mqtt_broker = os.getenv('MQTT_BROKER_HOST')  # Change to your MQTT broker
    polling_interval = int(os.getenv('POLLING_INTERVAL'))

    opcua_mqtt_client = OPCUAMQTTClient(opcua_url, json_file_path, mqtt_broker, polling_interval)
    opcua_mqtt_client.run()

####### This code is a listener, once a value changes on the OPC-UA it is published to a mqtt broker, it should work very well for continuous process, and float values, it tends to chenge frecuently
####### On boolean cases, is recomended to use Quality of service 2, on MQTT or instead use loop to read frecuently some values with low frecuncies.

import json
from opcua import Client
import time
import paho.mqtt.client as mqtt

class OPCUAMQTTClient:
    def __init__(self, opcua_url, json_file_path, mqtt_broker, mqtt_port=1883):
        # OPC UA setup
        self.client = Client(opcua_url)
        self.json_file_path = json_file_path
        self.sub = None
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

    def datachange_notification(self, node, val, data):
        node_id_str = f"ns={node.nodeid.NamespaceIndex};i={node.nodeid.Identifier}"
        print(f"Notification received for node: {node_id_str}, value: {val}")

        for tag in self.tags:
            tag_node_id = f"ns={tag['ns']};i={tag['id']}"
            if tag_node_id == node_id_str:
                self.data_dict[tag['Description']] = val
                json_output = json.dumps(self.data_dict, indent=4)
                print(f"Current Data (JSON format):\n{json_output}")

                # Publish to MQTT
                mqtt_topic = "opcua/raliagav/test"
                try:
                    self.mqtt_client.publish(mqtt_topic, json_output)
                    print(f"Published to MQTT topic '{mqtt_topic}'")
                except Exception as e:
                    print(f"Error publishing to MQTT: {e}")
                break

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

            # Load tags and subscribe
            self.load_tags_from_json()
            self.sub = self.client.create_subscription(500, self)

            handles = []
            for tag in self.tags:
                node_id = f"ns={tag['ns']};i={tag['id']}"
                try:
                    node = self.client.get_node(node_id)
                    handle = self.sub.subscribe_data_change(node)
                    handles.append(handle)
                    print(f"Listening for changes on {tag['Description']} with node ID {node_id}")
                except Exception as e:
                    print(f"Error subscribing to node {node_id}: {e}")

            # Keep the listener running
            while True:
                time.sleep(1)

        except Exception as e:
            print(f"An error occurred in the OPC UA or MQTT connection: {e}")
        finally:
            # Unsubscribe from all nodes
            if self.sub:
                for handle in handles:
                    try:
                        self.sub.unsubscribe(handle)
                    except Exception as e:
                        print(f"Error unsubscribing: {e}")
            
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
    opcua_url = "opc.tcp://192.168.2.50:4840"  # Change to your OPC UA server URL
    json_file_path = "Resources/nestle_mapping.json"  # Change to your JSON file path
    mqtt_broker = "172.172.1.12"  # Change to your MQTT broker

    opcua_mqtt_client = OPCUAMQTTClient(opcua_url, json_file_path, mqtt_broker)
    opcua_mqtt_client.run()

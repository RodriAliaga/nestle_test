"""from opcua import Client
from importlib import resources
import json


data = {}

def main():
    server_url = "opc.tcp://192.168.2.50:4840"
    client = Client(server_url)

    try:
        client.connect()
        #print("Connected to OPC UA Server")

        # Browse root and objects nodes for debugging
        root_node = client.get_root_node()
        print("Root Node Children:")
        for child in root_node.get_children():
            print("Child:", child)

        objects_node = client.get_objects_node()
        #print("Objects node is: ", objects_node)

        # Get namespace array for debugging
        ns_array = client.get_namespace_array()
        #print("Namespaces available:", ns_array)

        # Load the JSON mapping file
        try:
            with resources.path("Resources", "nestle_mapping_copy.json") as path:
                with open(path) as f:
                    df = json.load(f)
                    print("Loaded mapping JSON:", df)
        except Exception as e:
            print("Not possible to open the JSON file:", e)
            return

        # Iterate over the JSON data and read nodes using their string identifiers
        for el in df:
            try:
                ns = el["ns"]
                string_id = el["s"]
                tag_name = el["Description"]  

                # Create a NodeId using the string identifier
                node = client.get_node(f"ns={ns};s={string_id}")
                value = node.get_value()
                data[tag_name] = value
                #print(f'{tag_name}: {value}')
            except Exception as e:
                print(f"An error occurred while reading {tag_name}: {e}")
        print(f'The data is {data}')
        json_data = json.dumps(data)
        print(json_data)

    except Exception as e:
        print(f"An error occurred while connecting or browsing: {e}")

    finally:
        client.disconnect()
        print("Disconnected from OPC UA Server")

if __name__ == "__main__":
    main()"""


"""
import json
from opcua import Client
from importlib import resources
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

# Global dictionary to store tag values
data = {}


def load_mapping_file(file_name):
    
    try:
        with resources.path("Resources", file_name) as path:
            with open(path) as f:
                return json.load(f)
    except Exception as e:
        print(f"Failed to load JSON file: {e}")
        raise


def read_opcua_data(client, mapping):
    
    global data
    for el in mapping:
        try:
            ns = el["ns"]
            string_id = el["s"]
            tag_name = el["Description"]

            # Read value from OPC UA node
            node = client.get_node(f"ns={ns};s={string_id}")
            value = node.get_value()
            data[tag_name] = value

        except Exception as e:
            print(f"Error reading {tag_name}: {e}")


def main():
    # OPC connection
    #server_url = "opc.tcp://192.168.2.50:4840"
    load_dotenv()

    server_url = os.getenv('SERVER_URL')
    print(server_url)
    client = Client(server_url)
    
    # MQTT Connection
    broker = "https://test.mosquitto.org/" # Removed protocol
    port = "1883"
    topic = "/home/temperature/raliagav"

    print(f'{broker} : {port} - {topic}')

    try:
        # OPC UA connection
        client.connect()
        print("OPCUA connected")
        # MQTT connection
        mqtt_client = mqtt.Client()
        mqtt_client.connect(broker, port)
        mqtt_client.loop_start()  # Start the MQTT client loop

        print("MQTT Client Connected:", mqtt_client)

        # Browse the root node for debugging (optional, can be removed)
        root_node = client.get_root_node()
        print("Root Node Children:", root_node.get_children())

        # Load OPC UA node mapping from JSON file
        mapping = load_mapping_file("nestle_mapping_copy.json")

        # Read OPC UA data
        read_opcua_data(client, mapping)

        # Convert the collected data to JSON format
        json_data = json.dumps(data)
        print(f"Collected data: {json_data}")

        # Publish collected data to MQTT topic
        mqtt_client.publish(topic, json_data)  # Publish the JSON data

    except Exception as e:
        print(f"An error occurred during OPC UA operations: {e}")

    finally:
        # Ensure that the clients are disconnected
        client.disconnect()
        mqtt_client.loop_stop()  # Stop the MQTT client loop
        mqtt_client.disconnect()  # Disconnect MQTT client
        print("Disconnected from OPC UA Server and MQTT Broker.")


if __name__ == "__main__":
    main()"""


import json
from opcua import Client
from importlib import resources
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

# Global dictionary to store tag values
data = {}

def load_mapping_file(file_name):
    """Load the JSON mapping file containing OPC UA node information."""
    try:
        with resources.path("Resources", file_name) as path:
            with open(path) as f:
                return json.load(f)
    except Exception as e:
        print(f"Failed to load JSON file: {e}")
        raise

def read_opcua_data(client, mapping):
    """Read values from OPC UA server using mapping data."""
    global data
    for el in mapping:
        try:
            ns = el["ns"]
            string_id = el["s"]
            tag_name = el["Description"]

            # Read value from OPC UA node
            node = client.get_node(f"ns={ns};s={string_id}")
            value = node.get_value()
            
            # Ensure the value is converted to a suitable type (if needed)
            if isinstance(value, (str, bytes)):
                # Handle string values, if necessary
                value = value.decode() if isinstance(value, bytes) else value
            
            data[tag_name] = value

        except Exception as e:
            print(f"Error reading {tag_name}: {e}")

def main():
    # OPC connection
    load_dotenv()

    server_url = os.getenv('SERVER_URL')
    print(server_url)
    client = Client(server_url)
    
    # MQTT Connection
    broker = os.getenv('MQTT_BROKER_HOST')
    port = os.getenv('MQTT_BROKER_PORT')  # Changed to integer
    topic = os.getenv('MQTT_PUBLISH_TOPIC')

    print(f'{broker} : {port} - {topic}')

    try:
        # OPC UA connection
        client.connect()
        print("OPCUA connected")

        # MQTT connection
        mqtt_client = mqtt.Client()  # Updated for newer version
        mqtt_client.connect(broker, int(port))
        mqtt_client.loop_start()  # Start the MQTT client loop

        print("MQTT Client Connected:", mqtt_client)

        # Browse the root node for debugging (optional, can be removed)
        root_node = client.get_root_node()
        print("Root Node Children:", root_node.get_children())

        # Load OPC UA node mapping from JSON file
        mapping = load_mapping_file(os.getenv('NESTLE_JSON_MAPPING'))

        # Read OPC UA data
        read_opcua_data(client, mapping)

        # Convert the collected data to JSON format
        json_data = json.dumps(data)
        print(f"Collected data: {json_data}")

        # Publish collected data to MQTT topic
        mqtt_client.publish(topic, json_data)  # Publish the JSON data

    except Exception as e:
        print(f"An error occurred during OPC UA operations: {e}")

    finally:
        # Ensure that the clients are disconnected
        client.disconnect()
        mqtt_client.loop_stop()  # Stop the MQTT client loop
        mqtt_client.disconnect()  # Disconnect MQTT client
        print("Disconnected from OPC UA Server and MQTT Broker.")

if __name__ == "__main__":
    main()


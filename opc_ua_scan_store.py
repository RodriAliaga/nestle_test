import json
from opcua import Client
from opcua import ua

# Replace this URL with your OPC UA server endpoint
OPC_SERVER_URL = "opc.tcp://192.168.2.50:4840"  # Example endpoint

# Connect to the OPC UA server
client = Client(OPC_SERVER_URL)

# Data dictionary to store the scanned data
scanned_data = {}

try:
    # Establish connection to the OPC UA server
    client.connect()
    print(f"Connected to {OPC_SERVER_URL}")
    
    # Get the root node
    root = client.get_root_node()
    print("Root node:", root)

    # Function to convert values to JSON serializable format
    def serialize_value(value):
        if isinstance(value, (int, float, str, bool, type(None))):
            return value
        elif isinstance(value, list):
            return [serialize_value(v) for v in value]
        else:
            # Convert non-serializable values to strings
            return str(value)

    # Function to recursively browse nodes and store values in a dictionary
    def browse_nodes(node, data, level=0):
        children = node.get_children()
        for child in children:
            # Get node ID and display name
            node_id = str(child.nodeid)
            display_name = child.get_display_name().Text

            # Try to read the value of the node
            try:
                value = child.get_value()
                serialized_value = serialize_value(value)
            except ua.UaStatusCodeError:
                serialized_value = "N/A (No value or not readable)"
            except Exception as e:
                serialized_value = f"Error reading value: {e}"

            # Store node details in the data dictionary
            data[node_id] = {
                "name": display_name,
                "value": serialized_value
            }

            # Recurse into children nodes
            browse_nodes(child, data, level + 1)

    # Start browsing from the "Objects" folder
    objects_node = client.get_objects_node()
    browse_nodes(objects_node, scanned_data)

    # Save scanned data to a JSON file
    with open("scanned_data.json", "w") as json_file:
        json.dump(scanned_data, json_file, indent=4)

    print("Scanned data saved to scanned_data.json")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Disconnect from the server
    client.disconnect()
    print(f"Disconnected from {OPC_SERVER_URL}")

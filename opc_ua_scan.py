from opcua import Client
from opcua import ua

# Replace this URL with your OPC UA server endpoint
OPC_SERVER_URL = "opc.tcp://192.168.2.33:4840"  # Example endpoint

# Connect to the OPC UA server
client = Client(OPC_SERVER_URL)

try:
    # Establish connection to the OPC UA server
    client.connect()
    print(f"Connected to {OPC_SERVER_URL}")
    
    # Get the root node
    root = client.get_root_node()
    print("Root node:", root)

    # Function to recursively browse nodes and print values
    def browse_nodes(node, level=0):
        children = node.get_children()
        for child in children:
            # Get node ID and display name
            node_id = child.nodeid
            display_name = child.get_display_name().Text

            # Try to read the value of the node
            try:
                value = child.get_value()
            except ua.UaStatusCodeError:
                value = "N/A (No value or not readable)"
            except Exception as e:
                value = f"Error reading value: {e}"

            # Print node details
            print("  " * level + f"Node ID: {node_id}, Name: {display_name}, Value: {value}")

            # Recurse into children nodes
            browse_nodes(child, level + 1)

    # Start browsing from the "Objects" folder
    objects_node = client.get_objects_node()
    browse_nodes(objects_node)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Disconnect from the server
    client.disconnect()
    print(f"Disconnected from {OPC_SERVER_URL}")

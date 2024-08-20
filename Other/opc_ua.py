from opcua import Client
from opcua import ua

def main():
    # Define the server URL
    server_url = "opc.tcp://192.168.2.50:4840"

    # Create a client instance
    client = Client(server_url)

    try:
        # Connect to the OPC UA server
        client.connect()
        print("Connected to OPC UA Server")

        # Get the root node
        root_node = client.get_root_node()
        print("Root node is: ", root_node)

        # Browse the objects node
        objects_node = client.get_objects_node()
        print("Objects node is: ", objects_node)

        # Browse and read data from a specific node
        var = client.get_node("ns=4;i=12")  # Adjust the node ID based on your server
        print("Node: ", var)
        print("Value: ", var.get_value())

        # Write data to the node
        new_value = 42
        var.set_value(new_value, ua.VariantType.Int16)
        print("New Value: ", var.get_value())

    finally:
        # Close the connection
        client.disconnect()
        print("Disconnected from OPC UA Server")

if __name__ == "__main__":
    main()

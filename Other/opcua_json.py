from opcua import Client
from opcua import ua


def main():
    # Define the OPC UA server URL
    server_url = "opc.tcp://192.168.2.50:4840"

    # Create a client instance
    client = Client(server_url)
    
    try:
        # Connect to the OPC UA server
        client.connect()
        print("Connected to OPC UA Server")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the connection
        client.disconnect()
        print("Disconnected from OPC UA Server")

if __name__ == "__main__":
    main()

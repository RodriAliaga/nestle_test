from opcua import Client, ua
from importlib import resources
import json

def main():
    # Define the OPC UA server URL
    server_url = "opc.tcp://192.168.2.50:4840"

    # Create a client instance
    client = Client(server_url)

    try:
        # Connect to the OPC UA server
        client.connect()
        print("Connected to OPC UA Server")

        # Browse the objects node
        objects_node = client.get_objects_node()
        print("Objects node is: ", objects_node)

        try:
            with resources.path("Resources", "nestle_mapping.json") as path:
                with open(path) as f:
                    df = json.load(f)
                    print(df)
        
        except Exception as e:
            print("No possible to open the Json")


        for el in df:
            try:
                ns = el["ns"]
                i = el["id"]
                tag_name = el["Description"]
                xid = f"ns={ns};i={i}"
                value = client.get_node(xid).get_value()
                print(f'{tag_name}:{value}')
            except:
                 print(f"An error occurred: {e}")
        # Access the node using the namespace index and node ID
        
    except Exception as e:
             print(f"An error occurred: {e}")
    
    finally:
        # Close the connection
        client.disconnect()
        print("Disconnected from OPC UA Server")

if __name__ == "__main__":
    main()

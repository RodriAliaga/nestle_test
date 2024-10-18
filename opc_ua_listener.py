from opcua import Client, ua
import time

class OPCUAListener:
    def __init__(self, url, variable_node_id):
        self.client = Client(url)
        self.variable_node_id = variable_node_id
        self.sub = None

    def datachange_notification(self, node, val, data):
        print(f"Data changed: {node}, New value: {val}")

    def run(self):
        try:
            self.client.connect()
            print("Client connected")

            # Create a subscription to listen for changes
            self.sub = self.client.create_subscription(500, self)
            handle = self.sub.subscribe_data_change(self.client.get_node(self.variable_node_id))

            print(f"Listening for changes on {self.variable_node_id}...")
            while True:
                time.sleep(1)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.sub:
                self.sub.unsubscribe(handle)
            self.client.disconnect()
            print("Client disconnected")

if __name__ == "__main__":
    # Define your OPC UA server URL and the node ID of the variable to listen to
    opcua_url = "opc.tcp://192.168.2.50:4840"  # Change to your server URL
    variable_node_id = "ns=4;i=9"  # Change to your variable's Node ID

    listener = OPCUAListener(opcua_url, variable_node_id)
    listener.run()

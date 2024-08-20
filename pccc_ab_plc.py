from pycomm3 import SLCDriver
from importlib import resources
import json

def read_plc_data(plc_ip, address):
    # Create an instance of SLCDriver with the PLC IP address
    with SLCDriver(plc_ip) as plc:
        try:
            # Read data from the specified address
            response = plc.read(address)
            if response:
                print(f"Value at address {address}: {response.value}")
            else:
                print(f"Failed to read data from address {address}")
        except Exception as e:
            print(f"An error occurred: {e}")


def test_read():
    
        try:
            with resources.path("Resources", "nestle_plc_mapping.json") as path:
                with open(path) as f:
                    df = json.load(f)
                    #print(df)
        
        except Exception as e:
            print("No possible to open the Json")


        try:
            for el in df:
                add = el["Address"]
                var_name = el["Description"]
                read_plc_data("192.168.2.51",add)
                #print(add)

        except:
            print("Error Reading PLC data")

if __name__ == "__main__":
    # Define the IP address of the PLC and the address to read from
    test_read()

#source 44818 destn 62860
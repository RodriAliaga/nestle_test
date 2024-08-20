from pycomm3 import CIPDriver

# IP address and port of the AVEVA ArchestrA Wonderware server
server_ip = '192.168.2.78'
server_port = 44818

# List of known tags
tags = ['$SYS$ErrorCount', '$SYS$ItemCount', '$SYS$Licensed']

# Connect to the server
with CIPDriver(f'{server_ip}:{server_port}') as plc:
    for tag in tags:
        try:
            value = plc.read_tag(tag)  # Adjust this method as needed
            print(f'Tag: {tag}, Value: {value}')
        except Exception as e:
            print(f'Failed to read tag {tag}: {e}')

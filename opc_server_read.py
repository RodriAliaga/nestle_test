import OpenOPC

# Create an OPC client
opc = OpenOPC.client()

# List available OPC servers
servers = opc.servers()
print("Available OPC Servers:", servers)

# Connect to a specific OPC server
opc.connect('ArchestrA.DASABCIP')

# Read a tag
tag_value = opc.read('Your.Tag.Name')
print(f"Tag Value: {tag_value}")

# Disconnect the OPC client
opc.close()

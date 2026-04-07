# Read file and output hex only
with open("flag.enc", "rb") as f:
    data = f.read()

# Convert to hex string
hex_data = data.hex()

print(hex_data)  # prints pure hex characters

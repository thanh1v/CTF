from cryptography.hazmat.primitives import serialization

# Load the PEM file
with open("private.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,  # or provide the password if the key is encrypted
    )

# Print the key details
numbers = private_key.private_numbers()
print("Modulus (n):", numbers.public_numbers.n)
print("Public exponent (e):", numbers.public_numbers.e)
print("Private exponent (d):", numbers.d)
print("Prime factors (p, q):", numbers.p, numbers.q)

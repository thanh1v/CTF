import string

# Read the encoded text from out.txt
with open('out.txt', 'r') as f:
    encoded_text = f.read().strip()

# Step 1: Reverse the ROT-13 like shift
# If 'chr(ord(i)-13)' was used for encryption, then 'chr(ord(i)+13)' reverses it.
# However, we need to handle wrapping around the alphabet if it's truly a ROT-13
# for specific character sets, but here it's a direct ASCII shift.
# Let's assume it's a simple character code shift.

decrypted_rot_text_list = []
for char_code in encoded_text:
    decrypted_rot_text_list.append(chr(ord(char_code) + 13))

decrypted_rot_text = "".join(decrypted_rot_text_list)

# Step 2: Create a reverse Baconian dictionary for decoding
# Note that 'i' and 'j' map to the same code, and 'u' and 'v' map to the same code.
# This means there might be ambiguity in the original flag if 'i'/'j' or 'u'/'v' were used.
# For now, we'll just pick one (e.g., 'i' for '01000', 'u' for '10011')
reverse_baconian = {
    '00000': 'a', '00001': 'b', '00010': 'c', '00011': 'd', '00100': 'e',
    '00101': 'f', '00110': 'g', '00111': 'h', '01000': 'i', # Could be 'j'
    '01001': 'k', '01010': 'l', '01011': 'm', '01100': 'n', '01101': 'o',
    '01110': 'p', '01111': 'q', '10000': 'r', '10001': 's', '10010': 't',
    '10011': 'u', # Could be 'v'
    '10100': 'w', '10101': 'x', '10110': 'y', '10111': 'z'
}

# Step 3: Extract the Baconian binary and then the flag
decoded_flag = ""
# Process the decrypted_rot_text in chunks of 5 characters
for i in range(0, len(decrypted_rot_text), 5):
    segment = decrypted_rot_text[i:i+5]
    baconian_binary = ""
    for char in segment:
        if char.isupper():
            baconian_binary += '1'
        elif char.islower():
            baconian_binary += '0'
        # If there are non-alphabetic characters, they were skipped during encryption,
        # so they wouldn't contribute to the Baconian code.
        # We need to assume the `text` only contained alphabetic characters,
        # or that the `flag` was also purely alphabetic.

    if baconian_binary in reverse_baconian:
        decoded_flag += reverse_baconian[baconian_binary]
    else:
        # This case should ideally not happen if the input was properly formed
        decoded_flag += "?" # Placeholder for unknown or non-Baconian segments

print(f"Decoded Flag: {decoded_flag}")  #>>> flag: tjctf{oinkooinkoooinkooooink}

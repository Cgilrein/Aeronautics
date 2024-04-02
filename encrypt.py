key = b''  # Provide a non-empty key here

def encrypt(token):
    encrypted_data = bytearray()
    for index, letter in enumerate(token):
        encrypted_data.append(ord(letter) ^ key[index % len(key)])
    return encrypted_data.hex()

def decrypt(encrypted_data):
    decrypted_data = bytearray()
    for index, byte in enumerate(bytes.fromhex(encrypted_data)):
        decrypted_data.append(byte ^ key[index % len(key)])
    return decrypted_data.decode('utf-8')

### Put Tokens here ###
token = ""
encrypted_token = "0408060b14103c1113173e435220252025282f204237003d3133180a503e1019223c0f3e570b27522e230e050454330101342219151d3057225b583e551b38340c183329343a0521302834520847563321372e383b2c00142d0a0c5004"

if (input("Encrypting? y/n: ") == "y"):
    encrypted_token = encrypt(token)
    print("Encrypted:", encrypted_token)
else:
    decrypted_token = decrypt(encrypted_token)
    print("Decrypted:", decrypted_token)

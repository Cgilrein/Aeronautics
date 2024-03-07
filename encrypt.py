key = b''

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
encrypted_token = ""

if (input("Encrypting? y/n: ")):
    encrypted_token = encrypt(token)
    print("Encrypted:", encrypted_token)
else:
    decrypted_token = decrypt(encrypted_token)
    print("Decrypted:", decrypted_token)
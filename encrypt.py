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
encrypted_token = "0409023c30352f0e39342d285118210b3338562b4b0c1425352a3e1a271f2e19170c522435254728"

if (input("Encrypting? y/n: ") == "y"):
    encrypted_token = encrypt(token)
    print("Encrypted:", encrypted_token)
else:
    decrypted_token = decrypt(encrypted_token)
    print("Decrypted:", decrypted_token)

from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

print("FERNET_KEY:", key.decode())

encrypted_data = f.encrypt(b"This message is being encrypted and cannot be seen!")
print(encrypted_data)

decrypted_data = f.decrypt(encrypted_data) # f is the variable that has the value of the key.
print(decrypted_data)
print(decrypted_data.decode())
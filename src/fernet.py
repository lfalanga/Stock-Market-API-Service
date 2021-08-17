import os
import dotenv
from cryptography.fernet import Fernet

def get_ecryption_key():
    # Verify if an encription key exists
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    existing_key = os.getenv("FERNET_KEY")
    if (existing_key == None) or (existing_key == ""):
        key = Fernet.generate_key()
        os.environ["FERNET_KEY"] = key.decode()
        # Write changes to .env file.
        dotenv.set_key(dotenv_file, "FERNET_KEY", os.environ["FERNET_KEY"])
        return Fernet(key.encode("utf-8"))
    else:
        return Fernet(existing_key.encode("utf-8"))

def test_encryption():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    str_value = "123456"
    existing_key = os.getenv("FERNET_KEY")
    cipher = Fernet(existing_key.encode("utf-8"))
    encrypted_value = cipher.encrypt(str_value.encode("utf-8"))
    print("ENCRIPTED:", encrypted_value)
    decrypted_data = cipher.decrypt(encrypted_value)
    test_1 = "gAAAAABhGwkvKwtQtPr9Q3wy3Yz7hnAhTXqn2Qq1zMB7xh7i9BOfo0CO07KZo_XLLs7iEmeSpR_T0moQTrOOQtES15KrQtzbOA=="
    test_2 = "gAAAAABhGwmww8HYa66oeDpLN-Xau197qBCAXH_iT1-3OPuJUrF38zJmFAIdh3fMAV9Mjx-U4_K5si9Bu5PHuIowF0OAZu2LYw=="
    #decrypted_data = cipher.decrypt(test_2.encode("utf-8"))
    print("DECRIPTED:", decrypted_data)
    print("DECRIPTED_DECODED:", decrypted_data.decode("utf-8"))
    pass

if __name__ == '__main__':
    test_encryption()
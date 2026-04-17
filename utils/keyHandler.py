import os
from cryptography.hazmat.primitives import serialization

class KeyHandler:
    """Utilitário para salvar e carregar chaves RSA do disco."""
    
    @staticmethod
    def save_private_key(private_key, filename: str):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(filename, 'wb') as f:
            f.write(pem)

    @staticmethod
    def save_public_key(public_key, filename: str):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(filename, 'wb') as f:
            f.write(pem)

    @staticmethod
    def load_private_key(filename: str):
        with open(filename, 'rb') as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    @staticmethod
    def load_public_key(filename: str):
        with open(filename, 'rb') as f:
            return serialization.load_pem_public_key(f.read())
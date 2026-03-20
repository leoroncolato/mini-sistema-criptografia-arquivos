import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes

class CryptoManager:
    """Gerencia as operações de baixo nível de criptografia RSA e AES."""
    
    @staticmethod
    def generate_rsa_keypair():
        """Gera um par de chaves RSA de 2048 bits."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        return private_key, private_key.public_key()

    @staticmethod
    def rsa_encrypt(public_key, data: bytes) -> bytes:
        """Criptografa dados (como a chave AES) usando a Chave Pública RSA."""
        return public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def rsa_decrypt(private_key, encrypted_data: bytes) -> bytes:
        """Descriptografa dados usando a Chave Privada RSA."""
        return private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def rsa_sign(private_key, data: bytes) -> bytes:
        """Gera uma assinatura digital dos dados usando a Chave Privada."""
        return private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    @staticmethod
    def rsa_verify(public_key, signature: bytes, data: bytes) -> None:
        """Verifica a assinatura digital. Levanta exceção se for inválida."""
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    @staticmethod
    def aes_encrypt(data: bytes) -> tuple:
        """Gera chave AES-GCM, criptografa os dados e retorna (chave, nonce, ciphertext)."""
        aes_key = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(aes_key)
        nonce = os.urandom(12) # Vetor de inicialização (necessário para o GCM)
        ciphertext = aesgcm.encrypt(nonce, data, None)
        return aes_key, nonce, ciphertext

    @staticmethod
    def aes_decrypt(aes_key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
        """Descriptografa os dados usando a chave AES e o nonce."""
        aesgcm = AESGCM(aes_key)
        return aesgcm.decrypt(nonce, ciphertext, None)
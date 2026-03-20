import base64
from core.cryptoUtils import CryptoManager

class SenderService:
    """Lógica da Empresa A - Preparar e Enviar o Contrato"""
    
    def __init__(self, sender_private_key, receiver_public_key):
        self.sender_private_key = sender_private_key
        self.receiver_public_key = receiver_public_key

    def prepare_contract_package(self, document_bytes: bytes) -> dict:
        print("[Empresa A] Iniciando preparação do contrato...")
        
        # 1. Criptografa o documento com AES
        aes_key, nonce, encrypted_document = CryptoManager.aes_encrypt(document_bytes)
        print("[Empresa A] Documento criptografado com AES-256-GCM.")
        
        # 2. Criptografa a chave AES com a Chave Pública RSA da Empresa B
        encrypted_aes_key = CryptoManager.rsa_encrypt(self.receiver_public_key, aes_key)
        print("[Empresa A] Chave AES criptografada com RSA da Empresa B.")
        
        # 3. Gera a Assinatura Digital do documento ORIGINAL com a Chave Privada RSA da Empresa A
        digital_signature = CryptoManager.rsa_sign(self.sender_private_key, document_bytes)
        print("[Empresa A] Assinatura digital gerada com sucesso.")
        
        # 4. Monta o pacote final codificando bytes em Base64 (Prática de Mercado)
        package = {
            "chave_simetrica_criptografada": base64.b64encode(encrypted_aes_key).decode('utf-8'),
            "documento_criptografado": base64.b64encode(encrypted_document).decode('utf-8'),
            "informacoes_descriptografia": {
                "nonce": base64.b64encode(nonce).decode('utf-8')
            },
            "assinatura_digital": base64.b64encode(digital_signature).decode('utf-8')
        }
        
        print("[Empresa A] Pacote finalizado e pronto para envio.\n")
        return package


class ReceiverService:
    """Lógica da Empresa B - Receber, Decriptar e Validar o Contrato"""
    
    def __init__(self, receiver_private_key, sender_public_key):
        self.receiver_private_key = receiver_private_key
        self.sender_public_key = sender_public_key

    def process_received_package(self, package: dict) -> bytes:
        print("[Empresa B] Pacote recebido. Iniciando processamento...")
        
        # 1. Decodifica o Base64 de volta para bytes
        try:
            encrypted_aes_key = base64.b64decode(package["chave_simetrica_criptografada"])
            encrypted_document = base64.b64decode(package["documento_criptografado"])
            nonce = base64.b64decode(package["informacoes_descriptografia"]["nonce"])
            digital_signature = base64.b64decode(package["assinatura_digital"])
        except KeyError as e:
            raise ValueError(f"Pacote malformado. Faltando o campo: {e}")

        # 2. Descriptografa a chave AES usando a Chave Privada RSA da Empresa B
        aes_key = CryptoManager.rsa_decrypt(self.receiver_private_key, encrypted_aes_key)
        print("[Empresa B] Chave AES recuperada com sucesso.")
        
        # 3. Descriptografa o documento usando a chave AES e o nonce
        decrypted_document = CryptoManager.aes_decrypt(aes_key, nonce, encrypted_document)
        print("[Empresa B] Documento descriptografado com AES.")
        
        # 4. Valida a Assinatura Digital usando a Chave Pública RSA da Empresa A
        # Se a assinatura for inválida, o método rsa_verify levanta uma exceção (InvalidSignature)
        CryptoManager.rsa_verify(self.sender_public_key, digital_signature, decrypted_document)
        print("[Empresa B] Assinatura digital VALIDADA! O remetente é autêntico e o documento não foi alterado.")
        
        return decrypted_document
import socket
import json
from core.cryptoUtils import CryptoManager
from services.exchangeService import SenderService
from utils.keyHandler import KeyHandler
from utils.fileHandler import FileHandler

def setup_keys():
    """Gera e salva as chaves da Empresa A, caso não existam."""
    priv_path, pub_path = "chaves/empresa_a_priv.pem", "chaves/empresa_a_pub.pem"
    try:
        priv_key = KeyHandler.load_private_key(priv_path)
        print("[Empresa A] Chaves carregadas do disco.")
    except FileNotFoundError:
        print("[Empresa A] Gerando novas chaves RSA...")
        priv_key, pub_key = CryptoManager.generate_rsa_keypair()
        KeyHandler.save_private_key(priv_key, priv_path)
        KeyHandler.save_public_key(pub_key, pub_path)
    return priv_key

def main():
    print("=== EMPRESA A (CLIENTE) INICIADA ===")
    priv_key_a = setup_keys()
    
    # Carrega a chave pública da Empresa B
    try:
        pub_key_b = KeyHandler.load_public_key("chaves/empresa_b_pub.pem")
    except FileNotFoundError:
        print("Inicie o servidor da Empresa B primeiro para que ela gere sua chave pública!")
        return

    sender = SenderService(priv_key_a, pub_key_b)

    # Lê o contrato original em PDF [cite: 143]
    caminho_pdf = "data/contrato_teste.pdf"
    print(f"[Empresa A] Lendo arquivo: {caminho_pdf}")
    contrato_bytes = FileHandler.read_file(caminho_pdf)

    # Executar processo de preparação do contrato [cite: 144]
    pacote_json = sender.prepare_contract_package(contrato_bytes)
    dados_para_envio = json.dumps(pacote_json).encode('utf-8')

    # Configuração do Socket para envio
    host = '127.0.0.1'
    port = 65432

    print(f"[Empresa A] Conectando ao servidor em {host}:{port}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            s.sendall(dados_para_envio)
            print("[Empresa A] Pacote criptografado enviado com sucesso pela rede!")
        except ConnectionRefusedError:
            print("[ERRO] Não foi possível conectar. Certifique-se de que a Empresa B está rodando.")

if __name__ == "__main__":
    main()
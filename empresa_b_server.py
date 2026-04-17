import socket
import json
from core.cryptoUtils import CryptoManager
from services.exchangeService import ReceiverService
from utils.keyHandler import KeyHandler
from utils.fileHandler import FileHandler

def setup_keys():
    """Gera e salva as chaves da Empresa B, caso não existam."""
    priv_path, pub_path = "chaves/empresa_b_priv.pem", "chaves/empresa_b_pub.pem"
    try:
        priv_key = KeyHandler.load_private_key(priv_path)
        print("[Empresa B] Chaves carregadas do disco.")
    except FileNotFoundError:
        print("[Empresa B] Gerando novas chaves RSA...")
        priv_key, pub_key = CryptoManager.generate_rsa_keypair()
        KeyHandler.save_private_key(priv_key, priv_path)
        KeyHandler.save_public_key(pub_key, pub_path)
    return priv_key

def main():
    print("=== EMPRESA B (SERVIDOR) INICIADA ===")
    priv_key_b = setup_keys()
    
    # Carrega a chave pública da Empresa A (Necessária para validar a assinatura digital)
    # Em um cenário real, a Empresa B já teria recebido isso antes.
    try:
        pub_key_a = KeyHandler.load_public_key("chaves/empresa_a_pub.pem")
    except FileNotFoundError:
        print("Aguarde a Empresa A gerar suas chaves primeiro!")
        return

    receiver = ReceiverService(priv_key_b, pub_key_a)

    # Configuração do Socket
    host = '127.0.0.1'
    port = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[Empresa B] Aguardando conexão na porta {port}...")
        
        conn, addr = s.accept()
        with conn:
            print(f"[Empresa B] Conectado a {addr}")
            
            # Recebe os dados em blocos
            data = b""
            while True:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet
            
            # Deserializa o JSON recebido
            pacote_json = json.loads(data.decode('utf-8'))
            
            try:
                # Processo de validação e descriptografia [cite: 145]
                contrato_descriptografado = receiver.process_received_package(pacote_json)
                
                # Salva o arquivo em disco
                caminho_final = "data/Contrato_Recebido_Validado.pdf"
                FileHandler.write_file(caminho_final, contrato_descriptografado)
                print(f"\n[SUCESSO] Contrato recuperado e salvo em: {caminho_final}")
                
            except Exception as e:
                print(f"\n[ERRO CRÍTICO] Falha de segurança: {str(e)}")

if __name__ == "__main__":
    main()
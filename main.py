import json
from core.crypto_utils import CryptoManager
from services.exchange_service import SenderService, ReceiverService
from utils.file_handler import FileHandler

def main():
    print("=== INICIANDO SISTEMA DE TROCA SEGURA DE CONTRATOS ===\n")

    # Passo 1: Gerar pares de chaves para Empresa A e Empresa B
    print("1. Gerando chaves RSA (Empresa A e Empresa B)...")
    empresa_A_priv, empresa_A_pub = CryptoManager.generate_rsa_keypair()
    empresa_B_priv, empresa_B_pub = CryptoManager.generate_rsa_keypair()
    print("Chaves geradas.\n")

    # Passo 2: LER O CONTRATO EM PDF (Modificado)
    caminho_pdf_original = "data/contrato_teste.pdf"
    print(f"2. Lendo o arquivo original: {caminho_pdf_original}")
    
    try:
        # Lê os bytes do PDF
        contrato_bytes = FileHandler.read_file(caminho_pdf_original)
    except FileNotFoundError as e:
        print(f"[ERRO] {e}\nCrie a pasta 'data' e coloque um arquivo 'contrato_teste.pdf' nela.")
        return

    # Instanciar os serviços
    sender = SenderService(empresa_A_priv, empresa_B_pub)
    receiver = ReceiverService(empresa_B_priv, empresa_A_pub)

    # Passo 3: Executar processo de preparação do contrato (Empresa A)
    pacote_json = sender.prepare_contract_package(contrato_bytes)
    
    # (Opcional) Salvando o pacote criptografado no disco para o recrutador ver
    caminho_pacote = "data/pacote_criptografado.json"
    with open(caminho_pacote, "w") as f:
        json.dump(pacote_json, f, indent=4)
    print(f"   -> Pacote de dados salvo em: {caminho_pacote}\n")

    # Passo 4 e 5: Executar processo de validação e descriptografia (Empresa B)
    try:
        contrato_descriptografado = receiver.process_received_package(pacote_json)
        
        # Confirmação final e gravação do novo PDF
        if contrato_bytes == contrato_descriptografado:
            caminho_pdf_final = "data/contrato_validado_e_descriptografado.pdf"
            
            # Salva os bytes descriptografados em um NOVO arquivo PDF
            FileHandler.write_file(caminho_pdf_final, contrato_descriptografado)
            
            print("\n=== SUCESSO ABSOLUTO! ===")
            print("O contrato foi recebido, validado pela assinatura digital e descriptografado.")
            print(f"O PDF final foi salvo e pode ser aberto em: {caminho_pdf_final}")
        else:
            print("\n[ERRO] O contrato descriptografado não bate com o original.")
            
    except Exception as e:
        print(f"\n[ERRO CRÍTICO] Falha na validação ou descriptografia: {str(e)}")

if __name__ == "__main__":
    main()
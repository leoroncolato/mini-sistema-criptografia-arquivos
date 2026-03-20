from core.cryptoUtils import CryptoManager
from services.exchangeService import SenderService, ReceiverService
import json

def main():
    print("=== INICIANDO SISTEMA DE TROCA SEGURA DE CONTRATOS ===\n")

    # Passo 1: Gerar pares de chaves para Empresa A e Empresa B
    print("1. Gerando chaves RSA (Empresa A e Empresa B)...")
    empresa_A_priv, empresa_A_pub = CryptoManager.generate_rsa_keypair()
    empresa_B_priv, empresa_B_pub = CryptoManager.generate_rsa_keypair()
    print("Chaves geradas.\n")

    # Passo 2: Criar um contrato de teste (simulando a leitura de um PDF)
    contrato_original = b"CONTRATO DE PRESTACAO DE SERVICOS. Valor: R$ 100.000,00. Assinado: CEO."
    
    # Instanciar os serviços
    sender = SenderService(empresa_A_priv, empresa_B_pub)
    receiver = ReceiverService(empresa_B_priv, empresa_A_pub)

    # Passo 3: Executar processo de preparação do contrato (Empresa A)
    pacote_json = sender.prepare_contract_package(contrato_original)
    
    # (Opcional) Mostrando como o pacote viaja pela rede:
    print("=== PACOTE TRANSMITIDO PELA REDE ===")
    print(json.dumps(pacote_json, indent=2)[:300] + "...\n[CONTEUDO TRUNCADO PARA EXIBICAO]\n")

    # Passo 4 e 5: Executar processo de validação e descriptografia (Empresa B)
    try:
        contrato_descriptografado = receiver.process_received_package(pacote_json)
        
        # Confirmação final
        if contrato_original == contrato_descriptografado:
            print("\n=== SUCESSO! ===")
            print("O contrato recebido e descriptografado corresponde perfeitamente ao original.")
            print(f"Conteúdo: {contrato_descriptografado.decode('utf-8')}")
    except Exception as e:
        print(f"\n[ERRO CRÍTICO] Falha na validação ou descriptografia: {str(e)}")

if __name__ == "__main__":
    main()
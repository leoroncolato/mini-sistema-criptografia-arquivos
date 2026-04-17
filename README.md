# 🛡️ Sistema de Envio Seguro de Contratos Digitais

## 📌 Visão Geral
Este projeto simula uma plataforma corporativa (como a fictícia SecureDocs) para o envio e validação de documentos digitais confidenciais. Desenvolvido em **Python**, o sistema garante confidencialidade, integridade e autenticidade na troca de contratos em formato PDF entre duas organizações via rede (Sockets).

### 📋 Sistema de Logs e Auditoria
Para fins de conformidade e depuração, o sistema gera logs automáticos de todas as operações críticas:
- Cada etapa (geração de chave, cifragem, assinatura, recepção e validação) é registrada.
- Os logs são gravados em tempo real na pasta `logs/`, permitindo a auditoria completa do processo de transmissão.

## 🏗️ Arquitetura e Fluxo Criptográfico
A aplicação utiliza uma abordagem de **Criptografia Híbrida**, unindo a velocidade do AES com a segurança de distribuição de chaves do RSA, juntamente com Assinaturas Digitais.

O fluxo de funcionamento segue rigorosamente os seguintes passos:

1. **Geração de Chaves:** A Empresa A (Remetente) e a Empresa B (Destinatária) geram seus próprios pares de chaves RSA de 2048 bits.
2. **Preparação e Criptografia (Empresa A):**
   - O sistema lê o contrato em PDF em formato binário.
   - Gera-se uma chave simétrica efêmera (AES-256-GCM) para criptografar o documento de forma rápida.
   - A chave AES é então criptografada utilizando a **Chave Pública RSA da Empresa B** (garantindo que só ela possa acessar a chave simétrica).
   - O sistema gera um hash (SHA-256) do documento original e o assina com a **Chave Privada RSA da Empresa A** (garantindo a autoria e integridade).
3. **Transmissão:** Os dados (Chave AES cifrada, Documento cifrado, Nonce e Assinatura Digital) são codificados em Base64, empacotados em um JSON e enviados via Socket TCP.
4. **Validação e Descriptografia (Empresa B):**
   - O servidor recebe o pacote e utiliza a **Chave Pública da Empresa A** para validar a assinatura digital. Se o arquivo foi alterado na rede, o processo é abortado.
   - Com a assinatura validada, o sistema utiliza a **Chave Privada da Empresa B** para revelar a chave AES.
   - A chave AES descriptografa o documento, restaurando o PDF original perfeitamente.

## 🚀 Como Executar (Demonstração)

**Pré-requisitos:**
\`\`\`bash
pip install cryptography
\`\`\`

**Passo 1: Iniciar a Empresa B (Servidor / Destinatário)**
Em um terminal, inicie o servidor. Ele irá gerar suas chaves e aguardar a conexão:
\`\`\`bash
python servidor_empresa_b.py
\`\`\`

**Passo 2: Iniciar a Empresa A (Cliente / Remetente)**
Em um segundo terminal, inicie o cliente. Ele irá ler o arquivo `dados/Modelo de Contrato.pdf`, criptografar e enviar:
\`\`\`bash
python cliente_empresa_a.py
\`\`\`

**Resultado:**
O terminal da Empresa B confirmará a validação da assinatura digital e o documento descriptografado será salvo na pasta `dados/` em formato PDF, pronto para ser aberto.
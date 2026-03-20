# 🛡️ Mini Sistema de Criptografia de Arquivos

## 📌 Visão Geral
Este projeto é uma solução desenvolvida em **Node.js** para garantir a confidencialidade, integridade e autenticidade na troca de documentos (como contratos em PDF) entre diferentes organizações. O sistema simula a comunicação segura entre duas entidades (Empresa A e Empresa B), garantindo que apenas o destinatário correto consiga acessar o conteúdo e validando a identidade do remetente.

## 🏗️ Arquitetura e Segurança
A aplicação adota uma abordagem de **criptografia híbrida**, combinando algoritmos simétricos e assimétricos para otimizar performance e segurança.

O pacote de dados final transmitido entre os sockets contém:
1. A chave simétrica criptografada.
2. O documento alvo criptografado.
3. Informações necessárias para o processo de descriptografia.
4. A assinatura digital do remetente.

### Decisões Técnicas de Criptografia
- **AES (Advanced Encryption Standard):** Utilizado para a criptografia do documento em si, garantindo processamento rápido para arquivos.
- **RSA (Rivest-Shamir-Adleman):** Utilizado para o encapsulamento de chaves. A chave AES é criptografada com a Chave Pública da organização destinatária.
- **Assinatura Digital:** Gerada utilizando a Chave Privada da organização remetente, permitindo ao destinatário atestar a autoria e a integridade do arquivo recebido.

## 🔄 Fluxo de Execução
O ciclo de vida da troca de arquivos segue as seguintes etapas:
1. **Geração de Chaves:** Criação dos pares de chaves (Pública/Privada) para a Empresa A e Empresa B.
2. **Preparação:** Um contrato de teste (PDF) é submetido ao sistema. O documento é criptografado, a assinatura digital é gerada e o pacote seguro é montado.
3. **Transmissão:** Envio do pacote através de comunicação via Sockets.
4. **Validação e Descriptografia:** O destinatário recebe o pacote, valida a assinatura digital e descriptografa o arquivo.
5. **Auditoria:** Confirmação de que o arquivo recebido e descriptografado corresponde exatamente ao documento original.
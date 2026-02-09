## 3. Funcionalidades e Módulos

### 📡 [1] Ferramentas de Rede (Scanner & DoS)

_Módulo dedicado ao reconhecimento e testes de stress (Stress Testing)._

-   **🔍 Port Scanner:**
    
    -   **Input:** IP do alvo (ex: `192.168.56.101`).
        
    -   **Output:** Lista de portas **ABERTAS** (21, 22, 80, 443, etc.).
        
-   **💥 SYN Flood / UDP Flood:**
    
    -   **Interface:** `VirtualBox Host-Only Ethernet Adapter`.
        
    -   **IP Alvo:** O IP do Kali.
        
    -   **MAC Address:** `08:00:27:xx:xx:xx` (Essencial para contornar bloqueios do Windows).
        
    -   **Pacotes:** Define a quantidade (ex: `5000`) para simular tráfego intenso.
        

### 🌍 [2] Análise de Logs e Geolocalização

_Gera relatórios forenses visuais baseados em logs._

-   **Gerar Logs:** Cria dados fictícios de ataques globais.
    
-   **Analisar:** Processa o ficheiro, identifica Países de origem (GeoIP) e gera um **PDF** na pasta `reports/`.
    

### 🔐 [3] Segurança (Password Manager + 2FA)

_Cofre digital com encriptação AES e Autenticação de Dois Fatores._

1.  **Adicionar:** Guarda Serviço, User e Password (encriptado).
    
2.  **Consultar (Protegido):**
    
    -   Exige código **TOTP** (Time-based One-Time Password).
        
    -   Usa o **Microsoft Authenticator** 📱 para ler o QR Code.
        
    -   Desencriptação ocorre apenas com o código de 6 dígitos correto.
        

### 🚪 [4] Port Knocking (Acesso Secreto)

_Método avançado para abrir portas "invisíveis"._

-   **Cenário:** O SSH (Porta 22) está **bloqueado**.
    
-   **Ação:** Envia a sequência secreta: `7000` -> `8000` -> `9000`.
    
-   **Resultado:** A porta 22 abre-se durante **10 segundos**. ⏱️
    

----------

4. Estrutura de Ficheiros

Organização dos dados gerados pelo programa:

**Diretoria / Ficheiro**

**Descrição**

**Tipo**

`src/`

Código fonte do projeto

Python

`data/passwords.db`

Base de dados das credenciais

SQLite (Encriptado)

`data/secret.key`

Chave mestra de encriptação

**CRÍTICO** 🛑

`reports/*.pdf`

Relatórios gerados

Documento

`logs/auth.log`

Histórico de atividades

Texto

----------

## ⚠️ 5. Resolução de Problemas (Troubleshooting)

> **🔴 Erro: "MAC address to reach destination not found"**
> 
> **Solução:** O Windows falhou ao encontrar o caminho (ARP).
> 
> Preencha manualmente o campo **MAC Address** no menu de ataque com o endereço do Kali (use `ip a` no Linux para ver).

> **🔴 Erro: Port Knocking diz "OK" mas o SSH não abre**
> 
> **Soluções:**
> 
> 1.  Confirme se o serviço `knockd` está ativo: `sudo service knockd status`.
>     
> 2.  Confirme se o SSH está ligado: `sudo service ssh start`.
>     
> 3.  Verifique se está a usar o IP da rede **Host-Only** (`192.168.56.xxx`).
>     

> **🔴 Erro: Não consigo instalar o `knockd` no Kali**
> 
> **Solução:** A rede "Host-Only" não tem internet.
> 
> 1.  Mude a rede da VM para **NAT**.
>     
> 2.  Instale: `sudo apt install knockd`.
>     
> 3.  Mude a rede de volta para **Host-Only**.
>     

----------


----------

Desenvolvido por Rafael Narciso | 2026

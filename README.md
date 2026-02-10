Aqui tens o manual formatado em **Markdown** profissional, pronto para ser usado num ficheiro `README.md` no GitHub ou para entregar como documentação técnica.

Adicionei "Badges", ícones e tabelas para ficar com um aspeto visual moderno e organizado.

---

# 📘 PySecurity Toolkit - Manual de Utilização

**Mestrado em Engenharia de Segurança Informática** **Autor:** Rafael Conceição Narciso (24473)

**Data:** Janeiro 2026

---

## 📋 Índice

1. [Pré-requisitos e Ambiente](https://www.google.com/search?q=%231-pr%C3%A9-requisitos-e-ambiente)
2. [Instalação das Dependências](https://www.google.com/search?q=%232-instala%C3%A7%C3%A3o-das-depend%C3%AAncias)
3. [Configuração de Rede e Firewall](https://www.google.com/search?q=%233-configura%C3%A7%C3%A3o-de-rede-e-firewall)
4. [Estrutura do Projeto](https://www.google.com/search?q=%234-estrutura-do-projeto)
5. [Guia de Utilização](https://www.google.com/search?q=%235-guia-de-utiliza%C3%A7%C3%A3o)
6. [Resolução de Problemas](https://www.google.com/search?q=%236-resolu%C3%A7%C3%A3o-de-problemas)

---

## 1. Pré-requisitos e Ambiente

Para garantir o funcionamento correto dos módulos de rede (*Raw Sockets*) e criptografia, o sistema deve cumprir os seguintes requisitos:

* **Sistema Operativo:**
* Windows 10/11 (Host ou VM).
* Kali Linux (Recomendado para Pentest).


* **Virtualização (VirtualBox):**
* As máquinas devem estar configuradas em **Host-Only Adapter** (Rede Exclusiva de Hospedeiro).
* **Objetivo:** Permitir comunicação isolada (ex: IPs na gama `192.168.56.x`).


* **Permissões:**
* 🔓 **Windows:** Executar o terminal como **Administrador**.
* 🔓 **Linux:** Executar com `sudo` (obrigatório para o Scapy).



---

## 2. Instalação das Dependências

O projeto depende de bibliotecas externas para manipulação de pacotes, criptografia e geração de relatórios.

### 🪟 No Windows (PowerShell)

Execute o seguinte comando para instalar tudo de uma vez:

```powershell
pip install scapy cryptography pyotp reportlab requests

```

### 🐧 No Kali Linux (Terminal)

Devido às políticas de segurança do Python em distros modernas, use:

```bash
sudo pip3 install scapy cryptography pyotp reportlab requests --break-system-packages

```

---

## 3. Configuração de Rede e Firewall

⚠️ **CRÍTICO:** O módulo de Chat P2P utiliza a porta `9999`. A Firewall do Windows bloqueia esta porta por defeito.

### Passo 1: Configurar a Firewall no Windows

Tem duas opções para permitir a comunicação:

1. **Método Seguro (Recomendado):**
* Abrir "Firewall do Windows Defender com Segurança Avançada".
* Criar uma **Regra de Entrada (Inbound Rule)** para a porta **TCP 9999**.
* Ação: **Permitir conexão**.


2. **Método Rápido (Apenas para Testes):**
* Desativar temporariamente a Firewall para as redes "Privada" e "Pública".



### Passo 2: Sincronização de Chaves (Para o Chat)

O Chat P2P utiliza encriptação **AES Simétrica**. Para que o Windows e o Linux se entendam:

1. Execute o Chat no Windows primeiro (isto gera a chave `chat_secret.key`).
2. Copie este ficheiro da pasta `src/security/keys/` do Windows.
3. Cole-o na **mesma pasta** no Kali Linux.

> **Nota:** Se as chaves forem diferentes, a conexão estabelece-se, mas as mensagens aparecerão como "Erro de Desencriptação".

---

## 4. Estrutura do Projeto

A organização das pastas deve ser mantida para evitar erros de importação (`ModuleNotFoundError`).

```text
PySecurityToolkit/
│
├── main.py                 # 🚀 PONTO DE PARTIDA (Executar este ficheiro)
├── requirements.txt        # Lista de bibliotecas
│
└── src/                    # Código Fonte
    ├── network/            # Ferramentas de Rede
    │   ├── scanner.py
    │   ├── dos_attacks.py
    │   └── port_knocking.py
    │
    ├── security/           # Ferramentas de Segurança
    │   ├── pass_manager.py
    │   ├── secure_chat.py
    │   └── keys/           # 🔑 Chaves AES (chat_secret.key)
    │
    ├── reporting/          # Geração de PDF
    └── logs/               # Análise de Logs

```

---

## 5. Guia de Utilização

Para iniciar a aplicação, execute na raiz do projeto:

* **Windows:** `python main.py`
* **Linux:** `sudo python3 main.py`

### 📡 Menu [1] Ferramentas de Rede

| Ferramenta | Descrição |
| --- | --- |
| **Port Scanner** | Realiza um *TCP Connect Scan*. Insira o IP alvo e o intervalo de portas (ex: 1-100). |
| **UDP Flood** | Envia pacotes aleatórios para saturar a CPU do alvo. Use `Ctrl+C` para parar. |
| **SYN Flood** | **(Requer Root)** Envia pacotes com IPs falsos (*Spoofing*) para esgotar a memória do servidor. |

### 📊 Menu [2] Relatórios

* Gera um relatório detalhado em **PDF** sobre a atividade recente, incluindo scans realizados e tentativas de conexão. O ficheiro é guardado automaticamente na pasta raiz.

### 🔐 Menu [3] Segurança

#### 1. Password Manager (Cofre)

* Armazena credenciais encriptadas com **Fernet (AES-128)**.
* Na primeira execução, define uma *Master Password*.
* Funcionalidades: Adicionar, Listar (Desencriptar) e Remover senhas.

#### 2. Chat P2P Seguro

Comunicação em tempo real entre duas máquinas.

* **Modo [1] Hospedar (Servidor):**
* Fica à escuta na porta `9999`.
* Deve ser iniciado primeiro (geralmente no Windows).


* **Modo [2] Conectar (Cliente):**
* Pede o IP do servidor (ex: `192.168.56.1`).
* Conecta-se ao anfitrião.


* **Funcionamento:**
* Uma vez conectados, ambos podem escrever simultaneamente (*Full-Duplex*).
* Escreva `sair` para encerrar a conexão e as *threads*.



---

## 6. Resolução de Problemas

| Erro Comum | Causa Provável | Solução |
| --- | --- | --- |
| `ModuleNotFoundError` | Bibliotecas em falta. | Correr `pip install -r requirements.txt`. |
| `PermissionError` | Falta de privilégios. | Executar o terminal como **Admin** ou **sudo**. |
| Chat: `[*] A conectar...` (infinito) | Firewall a bloquear. | Verificar regra da porta 9999 no Windows. |
| Chat: Mensagens ilegíveis | Chaves diferentes. | Copiar `chat_secret.key` do Windows para o Linux. |
| `scapy` não envia pacotes | Interface errada. | O Scapy no Windows pode escolher a interface Wi-Fi em vez da VirtualBox. Desativar Wi-Fi durante o teste pode ajudar. |

---

> **Aviso Legal:** Esta ferramenta foi desenvolvida exclusivamente para fins académicos no âmbito do Mestrado em Engenharia de Segurança Informática. O autor não se responsabiliza pelo uso indevido das ferramentas ofensivas fora de um ambiente laboratorial controlado.
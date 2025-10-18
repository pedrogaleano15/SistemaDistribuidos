# Jogo Distribuído com Pygame e MQTT (Prova P1 - SD)

Este repositório contém um projeto de jogo multiplayer simples (movimentação de jogadores) desenvolvido para a disciplina de Sistemas Distribuídos. O projeto utiliza Pygame para a interface gráfica e o protocolo MQTT para gerenciar a comunicação em rede entre os jogadores.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Pygame**: Biblioteca para a criação da interface gráfica e lógica do jogo.
* **Paho-MQTT**: Biblioteca para implementação do cliente MQTT em Python.
* **Mosquitto**: (Recomendado) Broker MQTT para mediar a comunicação.

## 📦 Instalação

Para rodar este projeto, é altamente recomendado o uso de um ambiente virtual Python (`venv`) para isolar as dependências.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/pedrogaleano15/SistemaDistribuidos.git](https://github.com/pedrogaleano15/SistemaDistribuidos.git)
    cd SistemaDistribuidos
    ```

2.  **Crie e ative um ambiente virtual:**
    
    *(Execute os comandos abaixo dentro da pasta do projeto)*

    ```bash
    # 1. Crie o ambiente virtual (pode ser .venv ou venv)
    python -m venv .venv
    
    # 2. Ative o ambiente
    # No Windows (PowerShell/CMD):
    .\.venv\Scripts\activate
    # No macOS/Linux (Bash):
    source .venv/bin/activate
    ```
    *(Seu terminal deve agora mostrar `(.venv)` ao lado do prompt).*

3.  **Instale as dependências:**
    
    *(Com o ambiente virtual ainda ativo)*
    
    ```bash
    pip install -r requirements.txt
    ```
    *(Este comando irá ler o arquivo `requirements.txt` e instalar o `pygame` e o `paho-mqtt` automaticamente).*

4.  **Broker MQTT:**
    Este projeto requer um broker MQTT. Você pode usar uma instalação local do [Mosquitto](https://mosquitto.org/download/) ou um broker de teste público (como `broker.hivemq.com`).

    *Se for usar o Mosquitto localmente, certifique-se de que ele esteja em execução e ouvindo na porta configurada no código (padrão: 50000).*

## 🚀 Como Executar

Para iniciar o jogo, você precisa de (pelo menos) dois terminais para simular os dois jogadores.

**IMPORTANTE:** Certifique-se de que seu broker MQTT (Mosquitto) esteja em execução.

1.  **Terminal 1 (Inicia o Jogador 1):**
    *(Não se esqueça de ativar o `.venv` neste terminal!)*
    ```bash
    python jogo.py
    ```
    *(Este é o comando padrão, ele será o Jogador 1 [Verde]).*

2.  **Terminal 2 (Inicia o Jogador 2):**
    *(Abra um NOVO terminal e ative o `.venv` nele também!)*
    ```bash
    python jogo.py player2
    ```
    *(Ao passar o argumento "player2", o script se configura automaticamente como o Jogador 2 [Vermelho]).*

## 👨‍💻 Autor

* **Pedro Galeano** - [pedrogaleano15](https://github.com/pedrogaleano15)
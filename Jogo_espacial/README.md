# Jogo Espacial Multiplayer com MQTT

Este é um jogo de nave espacial multiplayer (estilo "space shooter") desenvolvido com Pygame e Python. A comunicação entre os jogadores e a geração de eventos são gerenciadas por um broker MQTT.

Este projeto foi desenvolvido como parte da disciplina de Sistemas Distribuídos.

## 🖼️ Assets Utilizados

* `nave.png`: Imagem da nave utilizada por todos os jogadores.
* `asteroide.png`: Imagem dos obstáculos.
* `fundo_espacial.jpg`: Imagem de fundo do jogo.

## 🏗️ Arquitetura do Sistema

Este projeto é composto por três componentes principais que rodam de forma independente:

1.  **`jogador.py` (Cliente do Jogo)**
    * É o script principal que o jogador executa.
    * Gerencia a interface gráfica (Pygame), a movimentação, os tiros e as colisões.
    * Publica a posição do jogador e os eventos (tiros, morte, reinício).
    * Escuta a posição de outros jogadores e os obstáculos gerados.

2.  **`gerador_obstaculo.py` (Serviço/Publisher)**
    * Um script que roda em segundo plano no servidor (ou localmente).
    * Ele espera por um sinal de "jogo_iniciado" no MQTT.
    * Quando o jogo começa, ele gera obstáculos em intervalos regulares e os publica no tópico `jogo/obstaculos`.

3.  **`observador.py` (Cliente/Subscriber)**
    * Um cliente "espectador" que se conecta ao broker.
    * Ele escuta todos os tópicos (posições, obstáculos, tiros, eventos) e recria uma visualização completa do jogo em tempo real, sem interagir.

## 📦 Instalação

(Siga os passos com o ambiente virtual ativado)

1.  **Clone o repositório e entre na pasta:**
    ```bash
    git clone [https://github.com/pedrogaleano15/SistemaDistribuidos.git](https://github.com/pedrogaleano15/SistemaDistribuidos.git)
    cd SistemaDistribuidos/Jogo_espacial
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # 1. Crie o venv
    python -m venv .venv
    
    # 2. Ative o venv (Windows)
    .\.venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Como Executar

Para rodar o jogo completo, você precisará de **4 ou 5 terminais** (todos com o ambiente virtual ativado).

**IMPORTANTE:** Todos os scripts (`jogador.py`, `gerador_obstaculo.py`, `observador.py`) possuem uma variável `BROKER_IP = "192.168.23.83"`. Você **DEVE** alterar este IP para o endereço IP da máquina que está rodando o broker Mosquitto (ou usar "localhost" se for tudo na mesma máquina).

1.  **Terminal 0: O Broker MQTT**
    * Inicie seu broker Mosquitto (ou use um público).

2.  **Terminal 1: Gerador de Obstáculos**
    * Este script deve ser iniciado primeiro. Ele ficará "Esperando sinal de início...".
    ```bash
    python gerador_obstaculo.py
    ```

3.  **Terminal 2: Observador (Opcional)**
    * Você pode rodar este script para ter uma visão geral do jogo.
    ```bash
    python observador.py
    ```

4.  **Terminal 3: Jogador 1**
    * O script `jogador.py` precisa de um ID como argumento.
    ```bash
    python jogador.py jogador1
    ```

5.  **Terminal 4: Jogador 2**
    * Ao iniciar o segundo jogador, o jogo começará automaticamente.
    ```bash
    python jogador.py jogador2
    ```

## 👨‍💻 Autor

* **Pedro Galeano** - [pedrogaleano15](https://github.com/pedrogaleano15)
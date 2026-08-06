# Sistemas Distribuídos — Projetos Práticos

Coleção de projetos desenvolvidos na disciplina de Sistemas Distribuídos durante a graduação em Engenharia da Computação na UCDB. Abrange implementações com diferentes tecnologias e paradigmas de comunicação distribuída: RMI (Java), RPC (Pyro5/Python) e MQTT (Pygame/Python).

---

## Projetos

### CalculadorRMI — Calculadora Distribuída com RMI
Aplicação de **calculadora remota** usando Java RMI (Remote Method Invocation). O cliente invoca operações matemáticas (`add`, `sub`, `mul`, `div`) em um servidor remoto de forma transparente, como se fossem chamadas locais.

**Conceitos:** RMI, stub/skeleton, registro de objetos remotos (RMI Registry), serialização Java.

```
Tecnologias: Java, Maven
```

Compilar e executar (veja detalhes em `CalculadorRMI/README.md`):
```bash
cd CalculadorRMI
mvn clean compile
java -cp target/classes Calculadora.Servidor   # Terminal 1
java -cp target/classes Calculadora.Cliente    # Terminal 2
```

---

### CriptoRMI — Criptografia via RMI
Serviço distribuído de **criptografia e descriptografia** (Base64) implementado com Java RMI. O cliente envia texto para o servidor, que aplica a codificação e retorna o resultado.

**Conceitos:** RMI, auto-registro do RMI Registry, comunicação cliente-servidor em sistemas distribuídos.

```
Tecnologias: Java
```

```bash
cd CriptoRMI
javac -d build/classes src/cripto/*.java
java -cp build/classes cripto.Servidor   # Terminal 1
java -cp build/classes cripto.Cliente    # Terminal 2
```

---

### chat_RMI — Chat Distribuído com RMI, JavaFX e SQLite (MVC)
Sistema de **chat distribuído** com interface gráfica (JavaFX), onde múltiplos clientes trocam mensagens (broadcast ou privadas, `@usuario mensagem`) através de um servidor RMI central. Todas as mensagens são persistidas em SQLite para auditoria. Organizado em MVC (Modelo/Controle/Visão).

**Conceitos:** RMI, callbacks remotos (push de mensagens para o cliente), concorrência, persistência com JDBC/SQLite, arquitetura MVC.

```
Tecnologias: Java, JavaFX, SQLite (JDBC)
```

Requer o JDK 25+ e o JavaFX SDK 25.0.1 baixado à parte (não incluído no repositório). Veja o passo a passo completo em `chat_RMI/README.md`.

---

### servidor_com_pyro — Calculadora Distribuída com Pyro5
Serviço de RPC em Python usando **Pyro5** (Python Remote Objects). O servidor expõe um objeto `calculador` (`add`, `sub`, `mul`, `div`) registrado em um name server; o cliente localiza o objeto e chama seus métodos remotamente.

**Conceitos:** RPC em Python, name server Pyro, objetos remotos via proxy.

```
Tecnologias: Python, Pyro5
```

```bash
cd servidor_com_pyro
pip install -r requirements.txt
pyro5-ns              # Terminal 1: name server
python servidor.py    # Terminal 2
python cliente.py     # Terminal 3
```

---

### Exemplo_jogo — Jogo Multiplayer com Pygame e MQTT
Protótipo simples de jogo multiplayer (dois círculos se movendo em tela) onde a posição de cada jogador é publicada e assinada via um broker MQTT (Mosquitto), demonstrando comunicação em tempo real entre processos.

**Conceitos:** publish/subscribe, broker MQTT, estado replicado entre clientes.

```
Tecnologias: Python, Pygame, paho-mqtt, Mosquitto
```

```bash
cd Exemplo_jogo
pip install -r requirements.txt
python jogo.py           # Terminal 1: Jogador 1
python jogo.py player2   # Terminal 2: Jogador 2
```

---

### Jogo_espacial — Jogo Espacial Multiplayer com MQTT
Evolução do jogo anterior: um "space shooter" multiplayer completo (movimento, tiros, colisões, pontuação e vitória) com estado sincronizado entre jogadores via MQTT, além de um serviço separado que gera obstáculos e um cliente "observador" somente leitura.

**Conceitos:** publish/subscribe, múltiplos componentes distribuídos independentes (jogador, gerador de obstáculos, observador), sincronização de estado em tempo real.

```
Tecnologias: Python, Pygame, paho-mqtt, Mosquitto
```

```bash
cd Jogo_espacial
pip install -r requirements.txt
python gerador_obstaculo.py   # Terminal 1
python observador.py          # Terminal 2 (opcional)
python jogador.py jogador1    # Terminal 3
python jogador.py jogador2    # Terminal 4
```

---

## Tecnologias

![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

**Protocolos & Tecnologias:** Java RMI · Pyro5 (RPC) · MQTT · JavaFX · SQLite

---

## Como clonar

```bash
git clone https://github.com/pedrogaleano15/SistemaDistribuidos.git
cd SistemaDistribuidos
```

Cada subpasta é um projeto independente, com seu próprio README contendo instruções detalhadas de compilação e execução.

---

## O que aprendi

- Diferença entre comunicação síncrona (RMI, RPC) e assíncrona (MQTT pub/sub)
- Como Java RMI abstrai a comunicação de rede via interfaces remotas
- Exposição de objetos Python como serviços remotos com Pyro5
- Desafios de sincronização de estado em sistemas com múltiplos clientes
- Persistência e auditoria em um sistema distribuído (chat_RMI + SQLite)

---

## Autor

**Pedro Henrique Morais Galeano**
Engenharia da Computação · UCDB · Campo Grande/MS
[GitHub](https://github.com/pedrogaleano15) · [LinkedIn](https://www.linkedin.com/in/pedro-henrique-morais-galeano)

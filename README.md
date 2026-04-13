# Sistemas Distribuídos — Projetos Práticos

Coleção de projetos desenvolvidos na disciplina de Sistemas Distribuídos durante a graduação em Engenharia da Computação na UCDB. Abrange implementações com diferentes tecnologias e paradigmas de comunicação distribuída.

---

## Projetos

### ServidorTCP — Servidor/Cliente TCP em C++
Implementação de um servidor e cliente utilizando **sockets TCP** em C++. O servidor aceita conexões simultâneas de múltiplos clientes e processa requisições em tempo real.

**Conceitos:** sockets BSD, protocolo TCP/IP, comunicação cliente-servidor, multiplexação de conexões.

```
Tecnologias: C++
```

---

### CalculadoraRMI / CalculadorRMI — Calculadora Distribuída com RMI
Aplicação de **calculadora remota** usando Java RMI (Remote Method Invocation). O cliente invoca operações matemáticas em um servidor remoto de forma transparente, como se fossem chamadas locais.

**Conceitos:** RMI, stub/skeleton, registro de objetos remotos, serialização Java.

```
Tecnologias: Java
```

---

### CriptoRMI — Criptografia via RMI
Serviço distribuído de **criptografia e descriptografia** implementado com Java RMI. O cliente envia texto para o servidor, que aplica algoritmos de cifra e retorna o resultado.

**Conceitos:** RMI, criptografia simétrica, comunicação segura em sistemas distribuídos.

```
Tecnologias: Java
```

---

### chat\_RMI — Chat em Tempo Real com RMI
Sistema de **chat distribuído** onde múltiplos clientes se comunicam através de um servidor RMI. Implementa padrão observer para notificação de mensagens em tempo real.

**Conceitos:** RMI, padrão Observer, concorrência, broadcast de mensagens.

```
Tecnologias: Java
```

---

### servidor\_com\_pyro — Servidor com Pyro5
Servidor de objetos remotos utilizando **Pyro5** (Python Remote Objects). Demonstra como expor objetos Python como serviços distribuídos acessíveis via rede.

**Conceitos:** RPC em Python, name server Pyro, objetos remotos.

```bash
pip install Pyro5
python servidor_com_pyro/servidor.py
```

```
Tecnologias: Python, Pyro5
```

---

### Jogo\_espacial — Jogo Espacial Distribuído
Jogo com componentes distribuídos, onde o estado do jogo é gerenciado de forma centralizada e compartilhado entre os clientes conectados.

**Conceitos:** estado compartilhado, sincronização, comunicação em tempo real.

```
Tecnologias: C++
```

---

## Tecnologias

![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=c%2B%2B&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

**Protocolos & Tecnologias:** TCP/IP · Java RMI · Pyro5 · Sockets

---

## Como clonar

```bash
git clone https://github.com/pedrogaleano15/SistemaDistribuidos.git
cd SistemaDistribuidos
```

Cada subpasta contém o projeto independente. Consulte os comentários no código para instruções de execução de cada um.

---

## O que aprendi

- Diferença entre comunicação síncrona (RMI, TCP) e assíncrona
- Como Java RMI abstrai a comunicação de rede via interfaces
- Implementação de sockets de baixo nível em C++
- Exposição de objetos Python como serviços remotos com Pyro5
- Desafios de sincronização em sistemas com múltiplos clientes

---

## Autor

**Pedro Henrique Morais Galeano**  
Engenharia da Computação · UCDB · Campo Grande/MS  
[GitHub](https://github.com/pedrogaleano15) · [LinkedIn](www.linkedin.com/in/pedro-henrique-morais-galeano)

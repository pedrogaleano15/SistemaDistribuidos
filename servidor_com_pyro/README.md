# Calculadora Distribuída com Pyro5

Este projeto é uma demonstração simples de Chamada de Procedimento Remoto (RPC) utilizando a biblioteca `Pyro5` (Python Remote Objects).

O sistema é composto por um servidor que expõe um objeto `calculador` e um cliente que consome os métodos desse objeto (`add`, `sub`, `mul`, `div`) como se fossem locais.

## 🏗️ Arquitetura

1.  **Servidor de Nomes (Name Server):** O Pyro5 utiliza um "servidor de nomes" (`pyro5-ns`) que funciona como uma lista telefônica. Os servidores registram seus objetos nele com um nome (ex: "calculadora").
2.  **`servidor.py` (Servidor):**
    * Define a classe `calculador` com os métodos a serem expostos.
    * Conecta-se ao Servidor de Nomes.
    * Registra uma instância da `calculador` com o nome "calculadora".
    * Fica ativo esperando por chamadas.
3.  **`cliente.py` (Cliente):**
    * Conecta-se ao Servidor de Nomes.
    * Procura pelo objeto "calculadora".
    * Cria um *Proxy* para o objeto remoto e chama seus métodos.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **[Pyro5](https://pyro5.readthedocs.io/en/latest/)**: Biblioteca para facilitar a criação de aplicações com objetos distribuídos em Python.

## 📦 Instalação

1.  **Clone o repositório e entre na pasta:**
    ```bash
    git clone [https://github.com/pedrogaleano15/SistemaDistribuidos.git](https://github.com/pedrogaleano15/SistemaDistribuidos.git)
    cd SistemaDistribuidos/servidor_com_pyro
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

Para rodar este projeto, você precisará de **3 terminais separados**, todos com o ambiente virtual ativado.

**⚠️ IMPORTANTE:** Os scripts estão com o IP `172.31.15.125` fixo (hardcoded). Para testar localmente na sua máquina, **substitua o IP `172.31.15.125` por `localhost`** nos arquivos `servidor.py` e `cliente.py`.

---
**Terminal 1: Iniciar o Servidor de Nomes (Name Server)**
(Não se esqueça de ativar o `.venv` primeiro!)

```bash
pyro5-ns
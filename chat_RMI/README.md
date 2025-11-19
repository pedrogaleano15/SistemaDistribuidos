# 💬 Sistema de Chat Distribuído com Java RMI e JavaFX (MVC)

Este projeto implementa um sistema de chat distribuído simples no modelo **Cliente/Servidor** utilizando **Java RMI (Remote Method Invocation)** para a comunicação e **JavaFX** para a interface gráfica, seguindo a arquitetura **MVC (Modelo, Controle, Visão)**.

O servidor atua como um nó central, responsável pelo registro de clientes e pelo *broadcast* (distribuição) de mensagens.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Java (JDK 25 ou superior)
* **Comunicação Distribuída:** Java RMI (Remote Method Invocation)
* **Interface Gráfica:** JavaFX (SDK 25.0.1 ou versão compatível com seu JDK)
* **Arquitetura:** MVC (Modelo, Controle, Visão)
* **Auditoria (Opcional):** SQLite JDBC (para persistência de mensagens)

---

## 📁 Estrutura do Projeto (MVC)

A lógica do sistema é rigidamente separada em três camadas dentro do pacote `chat`:

/src/chat ├── Controle/ # Camada de CONTROLE: Gerencia a lógica da aplicação e a interação entre Modelo e Visão. │ └── ChatController.java ├── Modelo/ # Camada de MODELO: Contém a lógica de negócio (RMI, IServer, IClient) e o estado do sistema. │ └── ClienteChat.java, ServidorChat.java, IServer.java, IClient.java └── visao/ # Camada de VISÃO: Lida com a apresentação dos dados (Interface JavaFX). └── ClienteChatV.java


---

## 🚀 Como Compilar e Executar

A compilação e execução exigem a instalação do **Java Development Kit (JDK 25+)** e o **JavaFX SDK 25.0.1**.

### 1. Configuração do Classpath (Para Auditoria)

Se você incluiu o módulo de Auditoria com SQLite (próximo passo), o driver (`sqlite-jdbc-3.44.1.0.jar`) deve estar na pasta `lib/`.

### 2. Compilação (Apenas para Recompilar)

O comando deve incluir o caminho do JavaFX SDK. Execute-o a partir da pasta `/chat_RMI`:

```bash
# Compilação: Aponta para a pasta 'lib' do JavaFX SDK
javac --module-path "[CAMINHO_DO_FX_SDK]\lib" --add-modules javafx.controls,javafx.fxml,javafx.graphics -encoding UTF-8 -d bin src/chat/Modelo/*.java src/chat/Controle/*.java src/chat/visao/*.java
3. Execução (Três Terminais)
Passo A: Iniciar o Servidor RMI (Terminal 1)
O servidor inicia o RMI Registry.

Bash

java -cp bin chat.Modelo.ServidorChat
(Se usar o SQLite, o comando deve ser: java -cp "bin;lib/sqlite-jdbc-3.44.1.0.jar" chat.Modelo.ServidorChat)

Passo B: Iniciar os Clientes (Terminal 2 e 3)
Execute o comando do cliente, substituindo [CAMINHO_DO_FX_SDK] pelo caminho correto (ex: C:\Program Files\Java\javafx-sdk-25.0.1).

Bash

# Execução do Cliente: Aponta para os módulos JavaFX
java --module-path "[CAMINHO_DO_FX_SDK]\lib" --add-modules javafx.controls,javafx.fxml,javafx.graphics -cp bin chat.visao.ClienteChatV
💡 Funcionalidades do Chat
Registro Único: O sistema impede que dois clientes usem o mesmo nome.

Broadcast: Mensagens enviadas sem prefixo vão para todos os clientes conectados.

Mensagem Privada: Use o formato @nome_usuario sua mensagem para envio privado.
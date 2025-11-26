# 💬 Sistema de Chat Distribuído com Java RMI, JavaFX e SQLite (MVC)

Este projeto implementa um sistema de chat distribuído completo utilizando **Java RMI** para comunicação em rede, **JavaFX** para a interface gráfica e **SQLite** para auditoria de mensagens. O projeto segue rigorosamente a arquitetura **MVC (Modelo, Controle, Visão)**.

## 📋 Funcionalidades

* **Arquitetura Cliente/Servidor:** Servidor centralizado com múltiplos clientes.
* **RMI (Remote Method Invocation):** Comunicação transparente entre objetos distribuídos.
* **Interface Gráfica (GUI):** Desenvolvida com JavaFX.
* **Auditoria:** Todas as mensagens trocadas são salvas automaticamente em um banco de dados SQLite local (`chat_auditoria.db`).
* **Mensagens Privadas:** Suporte para envio direto (`@usuario mensagem`).
* **Broadcast:** Mensagens enviadas para todos os conectados.

---

## 🛠️ Pré-requisitos e Configuração

Para executar este projeto, você precisará de:

1.  **Java Development Kit (JDK) 25** (ou superior).
2.  **JavaFX SDK 25.0.1** (Descompactado na raiz do projeto ou em local acessível).
3.  **Driver SQLite JDBC:** O arquivo `.jar` já está incluído na pasta `lib/` deste repositório.

### ⚠️ Configuração de Rede (Importante)

O sistema foi configurado com um **IP Fixo** para o Servidor.
* **IP do Servidor:** `seu ip`
* Se você for rodar em outra rede, altere o IP nos arquivos `src/chat/Modelo/ServidorChat.java` e `src/chat/visao/ClienteChatV.java` e recompile.

---

## 🚀 Como Compilar e Executar (Windows/PowerShell)

Certifique-se de estar na pasta raiz do projeto (`chat_RMI`).

### 1. Compilação

```powershell
javac --module-path "javafx-sdk-25.0.1\lib" --add-modules javafx.controls,javafx.fxml,javafx.graphics -encoding UTF-8 -d bin src/chat/Modelo/*.java src/chat/Controle/*.java src/chat/visao/*.java
2. Executar o Servidor (Máquina seu ip)
O servidor inicia o Registry automaticamente e cria o banco de dados de auditoria.

PowerShell

java "-Djava.rmi.server.hostname=seu ip" -cp "bin;lib/*" chat.Modelo.ServidorChat
3. Executar Clientes (Qualquer Máquina)
Os clientes se conectam ao IP 192.168.100.7. Certifique-se de usar nomes de usuário diferentes para cada cliente.

PowerShell

java --module-path "javafx-sdk-25.0.1\lib" --add-modules javafx.controls,javafx.fxml,javafx.graphics -cp "bin;lib/*" chat.visao.ClienteChatV
📁 Estrutura do Projeto
/chat_RMI
├── lib/                     # Dependências (Driver SQLite)
├── javafx-sdk-25.0.1/       # SDK do JavaFX
├── chat_auditoria.db        # Banco de dados (gerado automaticamente)
├── src/chat/
│   ├── Modelo/              # Lógica de Negócio, RMI e Banco de Dados
│   ├── Controle/            # Controlador (Ponte entre View e Model)
│   └── visao/               # Interface Gráfica
└── bin/                     # Binários compilados
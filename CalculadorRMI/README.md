# Calculadora Distribuída com Java RMI

Este é um projeto simples que demonstra o uso de Invocação de Método Remoto (RMI) em Java para criar uma calculadora distribuída.

O sistema consiste em:
* Uma interface remota (`Calculadora.java`) definindo as operações.
* Uma implementação no servidor (`rmi.java`) que realiza os cálculos.
* Um `Servidor.java` que instancia o objeto da calculadora e **inicia o RMI Registry** na porta 1099.
* Um `Cliente.java` que localiza o serviço remoto e invoca os métodos.

## Tecnologias Utilizadas

* **Java** (JDK 17)
* **Java RMI** (Remote Method Invocation)
* **Maven** (Para compilação)

## Estrutura do Projeto (Maven)

CalculadoraRMI/ ├── src/ │ ├── main/ │ │ └── java/ │ │ └── Calculadora/ │ │ ├── Calculadora.java # Interface Remota │ │ ├── Cliente.java # Aplicação Cliente │ │ ├── rmi.java # Implementação │ │ └── Servidor.java # Aplicação Servidor (inicia o Registry) ├── pom.xml # Configuração do Maven └── README.md # Este arquivo └── .gitignore # Arquivos ignorados pelo Git


## Requisitos

* JDK (Java Development Kit) versão 17 (ou compatível) instalado e configurado no PATH.
* Apache Maven instalado e configurado no PATH.

## Compilação

Navegue até a pasta `CalculadoraRMI` no terminal e execute o comando Maven para compilar o projeto:

```bash
mvn clean compile
Isso criará os arquivos .class na pasta target/classes/.

Execução (Apenas 2 Terminais)
A execução requer dois terminais separados abertos na pasta CalculadoraRMI.

⚠️ IMPORTANTE (IP e Firewall):

Os arquivos .java deste projeto estão configurados para usar o IP fixo 192.168.100.48. Se o seu IP mudar, você precisará atualizar os arquivos Servidor.java e Cliente.java e recompilar o projeto.

Ao executar o Servidor, o Firewall do Windows provavelmente pedirá permissão. Você DEVE "Permitir acesso" para que o Cliente possa se conectar.

Terminal 1: Iniciar o Servidor (e o Registry)

O Servidor.java foi programado para iniciar o RMI Registry e registrar a calculadora automaticamente.

Bash

# Navegue até a pasta CalculadorRMI
cd caminho/para/SistemaDistribuidos/CalculadorRMI

# Execute a classe Servidor
java -cp target/classes Calculadora.Servidor
(Você deverá ver as mensagens "RMI Registry iniciado..." e "Servidor da Calculadora pronto..."). Deixe este terminal rodando.

Terminal 2: Iniciar o Cliente

Abra um novo terminal.

Bash

# Navegue até a pasta CalculadoraRMI
cd caminho/para/SistemaDistribuidos/CalculadorRMI

# Execute a classe Cliente
java -cp target/classes Calculadora.Cliente
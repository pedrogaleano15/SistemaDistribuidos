<div align="center">

CriptoRMI 🔐
Serviço de Criptografia com Java RMI

Um projeto de exemplo simples em Java que demonstra o uso de RMI (Remote Method Invocation) para criar um serviço distribuído de criptografia (usando Base64).

</div>

✨ Recursos
 . Serviço Remoto: Um servidor RMI que expõe métodos de criptografia.

 . Cliente Interativo: Um cliente de console que permite ao usuário:

  . Criptografar uma mensagem (string para Base64).

  . Decriptografar uma mensagem (Base64 para string).

 . Auto-registro: O servidor inicia seu próprio registro RMI, simplificando a execução.

⚙️ Como Funciona
1. A interface ICripto.java define o "contrato" remoto.

2. O Servidor.java inicia, cria uma instância do CriptoImpl.java (a lógica real) e a registra no RMI Registry (que ele mesmo inicia na porta 1099).

3. O Cliente.java se conecta ao RMI Registry no localhost, "procura" pelo serviço e obtém um stub (objeto de proxy).

4. Quando o cliente chama servico.criptografar(), o RMI cuida de enviar a chamada pela rede, executar o método no servidor e retornar o resultado.

🚀 Requisitos
 .Java: Recomenda-se a versão 8 ou superior do JDK (Java Development Kit) (devido ao uso da biblioteca java.util.Base64).

 . Bibliotecas: Nenhuma biblioteca externa (arquivos .jar) é necessária. O projeto utiliza apenas as bibliotecas padrão do JDK.

📂 Estrutura do Projeto
CriptoRMI/
├── build/
│   └── classes/    # Onde os arquivos compilados (.class) são armazenados
└── src/
    └── cripto/     # Pacote principal do código-fonte
        ├── ICripto.java      # A interface RMI (o "contrato")
        ├── CriptoImpl.java   # A implementação real do serviço
        ├── Servidor.java     # O programa que inicia o servidor
        └── Cliente.java      # O programa cliente que consome o serviço


💻 Como Compilar

 1. Abra seu terminal e navegue (cd) até a pasta raiz do seu projeto (a pasta CriptoRMI que contém este README.md).

 2. Execute o comando javac para compilar todos os arquivos-fonte e salvar os arquivos .class na pasta build/classes:

 No Windows (PowerShell/CMD):

 javac -d build\classes src\cripto\ICripto.java src\cripto\CriptoImpl.java src\cripto\Servidor.java src\cripto\Cliente.java

 No Linux/macOS:

 javac -d build/classes src/cripto/*.java

▶️ Como Executar
Após a compilação, você precisará de dois terminais para rodar a aplicação.

 Importante: Este projeto não requer a execução do comando rmiregistry separadamente. O próprio Servidor.java já inicializa o registro RMI na porta 1099, tornando o processo mais simples.

🖥️ Terminal 1: Iniciar o Servidor
 1. No seu primeiro terminal, navegue (cd) até a pasta build/classes que foi criada dentro do seu projeto:

 No Windows:

 cd C:\caminho\completo\para\seu\projeto\CriptoRMI\build\classes
 
 No Linux/macOS:

 cd /caminho/completo/para/seu/projeto/CriptoRMI/build/classes

 2. Inicie o programa Servidor (note o uso de cripto.Servidor para especificar o pacote):

 java cripto.Servidor

 3. Você deverá ver as seguintes mensagens, indicando que o servidor está pronto:

 RMI Registry iniciado.
 Servidor: Serviço 'ServicoCripto' registrado e pronto.

 4. Deixe este terminal aberto! Ele é o seu servidor.

⌨️ Terminal 2: Iniciar o Cliente
 1. Abra um segundo terminal.

 2. Navegue (cd) até a mesma pasta build/classes:

 No Windows:

 cd C:\caminho\completo\para\seu\projeto\CriptoRMI\build\classes
 
 No Linux/macOS:

 cd /caminho/completo/para/seu/projeto/CriptoRMI/build/classes
 
 3. Inicie o programa Cliente:

 java cripto.Cliente
 
 4. O cliente irá se conectar ao servidor e mostrar o menu interativo:

 Cliente: Conectado ao Servidor RMI.

 --- MENU ---
 1. Criptografar Mensagem
 2. Decriptografar Mensagem
 3. Sair
 Escolha uma opção: 
 
 5. Agora você pode usar a aplicação! As mensagens que você digitar no Cliente aparecerão no console do Servidor.
package chat.visao;

import chat.Controle.ChatController;
import chat.Modelo.ClienteChat;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import java.util.Optional;

public class ClienteChatV extends Application {

    private static final String HOST = "localhost";
    private static final int PORTA_RMI = 1099;
    
    private ChatController controller; 
    
    private TextArea areaChat;
    private TextField campoMensagem;

    @Override
    public void start(Stage primaryStage) {
        Optional<String> resultado = pedirNomeUsuario();
        if (!resultado.isPresent() || resultado.get().trim().isEmpty()) {
            Platform.exit();
            return;
        }
        
        String nomeUsuario = resultado.get().trim();
        
        try {
            // 1. Inicializa o Modelo e o Controlador
            ClienteChat model = new ClienteChat(nomeUsuario);
            controller = new ChatController(model, this); 
            
            // --- Configuração da Interface JavaFX (Inicializa os componentes) ---
            primaryStage.setTitle("Chat RMI (MVC) - " + nomeUsuario);
            
            areaChat = new TextArea();
            areaChat.setEditable(false);
            areaChat.setWrapText(true);

            campoMensagem = new TextField();
            campoMensagem.setPromptText("Digite sua mensagem (@nome para privado)...");
            Button botaoEnviar = new Button("Enviar");
            
            botaoEnviar.setOnAction(e -> processarEnvio());
            campoMensagem.setOnKeyPressed(event -> {
                if (event.getCode() == KeyCode.ENTER) {
                    processarEnvio();
                }
            });

            HBox painelEntrada = new HBox(5, campoMensagem, botaoEnviar);
            HBox.setHgrow(campoMensagem, Priority.ALWAYS);

            VBox layoutPrincipal = new VBox(10, new Label("Bem-vindo ao Chat!"), areaChat, painelEntrada);
            layoutPrincipal.setPadding(new javafx.geometry.Insets(10));
            VBox.setVgrow(areaChat, Priority.ALWAYS);

            Scene scene = new Scene(layoutPrincipal, 500, 400);
            primaryStage.setScene(scene);
            
            // Trata o fechamento da janela via Controlador
            primaryStage.setOnCloseRequest(e -> {
                controller.fecharAplicacao();
            });
            
            primaryStage.show();

            // 2. CORREÇÃO FINAL: Inicia a Conexão RMI APÓS a GUI ser exibida (start concluído)
            controller.iniciarConexao(nomeUsuario, HOST, PORTA_RMI);

        } catch (Exception e) {
            mostrarAlerta("Erro Crítico", "Falha ao iniciar o sistema: " + e.getMessage());
            Platform.exit();
        }
    }
    
    private Optional<String> pedirNomeUsuario() {
        TextInputDialog dialog = new TextInputDialog();
        dialog.setTitle("Conexão ao Chat");
        dialog.setHeaderText("Digite seu nome de usuário para entrar no Chat RMI.");
        dialog.setContentText("Nome:");
        return dialog.showAndWait();
    }
    
    private void processarEnvio() {
        String mensagem = campoMensagem.getText();
        if (mensagem.trim().isEmpty()) return;
        
        controller.enviarMensagem(mensagem); 
        campoMensagem.setText("");
    }

    public void mostrarMensagem(String mensagem) {
        areaChat.appendText(mensagem + "\n");
    }
    
    public void fecharGUI() {
        Platform.exit();
        System.exit(0);
    }
    
    public void mostrarAlerta(String titulo, String cabecalho) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(titulo);
        alert.setHeaderText(cabecalho);
        alert.showAndWait();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
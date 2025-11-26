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

    // IP FIXO DO SERVIDOR
    private static final String HOST = "192.168.100.7"; 
    private static final int PORTA_RMI = 1099;
    
    private ChatController controller; 
    private TextArea areaChat;
    private TextField campoMensagem;

    @Override
    public void start(Stage primaryStage) {
        Optional<String> resultado = pedirNomeUsuario();
        if (resultado.isEmpty() || resultado.get().trim().isEmpty()) {
            Platform.exit(); return;
        }
        String nomeUsuario = resultado.get().trim();
        
        try {
            // Inicialização MVC
            ClienteChat model = new ClienteChat(nomeUsuario);
            controller = new ChatController(model, this); 
            
            // GUI
            primaryStage.setTitle("Chat Distribuído - " + nomeUsuario);
            
            areaChat = new TextArea();
            areaChat.setEditable(false);
            areaChat.setWrapText(true);

            campoMensagem = new TextField();
            campoMensagem.setPromptText("Digite sua mensagem...");
            Button botaoEnviar = new Button("Enviar");
            
            botaoEnviar.setOnAction(e -> processarEnvio());
            campoMensagem.setOnKeyPressed(event -> {
                if (event.getCode() == KeyCode.ENTER) processarEnvio();
            });

            HBox painelEntrada = new HBox(5, campoMensagem, botaoEnviar);
            HBox.setHgrow(campoMensagem, Priority.ALWAYS);
            VBox layout = new VBox(10, new Label("Bem-vindo(a) " + nomeUsuario), areaChat, painelEntrada);
            layout.setPadding(new javafx.geometry.Insets(10));
            VBox.setVgrow(areaChat, Priority.ALWAYS);

            primaryStage.setScene(new Scene(layout, 500, 400));
            primaryStage.setOnCloseRequest(e -> controller.fecharAplicacao());
            primaryStage.show();

            // CONEXÃO APÓS GUI ESTAR PRONTA (Evita o NullPointerException)
            controller.iniciarConexao(nomeUsuario, HOST, PORTA_RMI);

        } catch (Exception e) {
            mostrarAlerta("Erro Crítico", "Falha ao iniciar: " + e.getMessage());
            Platform.exit();
        }
    }
    
    private Optional<String> pedirNomeUsuario() {
        TextInputDialog dialog = new TextInputDialog();
        dialog.setTitle("Login");
        dialog.setHeaderText("Entre com seu nome:");
        return dialog.showAndWait();
    }
    
    private void processarEnvio() {
        controller.enviarMensagem(campoMensagem.getText()); 
        campoMensagem.clear();
    }

    public void mostrarMensagem(String msg) {
        areaChat.appendText(msg + "\n");
    }
    
    public void fecharGUI() {
        Platform.exit(); System.exit(0);
    }
    
    public void mostrarAlerta(String titulo, String msg) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(titulo);
        alert.setContentText(msg);
        alert.showAndWait();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
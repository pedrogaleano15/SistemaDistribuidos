package chat.Controle;

import chat.Modelo.ClienteChat;
import chat.Modelo.IServer;
import chat.visao.ClienteChatV;

import java.rmi.NotBoundException;
import java.rmi.RemoteException;

public class ChatController {

    private ClienteChat model; // Referência ao Modelo
    private ClienteChatV view; // Referência à Visão
    
    public ChatController(ClienteChat model, ClienteChatV view) {
        this.model = model;
        this.view = view;
        
        // Passa a referência da Visão para o Modelo para o Callback.
        this.model.setGUI(view);
    }
    
    // Inicia a conexão RMI no Modelo.
    public void iniciarConexao(String nomeUsuario, String host, int porta) throws RemoteException, NotBoundException {
        this.model.conectar(host, porta);
        view.mostrarMensagem("--- Conectado ao Servidor RMI como " + nomeUsuario + " ---");
    }
    
    // Trata a ação do usuário de enviar uma mensagem.
    public void enviarMensagem(String mensagem) {
        if (mensagem.trim().isEmpty()) return;

        try {
            String nomeUsuario = model.getNomeUsuario();
            IServer servidorProxy = model.getServidorProxy();

            if (mensagem.startsWith("@")) {
                // Mensagem Privada
                String[] partes = mensagem.split(" ", 2);
                if (partes.length == 2) {
                    String destinatario = partes[0].substring(1);
                    String conteudo = partes[1];
                    servidorProxy.enviarMensagem(nomeUsuario, conteudo, destinatario);
                } else {
                    view.mostrarMensagem("*** Formato privado inválido. Use: @nome_usuario sua mensagem ***");
                }
            } else {
                // Broadcast
                servidorProxy.enviarMensagem(nomeUsuario, mensagem, null);
            }
            
        } catch (RemoteException e) {
            view.mostrarAlerta("Erro de Comunicação", "Conexão perdida com o servidor: " + e.getMessage());
            model.desconectar();
        }
    }
    
    // Trata o fechamento da janela.
    public void fecharAplicacao() {
        model.desconectar();
        view.fecharGUI();
    }
}
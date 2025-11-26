package chat.Controle;

import chat.Modelo.ClienteChat;
import chat.Modelo.IServer;
import chat.visao.ClienteChatV;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;

public class ChatController {

    private ClienteChat model;
    private ClienteChatV view;
    
    public ChatController(ClienteChat model, ClienteChatV view) {
        this.model = model;
        this.view = view;
        this.model.setGUI(view);
    }
    
    public void iniciarConexao(String nomeUsuario, String host, int porta) throws RemoteException, NotBoundException {
        this.model.conectar(host, porta);
        view.mostrarMensagem("--- Conectado ao Servidor RMI (" + host + ") ---");
    }
    
    public void enviarMensagem(String mensagem) {
        if (mensagem.trim().isEmpty()) return;

        try {
            String nomeUsuario = model.getNomeUsuario();
            IServer servidorProxy = model.getServidorProxy();

            if (mensagem.startsWith("@")) {
                String[] partes = mensagem.split(" ", 2);
                if (partes.length == 2) {
                    servidorProxy.enviarMensagem(nomeUsuario, partes[1], partes[0].substring(1));
                } else {
                    view.mostrarMensagem("Erro: Use @nome mensagem");
                }
            } else {
                servidorProxy.enviarMensagem(nomeUsuario, mensagem, null);
            }
        } catch (RemoteException e) {
            view.mostrarAlerta("Erro", "Falha no envio: " + e.getMessage());
            model.desconectar();
        }
    }
    
    public void fecharAplicacao() {
        model.desconectar();
        view.fecharGUI();
    }
}
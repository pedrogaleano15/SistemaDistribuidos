package chat.Modelo;

import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import javafx.application.Platform; 
import chat.visao.ClienteChatV;

public class ClienteChat extends UnicastRemoteObject implements IClient {

    private String nomeUsuario;
    private IServer servidorProxy;
    private ClienteChatV gui; 

    // CONSTRUTOR CORRIGIDO: Deve ser public para ser acessado pela Visão/Controlador.
    public ClienteChat(String nomeUsuario) throws RemoteException {
        super();
        this.nomeUsuario = nomeUsuario;
    }

    // Conecta a instância ao RMI Registry e registra-se no Servidor.
    public void conectar(String host, int porta) throws RemoteException, NotBoundException {
        Registry registry = LocateRegistry.getRegistry(host, porta);
        servidorProxy = (IServer) registry.lookup("ChatServerService");
        
        String resultado = servidorProxy.registrarCliente(nomeUsuario, this);
        
        if (!resultado.equals("OK")) {
            throw new RemoteException(resultado);
        }
    }
    
    public void desconectar() {
         try {
            if (servidorProxy != null) {
                servidorProxy.desconectarCliente(nomeUsuario);
                UnicastRemoteObject.unexportObject(this, true); 
            }
        } catch (RemoteException e) {
            // Ignorar
        }
    }

    // CALLBACK RMI: Chamado remotamente pelo Servidor.
    @Override
    public void receberMensagem(String mensagem) throws RemoteException {
        if (gui != null) {
            // Usa Platform.runLater para garantir a atualização da GUI na thread correta.
            Platform.runLater(() -> {
                gui.mostrarMensagem(mensagem);
            });
        }
    }
    
    public void setGUI(ClienteChatV gui) {
        this.gui = gui;
    }
    public String getNomeUsuario() {
        return nomeUsuario;
    }
    public IServer getServidorProxy() {
        return servidorProxy;
    }
}
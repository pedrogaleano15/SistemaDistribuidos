package chat.Modelo;

import java.rmi.Remote;
import java.rmi.RemoteException;

// Interface para o Callback do Cliente (usada pelo Servidor)
public interface IClient extends Remote {
    
    // O Servidor chama este método remotamente para entregar uma nova mensagem ao cliente.
    void receberMensagem(String mensagem) throws RemoteException;
}
package chat.Modelo;

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

// IServer é a interface remota do servidor.
public interface IServer extends Remote {

    String registrarCliente(String nome, IClient cliente) throws RemoteException;

    void enviarMensagem(String remetente, String mensagem, String destinatario) throws RemoteException;
    
    void desconectarCliente(String nome) throws RemoteException;

    List<String> obterClientesAtivos() throws RemoteException;
}
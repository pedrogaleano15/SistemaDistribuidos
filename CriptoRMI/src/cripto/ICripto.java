// Local: CriptoRMI/src/cripto/ICripto.java
package cripto;

import java.rmi.Remote;
import java.rmi.RemoteException;

/**
 * Interface remota para o serviço de criptografia.
 */
public interface ICripto extends Remote {
    
    /**
     * Criptografa uma mensagem de texto.
     * @param textoPlano A mensagem a ser criptografada.
     * @return A mensagem criptografada (em Base64).
     * @throws RemoteException
     */
    String criptografar(String textoPlano) throws RemoteException;
    
    /**
     * Decriptografa uma mensagem.
     * @param textoCifrado A mensagem criptografada (em Base64).
     * @return A mensagem decriptografada (texto original).
     * @throws RemoteException
     */
    String decriptografar(String textoCifrado) throws RemoteException;
}
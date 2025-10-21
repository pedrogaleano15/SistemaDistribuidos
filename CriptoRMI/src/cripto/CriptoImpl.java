// Local: CriptoRMI/src/cripto/CriptoImpl.java
package cripto;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.Base64; // Importamos a biblioteca para Base64

/**
 * Implementação da interface remota ICripto.
 */
public class CriptoImpl extends UnicastRemoteObject implements ICripto {

    // Construtor padrão obrigatório
    public CriptoImpl() throws RemoteException {
        super();
    }

    @Override
    public String criptografar(String textoPlano) throws RemoteException {
        try {
            // Codifica o texto plano para Base64
            String textoCifrado = Base64.getEncoder().encodeToString(textoPlano.getBytes("UTF-8"));
            System.out.println("Servidor: Recebido '" + textoPlano + "', Criptografado para '" + textoCifrado + "'");
            return textoCifrado;
        } catch (Exception e) {
            throw new RemoteException("Erro ao criptografar: " + e.getMessage());
        }
    }

    @Override
    public String decriptografar(String textoCifrado) throws RemoteException {
         try {
            // Decodifica de Base64 para o texto original
            byte[] bytesDecodificados = Base64.getDecoder().decode(textoCifrado);
            String textoPlano = new String(bytesDecodificados, "UTF-8");
            System.out.println("Servidor: Recebido '" + textoCifrado + "', Decriptografado para '" + textoPlano + "'");
            return textoPlano;
        } catch (Exception e) {
            throw new RemoteException("Erro ao decriptografar: " + e.getMessage());
        }
    }
}
// Local: CriptoRMI/src/cripto/Servidor.java
package cripto;

import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

/**
 * Classe principal do Servidor.
 * Registra o serviço de criptografia no RMI Registry.
 */
public class Servidor {
    
    public static void main(String[] args) {
        try {
            // 1. Inicia o RMI Registry na porta 1099 (padrão)
            LocateRegistry.createRegistry(1099);
            System.out.println("RMI Registry iniciado.");

            // 2. Instancia a nossa implementação do serviço
            ICripto servico = new CriptoImpl();
            
            // 3. Registra (bind) o serviço com um nome público
            // O cliente usará este nome ("ServicoCripto") para encontrar o serviço
            Naming.rebind("rmi://localhost/ServicoCripto", servico);
            
            System.out.println("Servidor: Serviço 'ServicoCripto' registrado e pronto.");
            
        } catch (Exception e) {
            System.err.println("Erro no Servidor: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
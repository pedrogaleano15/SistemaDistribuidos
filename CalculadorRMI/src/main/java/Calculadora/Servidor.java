package Calculadora;

import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class Servidor {

    public static void main(String[] args) {
        
        // IP fixo da máquina servidora (ajuste para a sua rede)
        String seuIP = "192.168.100.48";
        
        // Define a propriedade do sistema para o RMI usar o seu IP correto
        // Isso é crucial para o rmiregistry funcionar com IPs
        System.setProperty("java.rmi.server.hostname", seuIP);

        try {
            // 1. Inicia o RMI Registry na porta padrão (1099)
            // (O Terminal 1 também precisa estar rodando o rmiregistry com este IP)
            LocateRegistry.createRegistry(1099); 
            System.out.println("RMI Registry iniciado na porta 1099.");

            // 2. Cria o objeto remoto (a calculadora)
            rmi calculadoraObj = new rmi();
            
            // 3. Define o nome do serviço usando o SEU IP
            // ** MODIFICAÇÃO IMPORTANTE AQUI **
            String nomeServico = "//" + seuIP + "/Calculadora"; 
            
            // 4. Registra o objeto no registry
            Naming.rebind(nomeServico, calculadoraObj);

            System.out.println("Servidor da Calculadora pronto. Aguardando conexões...");

        } catch (Exception e) {
            System.err.println("Erro no Servidor: " + e.getMessage());
            e.printStackTrace();
            javax.swing.JOptionPane.showMessageDialog(null, "Não conectado!\nVerifique o IP, o Firewall ou se o 'rmiregistry' está rodando corretamente.", "Erro do Servidor", javax.swing.JOptionPane.ERROR_MESSAGE);
        }
    }
}
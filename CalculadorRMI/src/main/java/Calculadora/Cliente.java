package Calculadora;

import java.rmi.Naming;
import javax.swing.JOptionPane; // Para mostrar erros

public class Cliente {

    public static void main(String[] args) {
        
        // --- MODIFICAÇÃO IMPORTANTE AQUI ---
        // Use o mesmo IP que você definiu no Servidor.java
        String ipServidor = "192.168.100.48"; 
        
        try {
            // 1. Define o nome do serviço para procurar (com o IP correto)
            String nomeServico = "//" + ipServidor + "/Calculadora";

            // 2. Procura pelo objeto remoto no RMI Registry
            System.out.println("Cliente: Procurando pelo serviço '" + nomeServico + "'...");
            Calculadora calc = (Calculadora) Naming.lookup(nomeServico);
            System.out.println("Cliente: Conectado ao servidor!");

            // 3. Usa os métodos remotos
            System.out.println("3 + 4 = " + calc.add(3, 4));
            System.out.println("3 - 4 = " + calc.sub(3, 4));
            System.out.println("3 * 4 = " + calc.mul(3, 4));
            System.out.println("3 / 4 = " + calc.div(3, 4));

        } catch (Exception e) {
            System.err.println("Erro no Cliente: " + e.getMessage());
            e.printStackTrace();
            // Mostra um erro se o cliente não conseguir encontrar o servidor
            JOptionPane.showMessageDialog(null, "Não foi possível conectar ao servidor em " + ipServidor, "Erro do Cliente", JOptionPane.ERROR_MESSAGE);
        }
    }
}
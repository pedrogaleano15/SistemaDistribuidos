// Local: CriptoRMI/src/cripto/Cliente.java
package cripto;

import java.rmi.Naming;
import java.util.Scanner;

/**
 * Classe principal do Cliente.
 * Procura pelo serviço RMI e interage com ele.
 */
public class Cliente {
    
    public static void main(String[] args) {
        try {
            // 1. Procura pelo serviço RMI no host e porta padrão
            // O nome "ServicoCripto" deve ser o mesmo usado pelo servidor
            ICripto servico = (ICripto) Naming.lookup("rmi://localhost/ServicoCripto");
            
            System.out.println("Cliente: Conectado ao Servidor RMI.");
            
            Scanner scanner = new Scanner(System.in);
            
            while(true) {
                System.out.println("\n--- MENU ---");
                System.out.println("1. Criptografar Mensagem");
                System.out.println("2. Decriptografar Mensagem");
                System.out.println("3. Sair");
                System.out.print("Escolha uma opção: ");
                
                String opcao = scanner.nextLine();
                
                if (opcao.equals("1")) {
                    System.out.print("Digite a mensagem para criptografar: ");
                    String msgOriginal = scanner.nextLine();
                    String msgCifrada = servico.criptografar(msgOriginal);
                    System.out.println(">> Resposta do Servidor (Criptografado): " + msgCifrada);

                } else if (opcao.equals("2")) {
                    System.out.print("Digite a mensagem (Base64) para decriptografar: ");
                    String msgCifrada = scanner.nextLine();
                    String msgOriginal = servico.decriptografar(msgCifrada);
                    System.out.println(">> Resposta do Servidor (Decriptografado): " + msgOriginal);

                } else if (opcao.equals("3")) {
                    System.out.println("Cliente encerrado.");
                    break;
                } else {
                    System.out.println("Opção inválida. Tente novamente.");
                }
            }
            
            scanner.close();

        } catch (Exception e) {
            System.err.println("Erro no Cliente: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
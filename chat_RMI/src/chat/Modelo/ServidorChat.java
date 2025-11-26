package chat.Modelo;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

public class ServidorChat extends UnicastRemoteObject implements IServer {
    
    private Map<String, IClient> clientesAtivos;
    private AuditService auditoria; // Serviço de auditoria
    private static final int PORTA_RMI = 1099;
    private DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss");

    protected ServidorChat() throws RemoteException {
        super();
        this.clientesAtivos = new HashMap<>();
        this.auditoria = new AuditService(); // Inicia o banco de dados
    }

    @Override
    public String registrarCliente(String nome, IClient cliente) throws RemoteException {
        if (clientesAtivos.containsKey(nome)) {
            return "Erro: O nome de usuário '" + nome + "' já está em uso.";
        }
        
        clientesAtivos.put(nome, cliente);
        System.out.println("Novo cliente conectado: " + nome);
        enviarMensagem("Servidor", "*** " + nome + " se juntou ao chat! ***", null);
        return "OK";
    }

    @Override
    public void enviarMensagem(String remetente, String mensagem, String destinatario) throws RemoteException {
        String dataHora = LocalTime.now().format(formatter);
        String msgFormatada = String.format("[%s] <%s>: %s", dataHora, remetente, mensagem);

        // 1. Grava no Banco de Dados (Auditoria)
        if (!remetente.equals("Servidor")) {
            auditoria.registrarMensagem(remetente, destinatario, mensagem);
        }

        // 2. Lógica de Envio
        if (destinatario != null && !destinatario.isEmpty()) {
            // Privado
            IClient clienteDestino = clientesAtivos.get(destinatario);
            if (clienteDestino != null) {
                clienteDestino.receberMensagem("[PRIVADO] " + msgFormatada);
                if (!remetente.equals("Servidor") && clientesAtivos.containsKey(remetente)) {
                    clientesAtivos.get(remetente).receberMensagem("[Você para " + destinatario + "] " + msgFormatada);
                }
            }
        } else {
            // Broadcast
            System.out.println("Broadcast: " + msgFormatada);
            for (Map.Entry<String, IClient> entry : new HashMap<>(clientesAtivos).entrySet()) {
                try {
                    entry.getValue().receberMensagem(msgFormatada);
                } catch (RemoteException e) {
                    System.err.println("Cliente " + entry.getKey() + " falhou. Removendo.");
                    clientesAtivos.remove(entry.getKey());
                }
            }
        }
    }

    @Override
    public void desconectarCliente(String nome) throws RemoteException {
        if (clientesAtivos.containsKey(nome)) {
            clientesAtivos.remove(nome);
            System.out.println("Cliente desconectado: " + nome);
            enviarMensagem("Servidor", "*** " + nome + " saiu do chat. ***", null);
        }
    }
    
    @Override
    public List<String> obterClientesAtivos() throws RemoteException {
        return new ArrayList<>(clientesAtivos.keySet());
    }

    public static void main(String[] args) {
        try {
            // --- CONFIGURAÇÃO AUTOMÁTICA ---
            // 1. Define o IP fixo da máquina servidora
            System.setProperty("java.rmi.server.hostname", "192.168.100.7");

            // 2. CRIA o Registry aqui mesmo (não precisa rodar rmiregistry separado)
            Registry registry = LocateRegistry.createRegistry(PORTA_RMI);
            
            // 3. Cria e registra o servidor
            ServidorChat server = new ServidorChat();
            registry.rebind("ChatServerService", server);

            System.out.println("--- Servidor do Chat RMI Iniciado ---");
            System.out.println("Registry rodando na porta " + PORTA_RMI);
            System.out.println("IP do Servidor: 192.168.100.7");
            System.out.println("Banco de Dados: Ativo (SQLite)");

        } catch (Exception e) {
            System.err.println("Erro no servidor: " + e.toString());
            e.printStackTrace();
        }
    }
}
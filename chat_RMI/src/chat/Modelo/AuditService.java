package chat.Modelo;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class AuditService {

    // Cria o arquivo de banco de dados na raiz do projeto
    private static final String URL_DB = "jdbc:sqlite:chat_auditoria.db";
    private DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public AuditService() {
        criarTabela();
    }

    private Connection conectar() throws SQLException {
        return DriverManager.getConnection(URL_DB);
    }

    private void criarTabela() {
        String sql = "CREATE TABLE IF NOT EXISTS mensagens ("
                   + "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   + "timestamp TEXT NOT NULL,"
                   + "remetente TEXT NOT NULL,"
                   + "destinatario TEXT,"
                   + "conteudo TEXT NOT NULL"
                   + ");";
        
        try (Connection conn = conectar();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.execute();
            System.out.println("Auditoria: Tabela verificada/criada com sucesso.");
        } catch (SQLException e) {
            System.err.println("Auditoria: Erro ao criar tabela: " + e.getMessage());
        }
    }

    public void registrarMensagem(String remetente, String destinatario, String conteudo) {
        String timestamp = LocalDateTime.now().format(formatter);
        String sql = "INSERT INTO mensagens(timestamp, remetente, destinatario, conteudo) VALUES(?, ?, ?, ?)";
        String dest = (destinatario == null || destinatario.isEmpty()) ? "TODOS" : destinatario;
        
        try (Connection conn = conectar();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, timestamp);
            pstmt.setString(2, remetente);
            pstmt.setString(3, dest);
            pstmt.setString(4, conteudo);
            pstmt.executeUpdate();
            System.out.println("[Auditoria] Mensagem salva no banco.");
        } catch (SQLException e) {
            System.err.println("Auditoria: Erro ao salvar mensagem: " + e.getMessage());
        }
    }
}
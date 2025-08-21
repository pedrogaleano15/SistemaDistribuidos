# Servidor TCP multi-threaded
import socket
import threading

# Configuração do host e porta do servidor
host = 'localhost'
port = 50000

# Lista para armazenar os clientes conectados
clientes_conectados = []
# Lock para garantir acesso seguro à lista de clientes entre threads
lock = threading.Lock()

# Função que lida com cada cliente conectado (executada em uma thread)
def handle_client(conn, addr):
    # Adiciona o cliente à lista de conectados de forma segura
    with lock:
        clientes_conectados.append(addr)
    print(f'Conectado a: {addr}')
    try:
        while True:
            # Recebe dados do cliente
            data = conn.recv(1024)
            if not data:
                # Se não receber dados, cliente desconectou
                print(f'Cliente {addr} desconectado.')
                break
            msg = data.decode().strip()
            print(f'Dados recebidos de {addr}: {msg}')
            # Comando para ecoar uma mensagem
            if msg == 'ECO':
                conn.sendall(b'Digite a mensagem para ecoar:')
                eco_msg = conn.recv(1024)
                conn.sendall(b'ECO: ' + eco_msg)
            # Comando para listar clientes conectados
            elif msg == 'LISTA':
                with lock:
                    lista = '\n'.join([str(a) for a in clientes_conectados])
                conn.sendall(f'Clientes conectados:\n{lista}'.encode())
            # Comando para encerrar a conexão do cliente
            elif msg == 'SAIR':
                conn.sendall(b'Conexao encerrada pelo cliente.')
                break
            # Comando para retornar a hora atual do servidor
            elif msg == 'HORA':
                import datetime
                agora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                conn.sendall(f'Hora do servidor: {agora}'.encode())
            # Comando desconhecido
            else:
                conn.sendall(b'Comando desconhecido. Use: ECO, LISTA, HORA ou SAIR.')
    finally:
        # Remove o cliente da lista ao desconectar e fecha a conexão
        with lock:
            if addr in clientes_conectados:
                clientes_conectados.remove(addr)
        conn.close()

# Função principal do servidor
def main():
    # Cria o socket TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Associa o socket ao endereço e porta
    s.bind((host, port))
    # Coloca o servidor em modo de escuta
    s.listen()
    print('Servidor ativo. Aguardando conexoes...')
    while True:
        # Aceita novas conexões
        conn, addr = s.accept()
        # Cria uma thread para cada cliente
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()

# Inicia o servidor
if __name__ == '__main__':
    main()
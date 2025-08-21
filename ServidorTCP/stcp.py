#Servidor TCP
import socket
import threading

host = 'localhost'
port = 50000

clientes_conectados = []  # lista de clientes conectados
lock = threading.Lock()

def handle_client(conn, addr):
    with lock:
        clientes_conectados.append(addr)
    print(f'Conectado a: {addr}')
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f'Cliente {addr} desconectado.')
                break
            msg = data.decode().strip()
            print(f'Dados recebidos de {addr}: {msg}')
            if msg == 'ECO':
                conn.sendall(b'Digite a mensagem para ecoar:')
                eco_msg = conn.recv(1024)
                conn.sendall(b'ECO: ' + eco_msg)
            elif msg == 'LISTA':
                with lock:
                    lista = '\n'.join([str(a) for a in clientes_conectados])
                conn.sendall(f'Clientes conectados:\n{lista}'.encode())
            elif msg == 'SAIR':
                conn.sendall(b'Conexao encerrada pelo cliente.')
                break
            elif msg == 'HORA':
                import datetime
                agora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                conn.sendall(f'Hora do servidor: {agora}'.encode())
            else:
                conn.sendall(b'Comando desconhecido. Use: ECO, LISTA, HORA ou SAIR.')
    finally:
        with lock:
            if addr in clientes_conectados:
                clientes_conectados.remove(addr)
        conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print('Servidor ativo. Aguardando conexoes...')
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()

if __name__ == '__main__':
    main()
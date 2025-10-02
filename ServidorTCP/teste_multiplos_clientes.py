# Script para simular múltiplos clientes conectando ao servidor TCP e enviando comandos em loop
import socket
import threading
import time

HOST = '192.168.22.126'  # Altere para o IP do servidor
PORT = 50000
NUM_CLIENTES = 2000  # Aumente para mais pressão
NUM_ITERACOES = 150  # Quantidade de comandos por cliente

def simula_cliente(id_cliente):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((HOST, PORT))
        print(f'Cliente {id_cliente} conectado.')
        for i in range(NUM_ITERACOES):
            # Alterna entre comandos para gerar carga
            if i % 4 == 0:
                c.sendall(b'LISTA')
                resposta = c.recv(1024)
            elif i % 4 == 1:
                c.sendall(b'HORA')
                resposta = c.recv(1024)
            elif i % 4 == 2:
                c.sendall(b'ECO')
                prompt = c.recv(1024)
                c.sendall(f'Loop {i} do cliente {id_cliente}'.encode())
                resposta = c.recv(1024)
            else:
                c.sendall(b'COMANDO_INVALIDO')
                resposta = c.recv(1024)
            print(f'Cliente {id_cliente} iteração {i+1}: {resposta.decode()}')
            # Pequeno delay para simular uso real
            
        # Envia comando SAIR ao final
        c.sendall(b'SAIR')
        resposta = c.recv(1024)
        print(f'Cliente {id_cliente} saiu: {resposta.decode()}')
        c.close()
    except Exception as e:
        print(f'Cliente {id_cliente} erro: {e}')

# Cria e inicia múltiplas threads de clientes
threads = []
for i in range(NUM_CLIENTES):
    t = threading.Thread(target=simula_cliente, args=(i+1,))
    t.start()
    threads.append(t)
    # Remova o delay abaixo para pressão máxima
    time.sleep(0.01)

# Aguarda todas as threads terminarem
for t in threads:
    t.join()

print('Teste de múltiplos clientes finalizado.')

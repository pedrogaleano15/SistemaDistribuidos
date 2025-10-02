# Cliente TCP multi-serviço
import socket
import sys

host = '192.168.22.12'  # endereço do servidor
port = 50000             # porta onde o servidor está

# Criando o socket IPV4 TCP
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((host, port))

print('Conectado ao servidor! Comandos disponíveis: ECO, LISTA, HORA, SAIR')

while True:
    comando = input('\nDigite o comando (ECO, LISTA, HORA, SAIR): ').strip().upper()
    c.sendall(comando.encode())
    resposta = c.recv(1024).decode()
    print('Servidor:', resposta)

    if comando == 'ECO':
        # Se o comando for ECO, o servidor pedirá a mensagem para ecoar
        eco_msg = input('Digite a mensagem para ecoar: ')
        c.sendall(eco_msg.encode())
        resposta_eco = c.recv(1024).decode()
        print('Servidor:', resposta_eco)
    elif comando == 'SAIR':
        print('Encerrando conexão com o servidor.')
        break

c.close()
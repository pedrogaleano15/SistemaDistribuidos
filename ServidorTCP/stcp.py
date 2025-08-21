#servidor TCP
import socket
import sys
host = 'localhost'
port = 50000 #porta do servidor
#criando o socket IPV4 TCP
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ligando o socket na porta e no endereco IP
s.bind((host, port))
#0 servidor fica escutando na porta 50000 no endereco IP 127.0.0.1
s.listen(1)
print('Servidor TCP esperando conexao na porta %s ...' % port)
#loop para ecoar os dados recebidos
conn,endr = s.accept() #aceitando a conexao
print('Conectado por', endr)
while True:
    data = conn.recv(1024) #recebendo os dados do cliente
    if not data: 
        print("Recebido do cliente: ", data.decode())
        conn.sendall(data) #enviando os dados para o cliente
        conn.close() #fechando a conexao
        break  # se não houver dados, encerra o loop
    print("Recebido do cliente: ", data.decode())
    conn.sendall(data) #enviando dados vazios para o cliente

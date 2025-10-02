import paho.mqtt.client as mqtt
import pygame
#dois dicionarios para gerenciar as posiçoes dos jogadores
my_pos={'x':600, 'y':200}
oponente_pos={'x':200,'y':200}
#funções MQTT
def on_connect (client,userdata,flags,rc):
    print("Jogador 2: Conectado ao broker!")
    client.subscribe("movimentos_jogador1")
def on_message(client,userdata,message):
    global oponente_pos
    comando = int(message.payload.decode("utf-8"))
    velocidade = 10
    #atualizar a posição do oponente
    if comando == 1 : oponente_pos['x'] -=velocidade
    if comando == 2 : oponente_pos['x'] +=velocidade
    if comando == 3 : oponente_pos['y'] -=velocidade
    if comando == 4 : oponente_pos['y'] +=velocidade
#configuraçao do MQTT
client = mqtt.Client("Jogador 2")
client.on_connect=on_connect
client.on_message=on_message
client.connect("localhost",50000)
client.loop_start()
#configuraçao do pygame
pygame.init()
tela = pygame.display.set_mode((800,400))
pygame.display.set_caption("Jogador 2")

COR_JOGADOR_LOCAL = (255,0,0) #VERMELHO
COR_OPONENTE = (0,255,0) #VERDE
COR_FUNDO = (0,0,255) #AZUL
#LOOP DO JOGO
sair = True
velocidade=10
clock = pygame.time.Clock()

while sair:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair=False
    # decodificação da teclas e movimentos
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        my_pos['x'] -=velocidade
        client.publish("movimentos_jogador2","1")
    if keys[pygame.K_RIGHT]:
        my_pos['x'] +=velocidade
        client.publish("movimentos_jogador2","2")
    if keys[pygame.K_UP]:
        my_pos['y'] -=velocidade
        client.publish("movimentos_jogador2","3")
    if keys[pygame.K_DOWN]:
        my_pos['y'] +=velocidade
        client.publish("movimentos_jogador2","4")
    #Desenhar na tela o jogador local e o openente
    tela.fill(COR_FUNDO)
    pygame.draw.circle(tela,COR_JOGADOR_LOCAL,(my_pos['x'],my_pos['y']),25)
    pygame.draw.circle(tela,COR_OPONENTE,(oponente_pos['x'],oponente_pos['y']),25)
    pygame.display.update()
    clock.tick(60) #limita frames por segundo
client.loop_stop()
pygame.quit()
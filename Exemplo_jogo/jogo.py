# Nome do arquivo: jogo.py
import paho.mqtt.client as mqtt
import pygame
import sys
import time

# --- Constantes de Configuração ---
LARGURA_TELA = 800
ALTURA_TELA = 400
COR_FUNDO = (0, 0, 255) # AZUL
FPS = 60
VELOCIDADE = 10
RAIO_JOGADOR = 25

# Configs MQTT
BROKER_HOST = "localhost"
# ATENÇÃO: A porta padrão do MQTT é 1883. 
# Você usou 50000, o que é incomum, mas vou manter.
# Se não funcionar, tente mudar para 1883 (e verifique seu broker Mosquitto)
BROKER_PORTA = 50000 

# --- Configuração do Jogador (Baseado no argumento de linha de comando) ---

# Por padrão, é o Jogador 1
PLAYER_ID = "Jogador 1"
TOPICO_PUBLICAR = "movimentos_jogador1"
TOPICO_INSCREVER = "movimentos_jogador2"
MY_POS_INICIAL = {'x': 600, 'y': 200}
OPONENTE_POS_INICIAL = {'x': 200, 'y': 200}
COR_JOGADOR_LOCAL = (0, 255, 0) # VERDE
COR_OPONENTE = (255, 0, 0) # VERMELHO

# Verifica se o script foi chamado com "player2"
if len(sys.argv) > 1 and sys.argv[1] == "player2":
    PLAYER_ID = "Jogador 2"
    TOPICO_PUBLICAR = "movimentos_jogador2"
    TOPICO_INSCREVER = "movimentos_jogador1"
    # Inverte as posições e cores
    MY_POS_INICIAL = {'x': 200, 'y': 200}
    OPONENTE_POS_INICIAL = {'x': 600, 'y': 200}
    COR_JOGADOR_LOCAL = (255, 0, 0) # VERMELHO
    COR_OPONENTE = (0, 255, 0) # VERDE

# --- Variáveis Globais do Jogo ---
my_pos = MY_POS_INICIAL.copy()
oponente_pos = OPONENTE_POS_INICIAL.copy()

# --- Funções MQTT ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{PLAYER_ID}]: Conectado ao broker em {BROKER_HOST}:{BROKER_PORTA}")
        client.subscribe(TOPICO_INSCREVER)
    else:
        print(f"[{PLAYER_ID}]: Falha na conexão! Código: {rc}")

def on_message(client, userdata, message):
    global oponente_pos
    try:
        comando = int(message.payload.decode("utf-8"))
        
        # Atualizar a posição do oponente
        if comando == 1: oponente_pos['x'] -= VELOCIDADE
        elif comando == 2: oponente_pos['x'] += VELOCIDADE
        elif comando == 3: oponente_pos['y'] -= VELOCIDADE
        elif comando == 4: oponente_pos['y'] += VELOCIDADE
            
    except ValueError:
        print(f"Mensagem inválida recebida: {message.payload}")
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

# --- Configuração MQTT ---
client = mqtt.Client(PLAYER_ID)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER_HOST, BROKER_PORTA)
except ConnectionRefusedError:
    print(f"[{PLAYER_ID}]: Erro! Não foi possível conectar ao broker.")
    print("Verifique se o seu broker (Mosquitto) está em execução.")
    sys.exit(1)
except Exception as e:
    print(f"[{PLAYER_ID}]: Ocorreu um erro inesperado na conexão MQTT: {e}")
    sys.exit(1)
    
client.loop_start()

# --- Configuração Pygame ---
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(PLAYER_ID)
clock = pygame.time.Clock()

# --- Loop Principal do Jogo ---
sair = True
while sair:
    # --- Processamento de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = False

    # --- Decodificação de Teclas e Movimentos ---
    keys = pygame.key.get_pressed()
    movimento_publicar = None
    
    # Usamos 'elif' para evitar publicar múltiplos movimentos no mesmo frame
    if keys[pygame.K_LEFT]:
        my_pos['x'] -= VELOCIDADE
        movimento_publicar = "1"
    elif keys[pygame.K_RIGHT]:
        my_pos['x'] += VELOCIDADE
        movimento_publicar = "2"
    elif keys[pygame.K_UP]:
        my_pos['y'] -= VELOCIDADE
        movimento_publicar = "3"
    elif keys[pygame.K_DOWN]:
        my_pos['y'] += VELOCIDADE
        movimento_publicar = "4"
    
    # Publica a mensagem MQTT apenas se uma tecla foi pressionada
    if movimento_publicar:
        client.publish(TOPICO_PUBLICAR, movimento_publicar)

    # --- Desenhar na Tela ---
    tela.fill(COR_FUNDO)
    pygame.draw.circle(tela, COR_JOGADOR_LOCAL, (my_pos['x'], my_pos['y']), RAIO_JOGADOR)
    pygame.draw.circle(tela, COR_OPONENTE, (oponente_pos['x'], oponente_pos['y']), RAIO_JOGADOR)
    
    # --- Atualização da Tela ---
    pygame.display.update()
    clock.tick(FPS) # Limita frames por segundo

# --- Finalização ---
print(f"[{PLAYER_ID}]: Encerrando...")
client.loop_stop()
pygame.quit()
sys.exit(0)
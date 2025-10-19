# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import pygame
import sys
import json
import random

# --- Tópicos ---
BROKER_IP = "192.168.23.83"
BROKER_PORT = 1883
TOPICO_POSICAO = "jogo/posicao"
TOPICO_OBSTACULOS = "jogo/obstaculos"
TOPICO_TIROS = "jogo/tiros"
TOPICO_DESTRUICAO = "jogo/destruicao"
TOPICO_EVENTOS = "jogo/eventos" 
TOPICO_PONTUACAO = "jogo/pontuacao"

# --- Variáveis de Estado ---
LARGURA_TELA = 800
ALTURA_TELA = 600
jogadores_pos = {}
obstaculos_ativos = []
tiros_ativos = {}
JOGADORES_VIVOS = {}
pontuacoes = {}
VENCEDOR_ID = None 

# --- Configurações do Pygame ---
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Observador do Jogo")
relogio = pygame.time.Clock()

# --- CORES E FONTES ---
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
VERDE_CLARO = (150, 255, 150)
FONTE_PONTOS = pygame.font.Font(None, 36)
FONTE_MENU = pygame.font.Font(None, 50)
FONTE_TITULO = pygame.font.Font(None, 72)

# --- Carregar Imagens ---
try:
    # *** ALTERAÇÃO: Carrega a mesma imagem de nave para todos ***
    nave_imagem_unica = pygame.image.load('nave.png').convert_alpha() # Imagem padrão
    
    fundo_imagem = pygame.image.load('fundo_espacial.jpg').convert()
    asteroide_imagem = pygame.image.load('asteroide.png').convert_alpha()
    tiro_surface = pygame.Surface((5, 15))
    tiro_surface.fill(BRANCO)
    
    # Redimensionamento
    fundo_imagem = pygame.transform.scale(fundo_imagem, (LARGURA_TELA, ALTURA_TELA))
    tamanho_nave = (60, 50) # Definição de um tamanho padrão para as naves
    
    # *** ALTERAÇÃO: Redimensiona apenas a imagem única ***
    nave_imagem = pygame.transform.smoothscale(nave_imagem_unica, tamanho_nave)
    asteroide_imagem = pygame.transform.smoothscale(asteroide_imagem, (50, 50))
    
except pygame.error as e:
    print(f"ERRO CRÍTICO: Não foi possível carregar uma imagem: {e}")
    sys.exit()

# --- Funções de Callback MQTT ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Observador: Conectado! Assinando tópicos...")
        client.subscribe(TOPICO_POSICAO)
        client.subscribe(TOPICO_OBSTACULOS)
        client.subscribe(TOPICO_TIROS)
        client.subscribe(TOPICO_DESTRUICAO)
        client.subscribe(TOPICO_EVENTOS)
        client.subscribe(TOPICO_PONTUACAO)
    else:
        print(f"Observador: Falha na conexão, código de erro: {rc}")

def on_message(client, userdata, message):
    global jogadores_pos, obstaculos_ativos, tiros_ativos, JOGADORES_VIVOS, pontuacoes, VENCEDOR_ID
    try:
        payload = message.payload.decode("utf-8")
        topico = message.topic
        data = json.loads(payload)
        
        if topico == TOPICO_EVENTOS:
            evento = data.get('evento')
            jogador_id = data.get('jogador_id')
            
            # CORREÇÃO AQUI: 'jogador_saiu' agora reseta o jogo
            if evento == 'reiniciar_jogo' or evento == 'jogador_saiu':
                if evento == 'jogador_saiu':
                    print(f"Observador: {jogador_id} saiu. Resetando o lobby.")
                else: # reiniciar_jogo
                    print("Observador: Recebido comando para reiniciar o jogo.")
                
                VENCEDOR_ID = None
                jogadores_pos.clear(); JOGADORES_VIVOS.clear()
                obstaculos_ativos.clear(); tiros_ativos.clear()
                pontuacoes.clear()
                
            elif evento == 'vitoria':
                VENCEDOR_ID = data.get('vencedor_id')
            elif evento == 'jogador_destruido':
                if jogador_id: JOGADORES_VIVOS[jogador_id] = False
            elif evento == 'jogador_renasceu':
                if jogador_id: JOGADORES_VIVOS[jogador_id] = True
            
        elif topico == TOPICO_POSICAO:
            jogador_id = data['jogador_id']
            # Só adiciona o jogador se o jogo não tiver um vencedor definido
            if VENCEDOR_ID is None:
                jogadores_pos[jogador_id] = data
                if jogador_id not in JOGADORES_VIVOS: JOGADORES_VIVOS[jogador_id] = True
                if jogador_id not in pontuacoes: pontuacoes[jogador_id] = 0

        elif topico == TOPICO_OBSTACULOS:
            obstaculos_ativos.extend(data)

        elif topico == TOPICO_TIROS:
            tiros_ativos[data['id_tiro']] = data

        elif topico == TOPICO_DESTRUICAO:
            tiro_id = data.get('id_tiro'); obs_id = data.get('id_obstaculo')
            if tiro_id in tiros_ativos: del tiros_ativos[tiro_id]
            obstaculos_ativos[:] = [obs for obs in obstaculos_ativos if obs.get('id') != obs_id]
            
        elif topico == TOPICO_PONTUACAO:
            jogador_id = data.get('jogador_id'); pontos = data.get('pontos')
            if jogador_id is not None and pontos is not None: pontuacoes[jogador_id] = pontos

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Erro ao processar mensagem: {e} - Payload: {payload}")

client = mqtt.Client(client_id="observador_gerenciador", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect; client.on_message = on_message
client.connect(BROKER_IP, BROKER_PORT, 60); client.loop_start()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: rodando = False
    
    for id_tiro, tiro in tiros_ativos.items(): tiro['y'] -= 10
    tiros_ativos = {id_tiro: tiro for id_tiro, tiro in tiros_ativos.items() if tiro['y'] > -20}
    for obs in obstaculos_ativos: obs['y'] += obs.get('velocidade_y', 3)
    obstaculos_ativos[:] = [obs for obs in obstaculos_ativos if obs['y'] < ALTURA_TELA + 50]
    
    tela.blit(fundo_imagem, (0, 0))

    if len(jogadores_pos) < 2 and not VENCEDOR_ID:
        texto_aguardando = FONTE_MENU.render(f"Aguardando {2 - len(jogadores_pos)} jogadores...", True, BRANCO)
        tela.blit(texto_aguardando, texto_aguardando.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2)))
    elif VENCEDOR_ID:
        texto_vitoria = FONTE_TITULO.render(f"O VENCEDOR É: {VENCEDOR_ID}", True, VERDE_CLARO)
        tela.blit(texto_vitoria, texto_vitoria.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 - 50)))
        pos_y_placar = ALTURA_TELA/2 + 50
        for jogador_id, pontos in sorted(pontuacoes.items(), key=lambda item: item[1], reverse=True):
            texto_placar = FONTE_MENU.render(f"{jogador_id}: {pontos} pontos", True, AMARELO)
            tela.blit(texto_placar, texto_placar.get_rect(center=(LARGURA_TELA/2, pos_y_placar))); pos_y_placar += 40
    else:
        # *** ALTERAÇÃO: Simplificado para desenhar sempre a mesma imagem de nave ***
        for id_jogador, pos in jogadores_pos.items():
            if JOGADORES_VIVOS.get(id_jogador, True):
                tela.blit(nave_imagem, nave_imagem.get_rect(center=(pos['x'], pos['y'])))
                    
        for obs in obstaculos_ativos:
            tela.blit(asteroide_imagem, asteroide_imagem.get_rect(center=(obs['x'], obs['y'])))
        for id_tiro, tiro_data in tiros_ativos.items():
            tela.blit(tiro_surface, tiro_surface.get_rect(center=(int(tiro_data['x']), int(tiro_data['y']))))
        pos_y_placar = 10
        for jogador_id, pontos in sorted(pontuacoes.items(), key=lambda item: item[1], reverse=True):
            texto_placar = FONTE_PONTOS.render(f"{jogador_id}: {pontos}", True, AMARELO)
            tela.blit(texto_placar, (10, pos_y_placar)); pos_y_placar += 30

    pygame.display.flip(); relogio.tick(60)

pygame.quit(); client.loop_stop(); sys.exit()
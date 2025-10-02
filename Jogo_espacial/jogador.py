# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import pygame
import sys
import json
import random
import time

if len(sys.argv) < 2:
    print("Uso: python jogador.py <ID_DO_JOGADOR>")
    sys.exit(1)
JOGADOR_ID = sys.argv[1]

# --- Configurações de Rede e Tópicos ---
BROKER_IP = "172.31.9.221"
BROKER_PORT = 50000
TOPICO_POSICAO = "jogo/posicao"
TOPICO_EVENTOS = "jogo/eventos" 
TOPICO_OBSTACULOS = "jogo/obstaculos"
TOPICO_TIROS = "jogo/tiros"
TOPICO_DESTRUICAO = "jogo/destruicao"
TOPICO_PONTUACAO = "jogo/pontuacao"

# --- Configurações do Pygame ---
LARGURA_TELA = 800
ALTURA_TELA = 600
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(f"Nave do Jogador {JOGADOR_ID}")
relogio = pygame.time.Clock()

# --- CORES E FONTES ---
BRANCO = (255, 255, 255)
CINZA = (100, 100, 100)
VERDE_CLARO = (150, 255, 150)
VERMELHO_CLARO = (255, 150, 150)
AMARELO = (255, 255, 0)
FONTE_MENU = pygame.font.Font(None, 50)
FONTE_TITULO = pygame.font.Font(None, 72)
FONTE_PONTOS = pygame.font.Font(None, 36)

# --- Variáveis de Estado do Jogo ---
posicao_jogador = {'x': 200 if JOGADOR_ID == 'jogador1' else 600, 'y': ALTURA_TELA - 60}
oponentes_pos = {}
obstaculos_ativos = []
tiros_ativos = {}
JOGADOR_ELIMINADO = False
# OPONENTES_VIVOS passa a rastrear o status de ELIMINAÇÃO (True = Vivo, False = Eliminado)
OPONENTES_ELIMINADOS = {} 
pontuacoes = {JOGADOR_ID: 0}
JOGO_INICIADO = False 
VENCEDOR = None 
rodando = True

# --- Carregar Imagens ---
try:
    # Usando 'nave.jpg' para ser compatível com o arquivo enviado
    nave_imagem = pygame.image.load('nave.png').convert_alpha() 
    fundo_imagem = pygame.image.load('fundo_espacial.jpg').convert()
    asteroide_imagem = pygame.image.load('asteroide.png').convert_alpha()
    tiro_surface = pygame.Surface((5, 15))
    tiro_surface.fill(BRANCO)
    fundo_imagem = pygame.transform.scale(fundo_imagem, (LARGURA_TELA, ALTURA_TELA))
    nave_imagem = pygame.transform.scale(nave_imagem, (60, 50))
    asteroide_imagem = pygame.transform.scale(asteroide_imagem, (50, 50))
except pygame.error as e:
    print(f"ERRO CRÍTICO: Não foi possível carregar uma imagem: {e}")
    sys.exit()

nave_rect = nave_imagem.get_rect(center=(posicao_jogador['x'], posicao_jogador['y']))

def resetar_estado_local():
    """Reinicia todas as variáveis de jogo para um novo início."""
    global posicao_jogador, oponentes_pos, obstaculos_ativos, tiros_ativos, JOGADOR_ELIMINADO, OPONENTES_ELIMINADOS, pontuacoes, JOGO_INICIADO, VENCEDOR
    
    posicao_jogador = {'x': 200 if JOGADOR_ID == 'jogador1' else 600, 'y': ALTURA_TELA - 60}
    nave_rect.center = (posicao_jogador['x'], posicao_jogador['y'])
    
    oponentes_pos.clear()
    obstaculos_ativos.clear()
    tiros_ativos.clear()
    OPONENTES_ELIMINADOS.clear() # Limpa o status de eliminação de todos os jogadores
    pontuacoes = {JOGADOR_ID: 0} # ZERA a pontuação do próprio jogador

    JOGADOR_ELIMINADO = False
    JOGO_INICIADO = False
    VENCEDOR = None
    
    client.publish(TOPICO_POSICAO, json.dumps({'jogador_id': JOGADOR_ID, 'x': posicao_jogador['x'], 'y': posicao_jogador['y']}))
    client.publish(TOPICO_EVENTOS, json.dumps({'evento': 'jogador_renasceu', 'jogador_id': JOGADOR_ID}))

def checar_vitoria():
    """Verifica se o jogo deve terminar e, se sim, quem é o vencedor por maior pontuação."""
    global VENCEDOR, JOGO_INICIADO, pontuacoes
    
    # Adiciona o status do próprio jogador à verificação
    todos_eliminados = JOGADOR_ELIMINADO
    
    # Verifica o status dos oponentes
    jogadores_ativos = 0
    for status in OPONENTES_ELIMINADOS.values():
        if status == True: # True significa que o oponente está VIVO
            jogadores_ativos += 1
            
    # Se o próprio jogador estiver eliminado E não houver mais jogadores ativos, o jogo acabou.
    if JOGADOR_ELIMINADO and jogadores_ativos == 0:
        
        # Encontra o jogador com a maior pontuação (o vencedor)
        if not pontuacoes: return
        
        # Converte para lista de tuplas (pontos, jogador_id) e ordena decrescente
        placar_ordenado = sorted(pontuacoes.items(), key=lambda item: item[1], reverse=True)
        
        if placar_ordenado:
            VENCEDOR = placar_ordenado[0][0] # Pega o ID do jogador com mais pontos
            JOGO_INICIADO = False
            
            # Publica o evento de vitória apenas uma vez
            if VENCEDOR:
                print(f"Todos eliminados! Vencedor por pontuação: {VENCEDOR}")
                client.publish(TOPICO_EVENTOS, json.dumps({'evento': 'vitoria', 'vencedor_id': VENCEDOR}))

# --- Funções de Callback MQTT ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Jogador '{JOGADOR_ID}': Conectado! Assinando tópicos...")
        client.subscribe(TOPICO_POSICAO)
        client.subscribe(TOPICO_OBSTACULOS)
        client.subscribe(TOPICO_TIROS)
        client.subscribe(TOPICO_DESTRUICAO)
        client.subscribe(TOPICO_EVENTOS)
        client.subscribe(TOPICO_PONTUACAO)
        client.publish(TOPICO_POSICAO, json.dumps({'jogador_id': JOGADOR_ID, 'x': posicao_jogador['x'], 'y': posicao_jogador['y']}))
    else:
        print(f"Jogador '{JOGADOR_ID}': Falha na conexão, código de erro:", rc)

def on_message(client, userdata, message):
    global obstaculos_ativos, oponentes_pos, tiros_ativos, OPONENTES_ELIMINADOS, pontuacoes, JOGO_INICIADO, VENCEDOR, JOGADOR_ELIMINADO, rodando
    try:
        payload = message.payload.decode("utf-8")
        topico = message.topic
        data = json.loads(payload)

        if topico == TOPICO_POSICAO:
            jogador_id = data['jogador_id']
            if jogador_id != JOGADOR_ID:
                oponentes_pos[jogador_id] = {'x': data['x'], 'y': data['y']}
                
                if jogador_id not in OPONENTES_ELIMINADOS:
                     OPONENTES_ELIMINADOS[jogador_id] = True # True = VIVO
                     pontuacoes[jogador_id] = 0
                     if not JOGO_INICIADO and len(oponentes_pos) >= 1: 
                         JOGO_INICIADO = True
                         JOGADOR_ELIMINADO = False
                         VENCEDOR = None
                         print("Oponente detectado. Jogo começando! Enviando sinal de início...")
                         client.publish(TOPICO_EVENTOS, json.dumps({'evento': 'jogo_iniciado'}))
                    

        elif topico == TOPICO_OBSTACULOS:
            if JOGO_INICIADO:
                obstaculos_ativos.extend(data)

        elif topico == TOPICO_TIROS:
            if JOGO_INICIADO and data['atirador_id'] != JOGADOR_ID:
                tiros_ativos[data['id_tiro']] = data

        elif topico == TOPICO_DESTRUICAO:
            tiro_id = data.get('id_tiro')
            obs_id = data.get('id_obstaculo')
            if tiro_id in tiros_ativos: del tiros_ativos[tiro_id]
            obstaculos_ativos[:] = [obs for obs in obstaculos_ativos if obs.get('id') != obs_id]
        
        elif topico == TOPICO_EVENTOS:
            evento = data.get('evento')
            jogador_id = data.get('jogador_id')
            
            if evento == 'jogo_iniciado':
                JOGO_INICIADO = True; JOGADOR_ELIMINADO = False; VENCEDOR = None
            
            elif evento == 'reiniciar_jogo':
                client.publish(TOPICO_EVENTOS, json.dumps({'evento': 'jogo_reiniciado'}))
            
            elif evento == 'jogo_reiniciado':
                resetar_estado_local()
            
            elif evento == 'jogador_saiu':
                if jogador_id == JOGADOR_ID: 
                    rodando = False
                elif jogador_id in oponentes_pos:
                    del oponentes_pos[jogador_id]
                    if JOGO_INICIADO and len(oponentes_pos) == 0:
                        # Se o oponente sair, encerra e declara o outro (este) vencedor
                        JOGO_INICIADO = False
                        VENCEDOR = JOGADOR_ID
                        client.publish(TOPICO_EVENTOS, json.dumps({'evento': 'vitoria', 'vencedor_id': JOGADOR_ID}))

            elif evento == 'jogador_destruido': 
                if jogador_id != JOGADOR_ID and jogador_id in OPONENTES_ELIMINADOS:
                    OPONENTES_ELIMINADOS[jogador_id] = False # False = ELIMINADO
                
                # Checa a condição de vitória global (todos eliminados)
                checar_vitoria()

            elif evento == 'jogador_renasceu':
                 if jogador_id in OPONENTES_ELIMINADOS: OPONENTES_ELIMINADOS[jogador_id] = True

            elif evento == 'vitoria':
                JOGO_INICIADO = False
                VENCEDOR = data.get('vencedor_id')
                JOGADOR_ELIMINADO = True # Garante que a tela final de placar seja exibida
                print(f"Fim do Jogo! O Vencedor é: {VENCEDOR}")


        elif topico == TOPICO_PONTUACAO:
            jogador_id = data.get('jogador_id')
            pontos = data.get('pontos')
            if jogador_id is not None and pontos is not None:
                pontuacoes[jogador_id] = pontos


    except (json.JSONDecodeError, KeyError) as e:
        print(f"Erro ao processar mensagem: {e} - Payload: {payload}")

# --- Configuração e Conexão MQTT ---
client = mqtt.Client(client_id=JOGADOR_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_IP, BROKER_PORT, 60)
client.loop_start()

# --- Loop Principal ---
ultima_vez_tiro = pygame.time.get_ticks()
botao_reiniciar = pygame.Rect(LARGURA_TELA / 2 - 150, ALTURA_TELA / 2 + 50, 300, 50)
botao_sair = pygame.Rect(LARGURA_TELA / 2 - 150, ALTURA_TELA / 2 + 125, 300, 50)

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            client.publish(TOPICO_EVENTOS, json.dumps({'evento': 'jogador_saiu', 'jogador_id': JOGADOR_ID}))
            rodando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if not JOGO_INICIADO and (JOGADOR_ELIMINADO or VENCEDOR):
                if botao_reiniciar.collidepoint(mouse_pos):
                    client.publish(TOPICO_EVENTOS, json.dumps({'evento': 'reiniciar_jogo', 'jogador_id': JOGADOR_ID}))
                if botao_sair.collidepoint(mouse_pos):
                    client.publish(TOPICO_EVENTOS, json.dumps({'evento': 'jogador_saiu', 'jogador_id': JOGADOR_ID}))
                    rodando = False

    if JOGO_INICIADO and not JOGADOR_ELIMINADO:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and nave_rect.left > 0: posicao_jogador['x'] -= 5
        if keys[pygame.K_d] and nave_rect.right < LARGURA_TELA: posicao_jogador['x'] += 5
        if keys[pygame.K_w] and nave_rect.top > 0: posicao_jogador['y'] -= 5
        if keys[pygame.K_s] and nave_rect.bottom < ALTURA_TELA: posicao_jogador['y'] += 5
        nave_rect.center = (posicao_jogador['x'], posicao_jogador['y'])
        client.publish(TOPICO_POSICAO, json.dumps({'jogador_id': JOGADOR_ID, 'x': posicao_jogador['x'], 'y': posicao_jogador['y']}))

        if keys[pygame.K_SPACE] and (pygame.time.get_ticks() - ultima_vez_tiro > 200):
            ultima_vez_tiro = pygame.time.get_ticks()
            id_tiro = f"{JOGADOR_ID}_{time.time()}"
            novo_tiro = {"id_tiro": id_tiro, "x": nave_rect.centerx, "y": nave_rect.top, "atirador_id": JOGADOR_ID}
            tiros_ativos[id_tiro] = novo_tiro
            client.publish(TOPICO_TIROS, json.dumps(novo_tiro))
        
        # --- LÓGICA DE COLISÃO DO PRÓPRIO JOGADOR COM OBSTÁCULO (Morte) ---
        for obs in obstaculos_ativos:
            obs_rect = pygame.Rect(obs['x'] - 25, obs['y'] - 25, 50, 50)
            if nave_rect.colliderect(obs_rect):
                JOGADOR_ELIMINADO = True
                
                # Publica que foi destruído
                client.publish(TOPICO_EVENTOS, json.dumps({'evento': 'jogador_destruido', 'jogador_id': JOGADOR_ID}))
                
                # Checa se o jogo termina agora
                checar_vitoria()

                break # Sai do loop de obstáculos pois o jogador morreu

    for obs in obstaculos_ativos: obs['y'] += obs['velocidade_y']
    obstaculos_ativos[:] = [obs for obs in obstaculos_ativos if obs['y'] < ALTURA_TELA + 50]
    for id_tiro, tiro in list(tiros_ativos.items()):
        tiro['y'] -= 10
        if tiro['y'] < -20: del tiros_ativos[id_tiro]

    # --- LÓGICA DE COLISÃO DO PRÓPRIO JOGADOR (Pontuação) ---
    for id_tiro, tiro in list(tiros_ativos.items()):
        if tiro['atirador_id'] == JOGADOR_ID:
            tiro_rect = pygame.Rect(tiro['x'] - 2, tiro['y'] - 7, 5, 15)
            for obs in list(obstaculos_ativos):
                obs_rect = pygame.Rect(obs['x'] - 25, obs['y'] - 25, 50, 50)
                if tiro_rect.colliderect(obs_rect):
                    pontuacoes[JOGADOR_ID] += 10 
                    
                    client.publish(TOPICO_PONTUACAO, json.dumps({'jogador_id': JOGADOR_ID, 'pontos': pontuacoes[JOGADOR_ID]}))
                    
                    payload_destruicao = {'id_tiro': id_tiro, 'id_obstaculo': obs['id']}
                    client.publish(TOPICO_DESTRUICAO, json.dumps(payload_destruicao))
                    
                    if id_tiro in tiros_ativos: del tiros_ativos[id_tiro]
                    if obs in obstaculos_ativos: obstaculos_ativos.remove(obs)
                    break

    # --- DESENHO NA TELA ---
    tela.blit(fundo_imagem, (0, 0))

    if not JOGO_INICIADO or JOGADOR_ELIMINADO:
        if VENCEDOR: 
            overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            tela.blit(overlay, (0, 0))
            
            if VENCEDOR == JOGADOR_ID: 
                texto_resultado = FONTE_TITULO.render("VOCÊ VENCEU!", True, VERDE_CLARO)
            else: 
                texto_resultado = FONTE_TITULO.render("VOCÊ PERDEU!", True, VERMELHO_CLARO)
            
            rect_resultado = texto_resultado.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 - 120))
            tela.blit(texto_resultado, rect_resultado)

            # Placar final (Ordenado pelo VENCEDOR primeiro)
            pos_y_placar = ALTURA_TELA/2 - 50
            
            # Função de ordenação: Vencedor primeiro, depois pontuação descendente
            def ordenar_placar(item):
                jogador_id, pontos = item
                # Coloca o VENCEDOR no topo (True = -1) e o restante pela pontuação (descendente)
                return (jogador_id != VENCEDOR, -pontos)
                
            for jogador_id, pontos in sorted(pontuacoes.items(), key=ordenar_placar):
                cor_placar = VERDE_CLARO if jogador_id == VENCEDOR else BRANCO
                texto_placar = FONTE_MENU.render(f"{jogador_id}: {pontos} pontos", True, cor_placar)
                rect_placar = texto_placar.get_rect(center=(LARGURA_TELA/2, pos_y_placar))
                tela.blit(texto_placar, rect_placar)
                pos_y_placar += 40
            
            # Botões
            pygame.draw.rect(tela, CINZA, botao_reiniciar); tela.blit(FONTE_MENU.render("Reiniciar Jogo", True, VERDE_CLARO), FONTE_MENU.render("Reiniciar Jogo", True, VERDE_CLARO).get_rect(center=botao_reiniciar.center))
            pygame.draw.rect(tela, CINZA, botao_sair); tela.blit(FONTE_MENU.render("Sair do Jogo", True, VERMELHO_CLARO), FONTE_MENU.render("Sair do Jogo", True, VERMELHO_CLARO).get_rect(center=botao_sair.center))
        else: # Tela de Espera Inicial ou Aguardando Fim da Partida
            if JOGADOR_ELIMINADO:
                texto_espera = FONTE_MENU.render("ELIMINADO. AGUARDANDO FIM DA PARTIDA...", True, VERMELHO_CLARO)
            else:
                texto_espera = FONTE_MENU.render("Aguardando oponente...", True, BRANCO)
            
            rect_espera = texto_espera.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2))
            tela.blit(texto_espera, rect_espera)
    else: # Jogo em andamento
        # Placar no canto superior esquerdo
        pos_y_placar = 10
        for jogador_id, pontos in sorted(pontuacoes.items(), key=lambda item: item[1], reverse=True):
            texto_placar = FONTE_PONTOS.render(f"{jogador_id}: {pontos}", True, AMARELO)
            tela.blit(texto_placar, (10, pos_y_placar))
            pos_y_placar += 30
            
        # Desenha apenas o jogador que está vivo
        if not JOGADOR_ELIMINADO: 
            tela.blit(nave_imagem, nave_rect)
            
        # Desenha apenas os oponentes que estão vivos (True = VIVO)
        for id_oponente, pos in oponentes_pos.items():
            if OPONENTES_ELIMINADOS.get(id_oponente, True):
                tela.blit(nave_imagem, nave_imagem.get_rect(center=(pos['x'], pos['y'])))
            
        for obs in obstaculos_ativos: tela.blit(asteroide_imagem, asteroide_imagem.get_rect(center=(obs['x'], obs['y'])))\
        
        for id_tiro, pos_tiro in tiros_ativos.items(): tela.blit(tiro_surface, tiro_surface.get_rect(center=(int(pos_tiro['x']), int(pos_tiro['y']))))


    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
client.loop_stop()
sys.exit()
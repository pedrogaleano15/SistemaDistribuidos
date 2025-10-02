# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time
import json
import random
import sys

# --- Configurações do Broker MQTT ---
BROKER_IP = "172.31.13.224"
BROKER_PORT = 50000
TOPICO_OBSTACULOS = "jogo/obstaculos"
TOPICO_EVENTOS = "jogo/eventos" # Novo tópico para escutar o início/fim

# --- Configurações do Jogo ---
NUM_OBSTACULOS_POR_RODADA = 15
LARGURA_TELA = 800
INTERVALO_GERACAO = 2
JOGO_INICIADO = False # Estado para controlar a geração

# Função chamada quando o cliente se conecta ao broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Gerador de Obstáculos: Conectado com sucesso ao broker!")
        # Assina o tópico de eventos para saber quando o jogo iniciar
        client.subscribe(TOPICO_EVENTOS)
    else:
        print("Gerador de Obstáculos: Falha na conexão, código de erro:", rc)
        sys.exit(1)

# Função chamada ao receber mensagens
def on_message(client, userdata, message):
    global JOGO_INICIADO
    try:
        payload = message.payload.decode("utf-8")
        topico = message.topic
        data = json.loads(payload)
        
        if topico == TOPICO_EVENTOS:
            evento = data.get('evento')
            
            if evento == 'jogo_iniciado':
                JOGO_INICIADO = True
                print("Gerador: Recebido sinal de INÍCIO. Começando a gerar obstáculos!")
            
            # Pausa a geração se o jogo terminar ou for reiniciado/saído
            elif evento in ['vitoria', 'jogo_reiniciado', 'jogador_saiu', 'todos_sairam']:
                JOGO_INICIADO = False
                print("Gerador: Jogo pausado/encerrado. Parando a geração de obstáculos.")
                
    except json.JSONDecodeError as e:
        print(f"Gerador: Erro ao processar mensagem JSON: {e}")

# Configura e conecta o cliente MQTT
client = mqtt.Client(client_id="GeradorObstaculos", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message # Adiciona o callback para eventos
client.connect(BROKER_IP, BROKER_PORT, 60)
client.loop_start()

print("Iniciando gerador de obstáculos. **Esperando sinal de início...**")

# Loop infinito para gerar obstáculos continuamente
while True:
    if JOGO_INICIADO: # SÓ GERA SE O JOGO ESTIVER INICIADO
        obstaculos_da_rodada = []
        for _ in range(NUM_OBSTACULOS_POR_RODADA):
            obstaculo = {
                "id": f"obs_{time.time()}_{random.randint(1000, 9999)}",
                "x": random.randint(30, LARGURA_TELA - 30),
                "y": -30,
                "raio": random.randint(15, 30),
                "velocidade_y": random.uniform(1.5, 4.0)
            }
            obstaculos_da_rodada.append(obstaculo)

        client.publish(TOPICO_OBSTACULOS, json.dumps(obstaculos_da_rodada))
        
        print(f"{NUM_OBSTACULOS_POR_RODADA} novos obstáculos gerados.")

    time.sleep(INTERVALO_GERACAO)
import pygame
#cores
preto = (0,0,0)
branco = (255,255,255)
vermelho = (255,0,0)
verde = (0,255,0)
azul = (0,0,255)

#padrão de tela para os desenhos
screen_width = 700
screen_height = 400
#Posição em x e y para iniciar o desenho
posX = screen_width/2
posY = screen_height/2
posX2 = screen_width/4
posY2 = screen_height/4
#tamanho padrão dos objetos
tam = 10
#variável cor
cor = verde
#inicializar a biblioteca
pygame.init()
#Montar a tela do jogo
tela=pygame.display.set_mode((screen_width,screen_height))
#Colocar um título na tela do jogo
pygame.display.set_caption("Meu primeiro jogo")
#auxiliar na finalização do jogo
sair=True
#Loop do jogo
while sair:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                posX -=10
            if event.key == pygame.K_RIGHT:
                posX +=10
            if event.key == pygame.K_UP:
                posY -=10
            if event.key == pygame.K_DOWN:
                posY +=10
        if pygame.mouse.get_pressed()[0]:
            cor = vermelho
            posX2=pygame.mouse.get_pos()[0]
            posY2=pygame.mouse.get_pos()[1]
        if pygame.mouse.get_pressed()[2]:
            cor = verde
            posX2=pygame.mouse.get_pos()[0]
            posY2=pygame.mouse.get_pos()[1]
    tela.fill(azul)
    pygame.draw.circle(tela,cor,[posX,posY],tam+20)
    pygame.draw.rect(tela,preto,[posX2,posY2,tam+100,tam+100])
    #atualzar a tela
    pygame.display.update()
#fechar a tela do jogo
pygame.display.quit()
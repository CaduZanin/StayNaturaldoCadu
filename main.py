import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
import json

pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Stay Natural do Cadu")
icone = pygame.image.load("recursos/imagens/icone.webp")
pygame.display.set_icon(icone)
branco = (255,255,255)
azul_claro = (0,200,255)
preto = (0, 0 ,0 )
natural = pygame.image.load("recursos/imagens/natural.png")
fundostart = pygame.image.load("recursos/imagens/academiastart.webp")
fundoJogo = pygame.image.load("recursos/imagens/atgym.jpg")
fundoDead = pygame.image.load("recursos/imagens/fundohospital.png")
trembo = pygame.image.load("recursos/imagens/trembo.png")
seringa = pygame.image.load("recursos/imagens/seringa.png")
trembosound = pygame.mixer.Sound("recursos/audios/audiocontra.mp3")
mortesound = pygame.mixer.Sound("recursos/audios/quandomorre.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/audios/fundogame.mp3")


fundostart = pygame.transform.scale(fundostart, (1000, 700)) 
trembo = pygame.transform.scale(trembo, (140,140)) 
natural = pygame.transform.scale(natural, (200,200))
fundoJogo = pygame.transform.scale(fundoJogo, (1000,700))
fundoDead = pygame.transform.scale(fundoDead, (1000, 700))
esperando_inicio = True
def jogar():
    largura_janela = 300
    altura_janela = 50
    def obter_nome():
        global nome
        nome = entry_nome.get()  # Obtém o texto digitado
        if not nome:  # Se o campo estiver vazio
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  # Exibe uma mensagem de aviso
        else:
            #print(f'Nome digitado: {nome}')  # Exibe o nome no console
            root.destroy()  # Fecha a janela após a entrada válida
    # Criação da janela principal
    root = tk.Tk()
    # Obter as dimensões da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    # Entry (campo de texto)
    entry_nome = tk.Entry(root)
    entry_nome.pack()

    # Botão para pegar o nome
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    # Inicia o loop da interface gráfica
    root.mainloop()
    

    posicaoXPersona = 500
    posicaoYPersona = 400
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXtrembo = 400
    posicaoYtrembo = -240
    velocidadetrembo = 1
    pygame.mixer.Sound.play(trembosound)
    pygame.mixer.music.play(-1)
    pontos = 0
    larguraPersona = 200
    alturaPersona = 200
    larguratrembo  = 140
    alturatrembo  = 140
    dificuldade  = 30
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 15
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -15
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
                
        posicaoXPersona = posicaoXPersona + movimentoXPersona                    
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 0
        elif posicaoXPersona >800:
            posicaoXPersona = 800
        
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        #pygame.draw.circle(tela, preto, (posicaoXPersona,posicaoYPersona), 40, 0 )
        tela.blit( natural, (posicaoXPersona, posicaoYPersona) )
        
        posicaoYtrembo = posicaoYtrembo + velocidadetrembo
        if posicaoYtrembo > 700:
            posicaoYtrembo = -140
            pontos = pontos + 1
            velocidadetrembo = velocidadetrembo + 1
            posicaoXtrembo = random.randint(0,1000)
            pygame.mixer.Sound.play(trembosound)
            
            
        tela.blit( trembo, (posicaoXtrembo, posicaoYtrembo) )
        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelstremboX = list(range(posicaoXtrembo, posicaoXtrembo + larguratrembo))
        pixelstremboY = list(range(posicaoYtrembo, posicaoYtrembo + alturatrembo))
        
        os.system("cls")
        # print( len( list( set(pixelstremboX).intersection(set(pixelsPersonaX))   ) )   )
        if  len( list( set(pixelstremboY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelstremboX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
        
        pygame.display.update()
        relogio.tick(120)


def start():
    larguraButtonStart = 165
    alturaButtonStart  = 40
    larguraButtonQuit = 165
    alturaButtonQuit  = 40
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 165
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 165
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 165
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 165
                    alturaButtonQuit  = 40
                    quit()
                    
            
            
        tela.fill(branco)
        tela.blit(fundostart, (0,0) )

        startButton = pygame.draw.rect(tela, azul_claro, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Matricular-se", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, azul_claro, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Continuar Frango", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(mortesound)
    larguraButtonStart = 165
    alturaButtonStart  = 40
    larguraButtonQuit = 165
    alturaButtonQuit  = 40
    
    
    root = tk.Tk()
    root.title("Tela da Morte")

    # Adiciona um título na tela
    label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    label.pack(pady=10)

    # Criação do Listbox para mostrar o log
    listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    # Adiciona o log das partidas no Listbox
    log_partidas = open("base.cadu", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
        
            
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0) )

        
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)
def tela_boas_vindas(nome):
            esperando_inicio = True
            while esperando_inicio:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if botao_iniciar.collidepoint(evento.pos):
                            esperando_inicio = False

                tela.fill(preto)
                tela.blit(fundostart, (0, 0))  # Ou um fundo específico para essa tela
                
                # Mensagem de boas-vindas
                texto_boas_vindas = fonteMenu.render(f"Bem-vindo, {nome}!", True, branco)
                texto_instrucao = fonteMenu.render("Evite as trembolonas usando as setas!", True, branco)
                tela.blit(texto_boas_vindas, (300, 200))
                tela.blit(texto_instrucao, (250, 250))
                
                # Botão "Iniciar"
                botao_iniciar = pygame.draw.rect(tela, azul_claro, (400, 350, 200, 50), border_radius=10)
                texto_botao = fonteMenu.render("INICIAR", True, preto)
                tela.blit(texto_botao, (460, 360))
                pygame.display.update()
                relogio.tick(60)
start()

import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados, escreverDados
import json
import math
import datetime
import pyttsx3  # Para síntese de voz (item 20)
import speech_recognition as sr

pygame.init()
inicializarBancoDeDados()
tamanho = (1000, 700)
tamanho_boasvindas = (100, 100)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Stay Natural do Cadu")
icone = pygame.image.load("recursos/imagens/icone.webp")
pygame.display.set_icon(icone)

# Cores
branco = (255, 255, 255)
azul_claro = (0, 200, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)
vermelho = (255,0,0)

# Carregar assets
natural = pygame.image.load("recursos/imagens/natural.png")
fundostart = pygame.image.load("recursos/imagens/academiastart.webp")
fundoJogo = pygame.image.load("recursos/imagens/atgym.jpg")
fundoDead = pygame.image.load("recursos/imagens/fundohospital.png")
trembo = pygame.image.load("recursos/imagens/trembo.png")
fundorecepcao = pygame.image.load("recursos/imagens/fundorecepcao.jpg")
ramonrandom = pygame.image.load("recursos/imagens/ramonrandom.png")  # Novo asset (item 14)
global halter
halter = pygame.image.load("recursos/imagens/halteresdecora.png")
global altura_halter 
global largura_halter
largura_halter = 130
altura_halter = 130
# Sons
trembosound = pygame.mixer.Sound("recursos/audios/audiocontra.mp3")
mortesound = pygame.mixer.Sound("recursos/audios/quandomorre.mp3")
pygame.mixer.music.load("recursos/audios/fundogame.mp3")
#direcoes
global direcao_animacao
direcao_animacao = "aumentando"
global contador_animacao
contador_animacao = 0

# Fontes
fonteMenu = pygame.font.SysFont("comicsans",18)
fonterecepcao = pygame.font.SysFont("comicsans", 40)
fonteMorte = pygame.font.SysFont("arial", 120)
fonteRanking = pygame.font.SysFont("arial", 24)
fontevoz = pygame.font.SysFont("comicsans", 20)
fontedead = pygame.font.SysFont("timesnewroman", 40)

# Redimensionar imagens
fundostart = pygame.transform.scale(fundostart, tamanho)
trembo = pygame.transform.scale(trembo, (140, 140))
natural = pygame.transform.scale(natural, (200, 200))
fundoJogo = pygame.transform.scale(fundoJogo, tamanho)
fundoDead = pygame.transform.scale(fundoDead, tamanho)
ramonrandom = pygame.transform.scale(ramonrandom, (150, 100))  # Item 14
fundorecepcao = pygame.transform.scale(fundorecepcao, (1000,700))
halter = pygame.transform.scale(halter, (130,130))
# --- FUNÇÃO: TELA DE BOAS-VINDAS (ITEM 9) ---
def tela_boas_vindas(nome_jogador):
    esperando_inicio = True
    recognizer = sr.Recognizer()
    
    while esperando_inicio:
        # Controles
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            # Tecla V ativa o reconhecimento
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_v:
                try:
                    with sr.Microphone() as source:
                        # Feedback visual
                        tela.fill(preto)
                        tela.blit(fundorecepcao, (0, 0))
                        tela.blit(fonterecepcao.render("Ouvindo... diga 'INICIAR'", True, vermelho), (300, 550))
                        pygame.display.update()
                        
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source, timeout=3)
                        comando = recognizer.recognize_google(audio, language="pt-BR").lower()
                        
                        if "iniciar" in comando:
                            esperando_inicio = False
                except Exception as e:
                    print(f"Erro no reconhecimento: {e}")
            
            # Clique no botão físico
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    esperando_inicio = False

        # Renderização
        tela.fill(preto)
        tela.blit(fundorecepcao, (0, 0))
        
        # Textos
        texto_boas_vindas = fonterecepcao.render(f"Bem-vindo, {nome_jogador}!", True, branco)
        texto_instrucao = fonterecepcao.render("Use as setas do eixo X para evitar as Trembolonas!", True, branco)
        tela.blit(texto_boas_vindas, (20, 20))
        tela.blit(texto_instrucao, (20, 500))
        
        # Botão
        pygame.draw.rect(tela, branco, (395, 595, 210, 60), 2, border_radius=12)
        botao_iniciar = pygame.draw.rect(tela, azul_claro, (400, 600, 200, 50), border_radius=10)
        texto_botao = fonterecepcao.render("INICIAR", True, preto)
        tela.blit(texto_botao, (410, 600))
        
        # Instrução de voz
        texto_voz = fontevoz.render("Pressione V e fale 'INICIAR'", True, branco)
        tela.blit(texto_voz, (700, 20))
        
        pygame.display.update()
        relogio.tick(60)

# --- FUNÇÃO PRINCIPAL DO JOGO ---
def jogar():
    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root = tk.Tk()
    root.title("Informe seu nickname")
    # Configurações para centralizar a janela
    largura_janela = 450
    altura_janela = 100 # Aumentei a altura para caber melhor o conteúdo
    
    # Obtém as dimensões da tela principal (do Pygame)
    largura_tela = root.winfo_screenmmwidth()  # Largura da tela do jogo (1000)
    altura_tela = root.winfo_screenheight()  # Altura da tela do jogo (700)
    
    # Calcula as coordenadas para centralizar
    pos_x = (largura_tela //2 + largura_janela ) 
    pos_y = (altura_tela //2 - altura_janela ) 
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.resizable(False, False)  # Impede redimensionamento
    
    # Campo de entrada
    tk.Label(root, text="Digite seu nome:").pack(pady=5)
    entry_nome = tk.Entry(root)
    entry_nome.pack(pady=5)
    
    # Botão de enviar
    tk.Button(root, text="Enviar", command=obter_nome).pack(pady=5)
    
    root.mainloop()

    tela_boas_vindas(nome)  # Mostra tela de boas-vindas

    # Variáveis do jogo
    posicaoXPersona = 500
    posicaoYPersona = 400
    movimentoXPersona = 0
    posicaoXtrembo = random.randint(0, 800)
    posicaoYtrembo = -140
    velocidadetrembo = 1
    pontos = 0
    pausado = False  # Item 11

    # Item 14: Objeto decorativo (ramonrandom)
    posicao_ramonrandom = [random.randint(0, 1000), random.randint(0, 700)]
    velocidade_ramonrandom = random.uniform(0.5, 1.5)

    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoXPersona = 15
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -15
                elif evento.key == pygame.K_SPACE:  # Item 11
                    pausado = not pausado
            elif evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    movimentoXPersona = 0

        if pausado:  # Lógica de pausa
            texto_pause = fonteMorte.render("PAUSE", True, branco)
            tela.blit(texto_pause, (350, 250))
            pygame.display.update()
            continue

        # Atualiza posições
        posicaoXPersona += movimentoXPersona
        posicaoXPersona = max(0, min(800, posicaoXPersona))
        
        posicaoYtrembo += velocidadetrembo
        if posicaoYtrembo > 700:
            posicaoYtrembo = -140
            pygame.mixer.Sound.play(trembosound)
            pontos += 1
            velocidadetrembo += 0.5
            posicaoXtrembo = random.randint(0, 800)

        # Item 14: Movimento da ramonrandom
        posicao_ramonrandom[0] -= velocidade_ramonrandom
        if posicao_ramonrandom[0] < -150:
            posicao_ramonrandom[0] = 1000
            posicao_ramonrandom[1] = random.randint(50, 200)

        # Desenhar cena
        tela.blit(fundoJogo, (0, 0))
        global altura_halter
        global largura_halter
        def animar():
            global direcao_animacao
            global contador_animacao
            if direcao_animacao == 'aumentando':
                if contador_animacao < 100:
                    contador_animacao += 1
                else:
                    direcao_animacao = 'diminuindo'
            else:
                if contador_animacao > 0:
                    contador_animacao -= 1
                else:
                    direcao_animacao = 'aumentando'

            escala = 1 + contador_animacao * 0.00115
            return escala
        escala = animar()
        nova_largura = int(largura_halter * escala)
        nova_altura = int(altura_halter * escala)
    
        #pega a superfície e coloca como image pro pygame entender que é a img
        image = pygame.transform.smoothscale(halter, (nova_largura,nova_altura))
        tela.blit(image,(820,20))
        

        tela.blit(ramonrandom, posicao_ramonrandom)  # Item 14
        tela.blit(natural, (posicaoXPersona, posicaoYPersona))
        tela.blit(trembo, (posicaoXtrembo, posicaoYtrembo))
        
        # Textos (Item 12)
        texto_pontos = fonteMenu.render(f"Pontos: {pontos}", True, branco)
        texto_pause_info = fonteMenu.render("Press SPACE to Pause", True, branco)
        tela.blit(texto_pontos, (15, 15))
        tela.blit(texto_pause_info, (20, 660))

        # Colisão
        if (abs(posicaoXPersona - posicaoXtrembo) < 124 and 
            abs(posicaoYPersona - posicaoYtrembo) < 124):
            data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            escreverDados(nome, pontos, data_hora)  # Item 15
            dead()

        pygame.display.update()
        relogio.tick(120)

# --- FUNÇÃO DE GAME OVER (ITEM 18) ---
def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(mortesound)

    # Carrega os últimos 5 registros
    try:
        with open("log.dat", "r") as f:
            registros = json.load(f)
        ultimos_5 = sorted(registros.items(), key=lambda x: x[1][0], reverse=True)[:5]
    except:
        ultimos_5 = []

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

        tela.blit(fundoDead, (0, 0))
        
        # Título
        texto_morte = fonteMorte.render("GAME OVER", True, (255, 0, 0))
        tela.blit(texto_morte, (200, 30))
        
        # Ranking (Item 18)
        y = 200
        for i, (nome_reg, (pontos_reg, data_reg)) in enumerate(ultimos_5):
            texto = fonteRanking.render(
                f"{i+1}. {nome_reg}: {pontos_reg} pts ({data_reg})", 
                True, branco
            )
            tela.blit(texto, (200, y))
            y += 40
        
        # Botões
        pygame.draw.rect(tela, azul_claro, (400, 500, 200, 50), border_radius=10)
        texto_reiniciar = fontedead.render("Reiniciar", True, preto)
        tela.blit(texto_reiniciar, (425, 500))
        
        pygame.draw.rect(tela, azul_claro, (400, 600, 200, 50), border_radius=10)
        texto_sair = fontedead.render("Sair", True, preto)
        tela.blit(texto_sair, (465, 600))
        
        pygame.display.update()
        relogio.tick(60)

    start()

# --- FUNÇÃO INICIAL ---
def start():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    jogar()
                elif quitButton.collidepoint(evento.pos):
                    pygame.quit()
                    quit()

        tela.blit(fundostart, (0, 0))
        
        startButton = pygame.draw.rect(tela, azul_claro, (10, 10, 165, 40), border_radius=15)
        startTexto = fonteMenu.render("Matricular-se", True, preto)
        tela.blit(startTexto, (25, 12))
        
        quitButton = pygame.draw.rect(tela, azul_claro, (10, 60, 165, 40), border_radius=15)
        quitTexto = fonteMenu.render("Continuar Frango", True, preto)
        tela.blit(quitTexto, (25, 62))
        
        pygame.display.update()
        relogio.tick(60)
        

start()
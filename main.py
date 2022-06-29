# Importamos las librerias que vamos a utilizar
import math
import random
import pygame  # Libreria especial para realizar juegos en python
from pygame import mixer  # Libreria para poner musica y sonidos dentro del juego

# Inicializamos pygame
pygame.init()

# Creamos la ventana para nuestro juego
screen = pygame.display.set_mode((800, 800))

# Le agregamos un limite a la velocidad de refresco de la pantalla
reloj = pygame.time.Clock()

# Titulo e icono de la ventana
pygame.display.set_caption("Snake  by: Diego Sandoval")
icon = pygame.image.load("snake.png")
pygame.display.set_icon(icon)

# importamos la fuente que utilizaremos para el texto
over_font = pygame.font.Font("Nintendo-DS-BIOS.ttf", 150)
reset_font = pygame.font.Font("Nintendo-DS-BIOS.ttf", 75)

# importamos y establecemos un loop en la musica de fondo
mixer.music.load("background1.mp3")
mixer.music.play(-1)


# Creamos un funcion para mostrar una imagen de fondo
def fondo():
    # Se carga y diibuja la imagen
    fondo_img = pygame.image.load("background.jpg")
    screen.blit(fondo_img, (0, 0))


# Creamos una funcion para mostrar el texto
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (170, 225))
    reset_tex = reset_font.render("Press Return to close", True, (255, 255, 255))
    screen.blit(reset_tex, (150, 360))


textoX = 10
textoY = 10
puntaje = 0


def mostrar_puntaje(x, y):
    global puntaje
    fuente_puntaje = pygame.font.Font("Nintendo-DS-BIOS.ttf", 55)
    score = fuente_puntaje.render("Puntaje: " + str(puntaje), True, (255, 255, 255))
    screen.blit(score, (x, y))



# cargamos la imagen deseada para la fruta
fresa_img = pygame.image.load("fruta.png")

# creamos el objeto (fruta) y le damos coordeanas de aparicion (estas seran aleatorias en toda la pantalla)

fresaX = random.randint(0, 760)
fresaY = random.randint(0, 760)


# Creamos la funcion para dibujar la fruta en la pantalla
def dibujar_fresa(x, y):
    fresa_rect = pygame.Rect(x, y, 40, 40)
    screen.blit(fresa_img, fresa_rect)


# Creamos funcion e ingresamos las coordenadas para dibujar el trofeo
trofeoX = 205
trofeoY = 15


def dibujar_trofeo(x, y):
    trofep_img = pygame.image.load("trofeo.png")
    screen.blit(trofep_img, (x, y))


# creamos a la serpiente y establecemos variables para su movimiento
serpienteX = 400
serpienteY = 400
serpienteX_mov = 0
serpienteY_mov = 0

# creamos una lista para guardar el cuerpo de la serpiente (que va ir en aumento)
cuerpo_lista = [(serpienteX, serpienteY)]


# Creamos la funcion de la serpiente para hacer su movimiento e interacciones

def serpiente():
    global serpienteX, serpienteY, fresaX, fresaY, puntaje
    serpienteX += serpienteX_mov  # con este aumento en las coordeanas da la sensacion de movimiento
    serpienteY += serpienteY_mov

    cuerpo_lista.append((serpienteX, serpienteY))  # agregamos a la lista las coordenadas de la serpiente

    # creamos un ciclo if en caso de colision entre la serpiente y la fruta

    colision = math.sqrt((math.pow(fresaX - serpienteX, 2)) + (
        math.pow(fresaY - serpienteY, 2)))  # Ecuacion de la distancia entre 2 puntos

    for (i, j) in cuerpo_lista:  # usamos el ciclo for para que el cuerpo pueda aumentar su tamaño
        pygame.draw.rect(screen, (51, 153, 255), [i, j, 40, 40])

    # si hay una distancia de 20 unidades la serpiente comenzara a crecer
    if colision < 20:
        while (fresaX, fresaY) in cuerpo_lista:
            continue

    # Para que la serpiente de sensacion de movimiento y no se este dibujando "sin fin" se elimina el ultimo bloque
    # A menos que este a 20 unidades de distancia de la fresa en ese caso si crece la serpiente
    else:
        del cuerpo_lista[0]

    if cuerpo_lista[-1] in cuerpo_lista[0:-2]:  # aqui detectamos cuando la serpiente choque consigo misma
        estado = "perdido"
        game_over_text()
        return estado

    # Creamos un ciclo if para que al colisionar se cree una nueva fruta de manera aleatoria
    elif colision < 8:

        # Creamos un sonido para cada vez que se consuma una fresa
        comer_music = mixer.Sound("increase sound.mp3")
        comer_music.set_volume(0.15)  # Fijamos un volumen del sonido para que no sea irritante
        comer_music.play()

        # incrementamos el puntaje cada que comemos una fresa y creamos otra fresa en coordenadas aleatorias
        puntaje += 1
        fresaX = random.randint(0, 760)
        fresaY = random.randint(0, 760)
        dibujar_fresa(fresaX, fresaY)


# Creamos una funcion para cuando se píerde el juego
def game_over():
    global cuerpo_lista  # hacemos global la lista con las variables serpienteX y serpienteY

    # Establecemos un ciclo if para cuando la serpiente intente salir de la pantalla lo que conduce a un GAME OVER
    if (serpienteX <= 0 or serpienteX >= 760) or (serpienteY <= 0 or serpienteY >= 760):
        game_over_text()

        estado = "perdido"
    else:
        estado = "normal"
    return estado


# Creamos una funcion para que se guarde la puntuacion del ultimo juego
def escribe_puntaje():
    file = open("Puntaje.txt", 'w')
    file.write("El puntaje del ultimo juego fue: ")
    file.write(str(puntaje))
    file.close()


# Creamos un ciclo para que la pantalla se muestre constantemente sin que se cierre

correr = True
while correr:

    # llamamos a la funcion del fondo
    fondo()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Crear forma de cerrar la ventana
            correr = False

        # Agregamos controles
        if event.type == pygame.KEYDOWN:  # Al presionar una tecla la imagen va a tener un cambio en el aumento en X y Y
            if event.key == pygame.K_UP:  # Agregamos opciones para cada tecla
                if serpienteY_mov != 2.5:  # Este ciclo if es para que si la serpiente va para abajo no pueda empezar a subir
                    serpienteX_mov = 0
                    serpienteY_mov = -2.5
            elif event.key == pygame.K_LEFT:
                if serpienteX_mov != 2.5:
                    serpienteX_mov = -2.5
                    serpienteY_mov = 0
            elif event.key == pygame.K_RIGHT:
                if serpienteX_mov != -2.5:
                    serpienteX_mov = 2.5
                    serpienteY_mov = 0
            elif event.key == pygame.K_DOWN:
                if serpienteY_mov != -2.5:
                    serpienteX_mov = 0
                    serpienteY_mov = 2.5
            else:
                continue

        # Con esto la imagen dara la ilusion de movimiento ya que estamos cambiando su ubicacion en la ventana

    # Mandamos a llamar las funciones para que se activen
    dibujar_fresa(fresaX, fresaY)
    mostrar_puntaje(textoX, textoY)
    dibujar_trofeo(trofeoX, trofeoY)
    game_over()
    serpiente()

    if game_over() == "perdido" or serpiente() == "perdido":
        # Establecemos un sonido que sonara cuando el juego se pierda
        pygame.mixer.music.set_volume(0)
        over_music = mixer.Sound("Game Over.wav")
        over_music.set_volume(0.2)
        over_music.play()

        # Cambiamos de lugar el texto de puntaje y trofeo
        textoX = 320
        textoY = 430
        trofeoX = 505
        trofeoY = 435

        # anulamos el movimiento de la serpiente para que no se mueva despues de perder
        serpienteX = 1000
        serpienteY = 1000
        serpienteX_mov = 0
        serpienteY_mov = 0
        escribe_puntaje()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break





    reloj.tick(60)
    pygame.display.update()  # Esta funcion es para que la pantalla constantemente se este actualizado

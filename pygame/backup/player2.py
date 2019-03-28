import pygame, rpyc, time
import pygame.examples.aliens

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        self.image = pygame.image.load("C:\Mikael\PPC\pygame\\car1.png")
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.origtop = self.rect.top
        self.facing = -1

    def move(self):
        self.rect.move_ip(600/15, 0)
        self.rect = self.rect.clamp(SCREENRECT)

def apertou(lista):
    for i in range(len(lista)):
        if(lista[i] == 1):
            return 1
    return 0

def main():
    c = rpyc.connect("localhost", 18861)
    pygame.init()
    jogador = 2
    size = width, height = 800,600
    screen = pygame.display.set_mode(size)
    black = 255, 255, 255
    finish = pygame.image.load("images\\finish.png")
    finishrect = finish.get_rect().move([150,5])
    car1 = pygame.image.load("cars\\p1.png")
    car1rect = car1.get_rect()
    car2 = pygame.image.load("cars\\p2.png")
    car2rect = car2.get_rect()
    road = pygame.image.load("images\\road.jpg")
    roadrect = road.get_rect().move([150,-5])
    grass = pygame.image.load("images\\grass.png")
    grassrect = grass.get_rect().move([0,0])
    car1rect = car1rect.move([450,500])
    car2rect = car2rect.move([250,500])
    speed = [0,-500/15]
    error_sound = pygame.mixer.Sound("sounds\error.wav")
    cont = 0
    pos1 = 0
    load = 0
    acertou = 0
    errou = 0
    n1 = pygame.image.load("icos\\number-1.png")
    n2 = pygame.image.load("icos\\number-1.png")
    n3 = pygame.image.load("icos\\number-1.png")
    n1rect = n1.get_rect().move([10,10])
    n2rect = n2.get_rect().move([42,10])
    n3rect = n3.get_rect().move([74,10])
    c.root.comeca()
    while c.root.get_winner() == 0:
        seq = c.root.get_seq(jogador)
        #n1 = pygame.image.load("C:\Mikael\PPC\pygame\\number-"+str(seq[0])+".png")
        if(load == 0):
            if(acertou):
                time.sleep(0.5)
                acertou = 0
            if(errou):
                time.sleep(1.5)
                errou = 0
            n1 = pygame.image.load("icos\\number-"+str(seq[0])+".png")
            n2 = pygame.image.load("icos\\number-"+str(seq[1])+".png")
            n3 = pygame.image.load("icos\\number-"+str(seq[2])+".png")
            load = 1
        n1rect = n1.get_rect().move([10,10])
        n2rect = n2.get_rect().move([42,10])
        n3rect = n3.get_rect().move([74,10])
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                _ = pygame.key.name(event.key)
                try:
                    if(int(_[1]) == seq[cont]):
                        cont = cont + 1
                        if(cont == 1):
                            n1 = pygame.image.load("icos\\accepted-"+str(seq[cont-1])+".png")
                            n1rect = n1.get_rect().move([10,10])
                        if(cont == 2):
                            n2 = pygame.image.load("icos\\accepted-"+str(seq[cont-1])+".png")
                            n2rect = n2.get_rect().move([42,10])
                        if(cont == 3):
                            n3 = pygame.image.load("icos\\accepted-"+str(seq[cont-1])+".png")
                            n3rect = n3.get_rect().move([74,10])
                    else:
                        if pygame.mixer and pygame.mixer.get_init():
                            error_sound.play()
                        if(cont == 0):
                            n1 = pygame.image.load("icos\\denied-"+str(seq[cont])+".png")
                            n1rect = n1.get_rect().move([10,10])
                        if(cont == 1):
                            n2 = pygame.image.load("icos\\denied-"+str(seq[cont])+".png")
                            n2rect = n2.get_rect().move([42,10])
                        if(cont == 2):
                            n3 = pygame.image.load("icos\\denied-"+str(seq[cont])+".png")
                            n3rect = n3.get_rect().move([74,10])
                        c.root.gera_seq(jogador)
                        errou = 1
                        cont = 0
                        load = 0
                    
                    if(cont == 3):
                        c.root.anda(jogador)
                        car2rect = car2rect.move(speed)
                        cont = 0
                        load = 0
                        acertou = 1
                except:
                    pass
        cont1 = c.root.get_cont(1)
        if(cont1 != pos1):
            aux = 500 + cont1*speed[1]
            car1rect = car1.get_rect().move([450, aux])
            pos1 = cont1
        
        screen.fill(black)
        screen.blit(grass, grassrect)
        screen.blit(road, roadrect)
        screen.blit(finish, finishrect)
        screen.blit(car1, car1rect)
        screen.blit(car2, car2rect)
        screen.blit(n1, n1rect)
        screen.blit(n2, n2rect)
        screen.blit(n3, n3rect)
        pygame.display.flip()
    
    confirm = 0
    while(not confirm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                confirm = 1
        
        screen.fill(black)
        screen.blit(grass, grassrect)
        screen.blit(road, roadrect)
        screen.blit(finish, finishrect)
        screen.blit(car1, car1rect)
        screen.blit(car2, car2rect)
        screen.blit(n1, n1rect)
        screen.blit(n2, n2rect)
        screen.blit(n3, n3rect)
        vic = pygame.image.load("images\win.png")
        if(c.root.get_winner() != jogador):
            vic = pygame.image.load("images\lose.png")
        
        vicrect = vic.get_rect().move([200,200])
        screen.blit(vic, vicrect)
        pygame.display.flip()

main()

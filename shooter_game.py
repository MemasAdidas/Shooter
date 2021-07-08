#Создай собственный Шутер!
#Код для игры шутер!
from pygame import *
from random import randint

mixer.init()
music=mixer.Sound('space.ogg')
music.play()



font.init()
font2 = font.SysFont('Arial',36)
font1= font.SysFont('Arial',80)
lose=font1.render("You Lose",True,(255,69,0))
win1=font1.render("You win!",True,(0,200,0))


score = 0
lost= 0
max_lost=3
goal=10
max_speed=3
ttt=0


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=player_speed
        #Хитбокс для спрайтов
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

ww=700
wh=500


class Player(GameSprite):
    def update(self):
        keys= key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < ww -70:
            self.rect.x += self.speed
    def fire(self):
        bullet= Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
        
            




class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > wh:
            self.rect.x= randint(80,ww-80)
            self.rect.y=0
            lost=lost+1

class Bullet(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y < 0:
            self.kill()
    



window=display.set_mode((ww,wh))
display.set_caption("shooter")
background=transform.scale(image.load("galaxy.jpg"),(ww,wh))
clock=time.Clock()
FPS=30

player = Player("rocket.png",250,430,80,50,7)
'''ufo= Enemy("ufo.png",200,0,2)'''

monsters= sprite.Group()
for i in range(1,6):
    ufo= Enemy("ufo.png",randint(80,ww-80),-40,80,50,randint(1,max_speed))
    monsters.add(ufo)

bullets= sprite.Group()













fire=mixer.Sound('fire.ogg')
finish=False

game= True
while game:
    for e in event.get():
        if e.type == QUIT:
            game= False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                player.fire()
    
    
    if not finish:
        window.blit(background,(0,0))
        ufo.update()
        player.update()
        monsters.update()
        text=font2.render("Счет: "+str(score),1,(255,255,255))
        propyck=font2.render("Пропущено: "+str(lost),True,(255,255,255))
        
        player.reset()
        
        ufo.reset()
        
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)
        window.blit(text,(10,20))
        window.blit(propyck,(10,50))
    
        collides= sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score = score+1
            ufo= Enemy("ufo.png",randint(80,ww-80),-40,80,50,randint(1,2))
            monsters.add(ufo)



        if sprite.spritecollide(player,monsters,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
            ttt=1
        if score >= goal: 
            finish = True
            window.blit(win1,(200,200))
    

            

    
    
        display.update()



    else:
        finish=False
        score=0
        lost=0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1,6):
            ufo= Enemy("ufo.png",randint(80,ww-80),-40,80,50,randint(1,3))
            monsters.add(ufo)
            if ttt == 1:
                max_speed=max_speed+1
                ttt=0 
    
    clock.tick(FPS)


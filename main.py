import pygame
import random as ran

pygame.init()

# SCREEN

WIDTH = 500
HEIGHT = 600
win = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

bg = pygame.image.load('img/bg.png').convert()
bgmusic = pygame.mixer.Sound('sound/bg.mp3')
bgmusic.play(-1)

# YOU THE PLAYER

player = pygame.Rect(WIDTH/2,HEIGHT-35, 32,32)
playerIMG = pygame.image.load('img/player2.png').convert_alpha()
playerHealth = 200
playerCoins = 0 # or points
playerX_change = 0

# BULLETS

ismachinegun = False
bullet = []
bulletIMG = pygame.image.load("img/bullet.png").convert_alpha()
bulletY_change = -3
bulletfire = pygame.mixer.Sound("sound/fire.mp3")
bullethit = pygame.mixer.Sound("sound/hit.mp3")
bulletleft = 15

# ENEMY OR ASTEROIDS

enemy = []
enemyIMG = []
enemyCount = 10
enemyAngle = []
enemyVelocity = []
enemyMovement = []
enemyRestart = 0
eneRes = 0

for e in range(int(enemyCount)):
	enemy.append(pygame.Rect(ran.randint(0,WIDTH-32),ran.randint(300,400),32,32))
	enemyIMG.append(pygame.image.load('img/projectile.png').convert_alpha())
	enemyAngle.append(0)
	enemyMovement.append(1)
# REAL ENEMY OR U.F.O

ufo = pygame.Rect(32,150,32,32)
ufeIMG = pygame.image.load('img/ufo.png').convert_alpha()
ufoX_change = 1
ufoX_change2 = 1
enemyHealth = 200

# UFO Fire Ball / Laser

laser = []
laserIMG = pygame.image.load("img/laser.png").convert_alpha()
laserfirerate = 200
lasertimer = 0
laserSound = pygame.mixer.Sound("sound/laser.mp3")

# FONTS

game_over = pygame.font.Font('font/STENCIL.TTF',64)
pauses = pygame.font.Font('font/STENCIL.TTF',64)
bulletText = pygame.font.Font('font/STENCIL.TTF', 11)
winer = pygame.font.Font('font/STENCIL.TTF', 64)
god_mode = pygame.font.Font('font/STENCIL.TTF',11)

# WRITE SOMETHING

def PauseText(win,text):
	pauseText = text.render("PAUSED", True, (255,255,255))
	win.blit(pauseText, (64*2, HEIGHT/2))

def gameOver(win,text):
	gameText = text.render("GAME OVER", True, (255,255,255))
	win.blit(gameText, (64+16,HEIGHT/2))

def mybullet(win,text):
	bulText = text.render("Bullets: " + str(bulletleft), True, (255,255,255))
	win.blit(bulText, (0,0))

def PlayerWin(win,text):
	winText = text.render("YOU WIN!", True, (255,255,255))
	win.blit(winText, (64+16+8, HEIGHT/2))

def GodMode(win,text):
	godText = text.render("Godmode: True", True, (255,255,255))
	win.blit(godText, (0,12))
# WALLPAPER

def background(win,img):
	win.blit(img, (0,0))

# ENTITY

def players(win,img,pos):
	win.blit(img, pos)

def bullets(win,img,pos):
	win.blit(img,pos)

def enemyimg(win,img,pos,angle):
	newimg = pygame.transform.rotate(img, angle)
	win.blit(newimg,pos)

def ufoimg(win,img,pos):
	win.blit(img, pos)

def enemyBullet(win,img,pos):
	win.blit(img,pos)

# BUFFS for image

def buff(win,img,pos):
	win.blit(img, pos)

# Functions

suggestedSizex= 200
suggestedSizey= 20
border=2

def healthBar(posx,posy,sizex,sizey,border, health):
	pygame.draw.rect(win, (255,255,255),(posx,posy,sizex+border,sizey+border))
	pygame.draw.rect(win, (255,0,0), (posx + border, posy+border, sizex -border, sizey-border))
	pygame.draw.rect(win, (0,255,0), (posx + border, posy+border, health -border, sizey-border))


# BUFF

buff1 = pygame.image.load('img/cratebullet.png').convert_alpha()
buff2 = pygame.image.load('img/heartcrate.png').convert_alpha()
buff3 = pygame.image.load('img/damagebuff.png').convert_alpha()

bufflist = []
bufflist2 = []
bufflist3 = []

buffrate = 0.15 # 15% chance to get by destroying asteroid || but only you
buffrate3 = 0.01# 10% chance drop by hitting enemy
# VARIABLE

enemyDamage = 5
playerDamage = 5

isFinalPhase = False
isbuffed = False
bufftimer = 0

isgod=  False

# GAME LOOP

run = True
pause = False
gamepause = False

while run:
	for event in pygame.event.get():
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_p:
				pause = False
			if event.key == pygame.K_g:
				isgod = False
		if event.type == pygame.QUIT:
			run = False
			pygame.quit

	while not pause:
		background(win,bg)
		players(win,playerIMG, (player.x,player.y))
		ufoimg(win,ufeIMG, (ufo.x,ufo.y))
		mybullet(win,bulletText)
		clock.tick(200)
		accelerate = 4 * ufoX_change
		
		MOUSEBUTTONDOWN = pygame.mouse.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					playerX_change = -1
				if event.key == pygame.K_d:
					playerX_change = 1
				if event.key == pygame.K_SPACE:
					if bulletleft > 0:
						bullet.append(pygame.Rect(player.x+12,player.y, 8,8))
						bulletfire.play()
						bulletleft -= 1
			if MOUSEBUTTONDOWN[0] == 1:
				bulletleft += 3
				print("CHEAT DETECTED")

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_d:
					playerX_change = 0
				if event.key == pygame.K_g:
					isgod = True
				if event.key == pygame.K_p:
					pause = True
					PauseText(win,pauses)
	# PLAYER MOVEMENT
		player.x += playerX_change

		if player.x > WIDTH:
			player.x = -32
		if player.x < -32:
			player.x = WIDTH
		
	# REAL ENEMY OR UFO MOVEMENT

		ufo.x += ufoX_change

		if ufo.x >= WIDTH-32 or ufo.x <= 0:
			ufoX_change *= -1
			ufoX_change2 *= -1
			if isFinalPhase:
				ufo.y += 20


		if enemyHealth <= 100: # second form
			ufoX_change = ufoX_change2 * 3
			laserfirerate = 100
			enemyDamage = 10
			ufeIMG = pygame.image.load('img/ufo2.png').convert_alpha()

		if enemyHealth <= 75: # third form
			laserfirerate = 50
			ufeIMG = pygame.image.load('img/ufo3.png').convert_alpha()

		if enemyHealth <= 50: # Pray for WIN FINAL FORM !!
			ufoX_change = ufoX_change2 * 5
			isFinalPhase = True
			laserfirerate= 125
			ufeIMG = pygame.image.load('img/ufo4.png').convert_alpha()

	# BUFF
		for buffa in range(len(bufflist)):
			bufflist[buffa].y += 1
			buff(win,buff1,(bufflist[buffa].x,bufflist[buffa].y))

		for buffa1, buffa2 in enumerate(bufflist):
			if bufflist[buffa1].colliderect(player):
				bulletleft += 5 
				del bufflist[buffa1]
			if buffa2.y >= HEIGHT+16:
				del bufflist[buffa1]
		# buff 2
		if lasertimer % 1000 == 0:
			bufflist2.append(pygame.Rect(ran.randint(32,WIDTH-32),0,16,16))
		for buffb in range(len(bufflist2)):
			bufflist2[buffb].y += 1
			buff(win,buff2,(bufflist2[buffb].x,bufflist2[buffb].y))

		for buffb1, buffb2 in enumerate(bufflist2):
			if bufflist2[buffb1].colliderect(player):
				if playerHealth <= 200:
					playerHealth = 200
				else:
					playerHealth += 10
				del bufflist2[buffb1]
			if buffb2.y >= HEIGHT+16:
				del bufflist2[buffb1]

		# buff 3
		if isbuffed:
			playerDamage = 10
			bulletIMG = pygame.image.load('img/bulletcrit.png').convert_alpha()
			bufftimer += 1
			if bufftimer % 3000 == 0:
				isbuffed = False
				bufftimer = 0
				playerDamage = 5
				bulletIMG = pygame.image.load('img/bullet.png').convert_alpha()


		for buffd in range(len(bufflist3)):
			bufflist3[buffd].y += 1
			buff(win,buff3,(bufflist3[buffd].x,bufflist3[buffd].y))
			if bufflist3[buffd].colliderect(player):
				playerDamage += 5

		for buffd1, buffd2 in enumerate(bufflist3):
			if bufflist3[buffd1].colliderect(player):
				isbuffed = True
				del bufflist3[buffd1]
			if buffd2.y >= HEIGHT+16:
				del bufflist3[buffd1]

	# COLLISION of player and ufo
		if ufo.colliderect(player):
			gameOver(win, game_over)
			pause = True

	# PROJECTILE

		for e in range(len(enemy)):
			enemyAngle[e] += -1
			enemyimg(win,enemyIMG[e], (enemy[e].x, enemy[e].y), enemyAngle[e])
			enemy[e].x += enemyMovement[e]
			if enemy[e].right >= WIDTH or enemy[e].left <= 0:
				enemyMovement[e] *= -1
			if enemy[e].bottom <= 32 or enemy[e].top >= HEIGHT-32:
				enemyMovement[e] *= -1
	# BULLET MOVEMENT
		for b in range(len(bullet)):
			bullet[b].y += bulletY_change
			bullets(win,bulletIMG, (bullet[b].x,bullet[b].y))
	
		for pls,bulletb in enumerate(bullet):
			if bulletb.y <= 0:
				del bullet[pls]
	# LASER MOVEMENT
		lasertimer += 1

		if lasertimer % laserfirerate == 0:
			if not isFinalPhase:
				laser.append(pygame.Rect(ufo.x,ufo.y,16,16))
			if enemyHealth <= 100:
				laser.append(pygame.Rect(ufo.x+16,ufo.y,16,16))
			if isFinalPhase:
				laser.append(pygame.Rect(ufo.x,ufo.y+8,16,16))
				laser.append(pygame.Rect(ufo.x-16,ufo.y,16,16))
			laserSound.play()
		for t in range(len(laser)):
			laser[t].y += 2 # 2 = speed
			enemyBullet(win,laserIMG, (laser[t].x,laser[t].y))
	
		for a,z in enumerate(laser):
			if z.y >= HEIGHT:
				del laser[a]
	# COLLISION oh it work
		for x in range(len(bullet)):
			for y in range(enemyCount):
				if bullet[x].colliderect(enemy[y]):
					if not isbuffed:
						bullet[x].y = -3
						enemy[y].y = -30 * HEIGHT
						enemy[y].x = -30 * WIDTH
						enemyMovement[y] = 0
						bullethit.play()
						enemyRestart += 1
						bulletleft += 3
					if isbuffed:
						enemy[y].y = -30 * HEIGHT
						enemy[y].x = -30 * WIDTH
						enemyMovement[y] = 0
						bullethit.play()
						enemyRestart += 1
						bulletleft += 3
					if ran.random() < buffrate:
						bufflist.append(pygame.Rect(ran.randint(32,WIDTH-32),0,16,16))

			if bullet[x].colliderect(ufo):
				bullet[x].y = -3
				enemyHealth -= playerDamage
				bullethit.play()
				if ran.random() < buffrate3:
					bufflist3.append(pygame.Rect(ufo.x,ufo.y,16,16))
	
		for q in range(len(laser)):
			for w in range(enemyCount):
				if laser[q].colliderect(enemy[w]):
					enemy[w].y = -30 * HEIGHT
					enemyRestart += 1
					enemy[w].x = -30 * WIDTH
					bullethit.play()

			if laser[q].colliderect(player):
				laser[q].y = HEIGHT + 3
				playerHealth -= enemyDamage
				bullethit.play()
		while enemyRestart == enemyCount:
			eneRes += 1
			if eneRes >= enemyCount:
				eneRes = 0
				enemyRestart = 0

			enemy[eneRes].x = ran.randint(32,WIDTH-32)
			enemy[eneRes].y = ran.randint(300,400)
			enemyMovement[eneRes] = 1
		players(win,playerIMG, (player.x,player.y))
		healthBar(WIDTH-200-border*2,40, suggestedSizex,suggestedSizey, border, enemyHealth)
		healthBar(0+border*2,40, suggestedSizex,suggestedSizey, border, playerHealth)
		if isgod:
			GodMode(win, god_mode)
			playerHealth = 200
		if playerHealth <= 1:
			playerHealth = 1
			gameOver(win, game_over)
			gamepause = True
		if enemyHealth <= 1:
			enemyHealth = 1
			PlayerWin(win, winer)
			gamepause = True
		pygame.display.update()
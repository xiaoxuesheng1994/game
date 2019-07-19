# 创建一个Pygame精灵
import pygame
import random
from os import path

WIDTH,HEIGHT = 480,600
player_width = 35
enemy_width = 30
#enemy_size = (30,30)

enemy_split_width = 20
enemy_split_size = (20,20)
player_size = (35,35)
bullet_width = 5
bullet_length = 10
bullet_size = (10,15)
explosion_size = (30,30)
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
color_p = (0,255,0)
color_e = (255,0,0)
color_b = (0,0,0)
new_enemy_generate_interval = 500
last_enemy_generate_time = 0
missile_lifetime = 10000
missile_interval = 500

game_state = 0

class Player(pygame.sprite.Sprite): #Simple base class for visible game objects.
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) # ???
		#self.image=pygame.Surface((player_width,player_width))  # 精灵图像设置为Surface（默认为矩形），存在self.image里
		#self.image = player_image
		self.image = pygame.transform.scale(pygame.transform.flip(player_img,False,True),player_size) # 翻转图像 False不左右翻转，True上下翻转
		self.image.set_colorkey(black)   # 去除掉图片中黑色的部分
		#self.image.fill(color_p)         # 填充颜色
		self.rect = self.image.get_rect()  #获取精灵的位置信息，存在self.rect里
		self.radius = player_width//2
		self.direction = 1
		self.rect.center = (WIDTH/2,HEIGHT-player_width/2)  #出生位置初始化
		#self.rect.bottom = HEIGHT
		self.hp = 100
		self.lives = 3
		self.score = 0

		self.hidden = False
		self.hide_time = 0

		self.is_missile_firing = False
		self.start_missile_time = 0
		self.last_missile_time = 0




	def update(self):
		#self.image = pygame.transform.scale(player_img,player_size)
		key_state = pygame.key.get_pressed() # get the state of all keyboard buttons
		if key_state[pygame.K_LEFT]:
			self.rect.x -= 5
		if key_state[pygame.K_RIGHT]:
			self.rect.x += 5 
		if key_state[pygame.K_UP]:
			self.rect.y -= 5
		if key_state[pygame.K_DOWN]:
			self.rect.y += 5

		if self.rect.right >= WIDTH:
			self.rect.right = WIDTH
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.bottom >= HEIGHT:
			self.rect.bottom = HEIGHT
		# if self.rect.top <= 0:
		# 	self.rect.top = 0


		now = pygame.time.get_ticks()
		if self.hidden and now - self.hide_time >1000:
			self.hidden = False
			self.rect.bottom = HEIGHT


		if self.is_missile_firing:
			if now - self.start_missile_time < missile_lifetime:
				if now - self.last_missile_time > missile_interval:
					missile = Missile(self.rect.center)
					missiles.add(missile)
					self.last_missile_time = now
			else:
				self.is_missile_firing = False

		
	def shoot(self):
		bullet = Bullet(self.rect.centerx,self.rect.centery)
		bullets.add(bullet)
		shoot_sound.play()
		
		# self.rect.x += self.direction*5
		# if self.rect.right >= WIDTH:
		# 	self.direction = -1
		# if self.rect.left <= 0:
		# 	self.direction = 1
		# if self.rect.left > 480:
		# 	self.rect.right = 0

	def hide(self):
		self.hidden = True
		self.rect.y = -2000
		self.hide_time = pygame.time.get_ticks()

	def fire_missile(self):
		self.is_missile_firing = True
		self.start_missile_time = pygame.time.get_ticks()


class Enemy(pygame.sprite.Sprite): #Simple base class for visible game objects.
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #
		#self.image=pygame.Surface((enemy_width,enemy_width))  # 精灵图像设置为Surface（默认为矩形），存在self.image里
		#self.image = enemy_img
		img_width = random.randint(20,50)
		enemy_size = (img_width,img_width) 
		self.image = pygame.transform.scale(enemy_img,enemy_size) # 缩放图片
		self.image.set_colorkey(black) 
		self.image_origin = self.image.copy()  # 保存一份原始图像

		
		#self.image.fill(color_e)         # 填充颜色
		self.rect = self.image.get_rect()  #获取精灵的位置信息，存在self.rect里
		self.radius = img_width//2
		#pygame.draw.circle(self.image, (255,0,0),self.rect.center,self.radius)
		self.direction_x = 1
		self.direction_y = 1
		self.rect.center = (random.randint(0,WIDTH),-img_width/2)  #出生位置初始化		
		self.vx = random.randint(-2,2)  # 横向速度初始化
		self.vy = random.randint(2,5)	#纵向速度初始化

		self.last_rotate_time = pygame.time.get_ticks()
		self.rotate_speed = random.randint(-5,5) # 旋转速度
		self.rotate_angle = 0 #旋转角度


	def update(self):
		self.rect.x += self.direction_x*self.vx
		self.rect.y += self.direction_y*self.vy
		if self.vx >= 0:
			if self.rect.right >= WIDTH:
				self.direction_x = -1
			if self.rect.left <= 0:
				self.direction_x = 1
		else:
			if self.rect.right >= WIDTH:
				self.direction_x = 1
			if self.rect.left <= 0:
				self.direction_x = -1			


		if self.rect.bottom >= HEIGHT:
			self.direction_y = -1
		if self.rect.top <= 0:
			self.direction_y = 1

		old_center = self.rect.center
		self.rotate()
		self.rect = self.image.get_rect()
		self.rect.center = old_center

		# now = pygame.time.get_ticks() 
		# if now - self.last_rotate_time > 30:
		# 	self.image = pygame.transform.rotate(self.image,self.rotate_speed)  #rotate an image
		# 	self.last_rotate_time = now

	def rotate(self):
		now = pygame.time.get_ticks() 
		if now - self.last_rotate_time > 30:
			self.rotate_angle = (self.rotate_angle+self.rotate_speed)%360
			self.image = pygame.transform.rotate(self.image_origin,self.rotate_angle)  #rotate an image
			self.last_rotate_time = now



class Bullet(pygame.sprite.Sprite): #Simple base class for visible game objects.
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self) #
		#self.image=pygame.Surface((bullet_width,bullet_width))  # 精灵图像设置为Surface（默认为矩形），存在self.image里
		#self.image = bullet_img
		self.image =  pygame.transform.scale(bullet_img, bullet_size )
		self.image.set_colorkey(black) 
		#self.image.fill(color_b)         # 填充颜色
		self.rect = self.image.get_rect()  #获取精灵的位置信息，存在self.rect里
		self.rect.centerx = x
		self.rect.centery = y

	def update(self):
		self.rect.y -= 10

class Explosion(pygame.sprite.Sprite): #Simple base class for visible game objects.
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self) #
		#self.image=pygame.Surface((bullet_width,bullet_width))  # 精灵图像设置为Surface（默认为矩形），存在self.image里
		self.image =  pygame.transform.scale(explosion_animation[0],explosion_size)
		self.image.set_colorkey(black) 
		#self.image.fill(color_b)         # 填充颜色
		self.rect = self.image.get_rect()  #获取精灵的位置信息，存在self.rect里
		self.rect.center = center
		self.frame = 0
		self.last_time = pygame.time.get_ticks() #获取游戏开始后已经经过了多少微秒，给Explosion添加一个last_time属性，记录上次播放时间
		#explosion_sound.play()

	def update(self):

		now = pygame.time.get_ticks()
		if now - self.last_time > 30:
			if self.frame < len(explosion_animation):
				self.image = pygame.transform.scale(explosion_animation[self.frame],explosion_size)
				self.frame += 1
			else:
				self.kill()
		self.image.set_colorkey(black) 


class Enemy_split(pygame.sprite.Sprite): #Simple base class for visible game objects.
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self) #
		#self.image=pygame.Surface((enemy_width,enemy_width))  # 精灵图像设置为Surface（默认为矩形），存在self.image里
		#self.image = enemy_img
		self.image = pygame.transform.scale(enemy_split_img ,enemy_split_size) # 缩放图片
		self.image.set_colorkey(black) 
		
		#self.image.fill(color_e)         # 填充颜色
		self.rect = self.image.get_rect()  #获取精灵的位置信息，存在self.rect里
		self.rect.center = center          #出生位置初始化	
		self.radius = enemy_split_width//2
		#pygame.draw.circle(self.image, (255,0,0),self.rect.center,self.radius)
		self.direction_x = 1
		self.direction_y = 1
			
		self.vx = random.randint(-2,2)  # 横向速度初始化
		self.vy = random.randint(2,5)	#纵向速度初始化

	def update(self):
		self.rect.x += self.direction_x*self.vx
		self.rect.y += self.direction_y*self.vy
		if self.vx >= 0:
			if self.rect.right >= WIDTH:
				self.direction_x = -1
			if self.rect.left <= 0:
				self.direction_x = 1
		else:
			if self.rect.right >= WIDTH:
				self.direction_x = 1
			if self.rect.left <= 0:
				self.direction_x = -1			


		if self.rect.bottom >= HEIGHT:
			self.direction_y = -1
		if self.rect.top <= 0:
			self.direction_y = 1

class Powerup(pygame.sprite.Sprite): #Simple base class for visible game objects.
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self) #
		random_num = random.random()
		if random_num <0.5:
			self.type = 'add_hp'
		elif random_num < 0.8:
			self.type = 'add_missile'
		else:
			self.type = 'add_life'
		self.image = powerup_imgs[self.type]
		self.rect = self.image.get_rect()
		self.image.set_colorkey(black)
		self.rect.center = center

	def update(self):
		self.rect.y += 3

class Missile(pygame.sprite.Sprite): #Simple base class for visible game objects.
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self) 
		self.image = missile_img
		self.rect = self.image.get_rect()
		self.image.set_colorkey(black)
		self.rect.center = center

	def update(self):
		self.rect.y -= 5

def draw_ui():
	pygame.draw.rect(screen,green,(10,10,player.hp,15))
	pygame.draw.rect(screen,white,(10,10,100,15),2)  # 2表示只画一个框

	draw_text('score='+str(player.score), screen, white,20, WIDTH/2, 10)

	player_life_img_rect = player_life_img.get_rect()
	player_life_img_rect.right = WIDTH-10
	player_life_img_rect.top = 10
	for i in range(player.lives):
		screen.blit(player_life_img, player_life_img_rect)
		player_life_img_rect.right -= player_life_img_rect.width + 10

def draw_text(text, surface, color, font_size, x, y):
	font_name = pygame.font.match_font('arial') # find a specific font on the system
	font = pygame.font.Font(font_name,font_size) # create a new Font object from a file, Font(object, size) -> Font
	text_surface = font.render(text,True,color)       #draw text on a new Surface
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surface.blit(text_surface,text_rect)

def show_menu():
	global game_state, screen

	screen.blit(background_img,background_rect)

	draw_text('Space Shooter!', screen, white, 40, WIDTH/2, 100)
	draw_text('Press Space key to start', screen, white, 20, WIDTH/2, 300)
	draw_text('Press Esc key to quit!', screen, white, 20, WIDTH/2, 350)

	event_list = pygame.event.get()
	for event in event_list:
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				quit()
			if event.key == pygame.K_SPACE:
				game_state = 1

	pygame.display.flip() 


pygame.mixer.pre_init(44100,-16,2,2048)
pygame.mixer.init()

pygame.init()

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("My Game") 
clock = pygame.time.Clock()  #create an object to help track time, pygame添加FPS控制

img_dir = path.join(path.dirname(__file__),'img') # 当前程序所在目录加上'img'文件夹, 变成新的路径

background_dir = path.join(img_dir,'background.png')
background_img = pygame.image.load(background_dir).convert() # convert 的作用是把图片的格式转化成更容易处理的格式
background_rect = background_img.get_rect() #获取background图像的尺寸信息

player_dir = path.join(img_dir,'spaceShips_002.png')
player_img = pygame.image.load(player_dir).convert()

enemy_dir = path.join(img_dir,'spaceMeteors_001.png')
enemy_img = pygame.image.load(enemy_dir).convert()

bullet_dir = path.join(img_dir,'spaceMissiles_001.png')
bullet_img = pygame.image.load(bullet_dir).convert()

missile_dir = path.join(img_dir,'spaceMissiles_003.png')
missile_img = pygame.image.load(missile_dir).convert()


enemy_split_dir = path.join(img_dir,'spaceMeteors_002.png')
enemy_split_img = pygame.image.load(enemy_dir).convert()

player_life_dir = path.join(img_dir,'heartFull.png')
player_life_img = pygame.transform.scale(pygame.image.load(player_life_dir).convert(),(15,15))
player_life_img.set_colorkey((0,0,0))

powerup_imgs = {}
powerup_add_hp_dir = path.join(img_dir,'gem_red.png')
powerup_imgs['add_hp'] = pygame.image.load(powerup_add_hp_dir).convert()


powerup_add_life_dir = path.join(img_dir,'heartFull.png')
powerup_imgs['add_life'] = pygame.image.load(powerup_add_life_dir).convert()

powerup_add_missile_dir = path.join(img_dir,'gem_yellow.png')
powerup_imgs['add_missile'] = pygame.image.load(powerup_add_missile_dir).convert()





sound_dir = path.join(path.dirname(__file__),'sound')
shoot_sound = pygame.mixer.Sound(path.join(sound_dir,'Laser_shoot12.wav'))  #Create a new Sound object from a file or buffer object
explosion_sound = pygame.mixer.Sound(path.join(sound_dir,'Explosion3.wav'))

pygame.mixer.music.load(path.join(sound_dir,'s8bgm.mp3'))







explosion_animation = []
for i in range(9):
	explosion_dir = path.join(img_dir,'regularExplosion0{}.png'.format(i))
	explosion_img = pygame.image.load(explosion_dir).convert()
	explosion_animation.append(explosion_img)

# 实例化
player = Player()
enemys = pygame.sprite.Group() #A container class to hold and manage multiple Sprite objects.
# for i in range(10):
# 	enemy = Enemy()
# 	enemys.add(enemy)

bullets = pygame.sprite.Group()

explosions = pygame.sprite.Group()

enemys_split = pygame.sprite.Group()

powerups = pygame.sprite.Group()

missiles = pygame.sprite.Group()



game_over = False
pygame.mixer.music.play(loops=-1)  # 播放背景音乐
while not game_over:
	clock.tick(60)
	if game_state == 0:
		show_menu()
	elif game_state == 1:
		now = pygame.time.get_ticks()
		if now - last_enemy_generate_time > new_enemy_generate_interval:
			enemy = Enemy()
			enemys.add(enemy)
			last_enemy_generate_time = now



		event_list = pygame.event.get()   # get events from the queue
		# if len(event_list)>0
		# 	print(event_list)
		for event in event_list:
			if event.type == pygame.QUIT:  #判断用户是否按了窗口的关闭键
				game_over = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE: #判断用户按下ESC键
					game_over = True
				if event.key == pygame.K_SPACE:
					player.shoot()
			# if event.type == pygame.MOUSEMOTION:  # 通过判断是鼠标移动事件来找到event.pos
			# 	mouse_pos = event.pos
			# 	p
		mouse_x,mouse_y = pygame.mouse.get_pos() #get the mouse cursor position
		 

		#hits = pygame.sprite.spritecollide(player, enemys, False, pygame.sprite.collide_rect_ratio(0.7)) # 调整碰撞检测绑定框的比例，在碰撞检测函数中加入该参数
		hits = pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_circle) #调整碰撞检测函数类型
		# if hits:
		# 	game_over = True
		for hit in hits:
			player.hp -= hit.radius*1
			if player.hp < 0:
				player.lives -= 1
				player.hp = 100
				player.hide()
				if player.lives == 0:
					game_over = True

		b_e_hits = pygame.sprite.groupcollide(enemys,bullets,True,True)
		#if b_e_hits:
			# enemy = Enemy()
			# enemys.add(enemy)
		for hit in b_e_hits:
			explosion = Explosion(hit.rect.center)
			explosions.add(explosion)
			explosion_sound.play()
			for i in range(2):
				enemy_split = Enemy_split(hit.rect.center)
				enemys_split.add(enemy_split)

			player.score += hit.radius
			if random.random() > 0.1: # 返回一个0—1之间的随机数
				powerup = Powerup(hit.rect.center)
				powerups.add(powerup)

		p_p_hits = pygame.sprite.spritecollide(player,powerups,True,pygame.sprite.collide_circle)
		for hit in p_p_hits:
			if hit.type == 'add_hp':
				player.hp += 50
				if player.hp > 100:
					player.hp = 100
			elif hit.type == 'add_life':
				player.lives += 1
				if player.lives > 3:
					player.lives = 3
			else:
				player.fire_missile()


		m_e_hits = pygame.sprite.groupcollide(enemys,missiles,True,True)
		#if b_e_hits:
			# enemy = Enemy()
			# enemys.add(enemy)
		for hit in m_e_hits:
			explosion = Explosion(hit.rect.center)
			explosions.add(explosion)
			explosion_sound.play()
			for i in range(2):
				enemy_split = Enemy_split(hit.rect.center)
				enemys_split.add(enemy_split)

			player.score += hit.radius
			if random.random() > 0.1: # 返回一个0—1之间的随机数
				powerup = Powerup(hit.rect.center)
				powerups.add(powerup)

		#b_es_split_hits = pygame.sprite.groupcollide(bullets,enemys_split,True,True)


		player.update()
		enemys.update() 
		bullets.update()
		explosions.update()
		powerups.update()
		missiles.update()
		#enemys_split.update()

		

		#screen.fill((254,221,85))  # fill the screen with a solid color
		screen.blit(background_img,background_rect)
		# pygame.draw.rect(screen,(0,255,0),(100,100,50,80))          # draw a rectangle shape 在哪画，颜色，矩形左上角位置和长宽
		# pygame.draw.circle(screen,(0,0,255),(300,300),50)
		# pygame.draw.ellipse(screen,(18,140,135),(200,100,50,80))

		screen.blit(player.image,player.rect) #被画的Surface.blit(要画的Surface,(X坐标，Y坐标))
		enemys.draw(screen)
		bullets.draw(screen)
		explosions.draw(screen) 
		powerups.draw(screen)
		missiles.draw(screen)
		#enemys_split.draw(screen)
		draw_ui()

		pygame.display.flip()       # Update the full display Surface to the screen
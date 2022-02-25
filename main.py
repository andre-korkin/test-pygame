import sys
import pygame


def run():
	pygame.init()
	window = pygame.display
	window.set_caption('Test')

	#------------------------------
	WIN_WIDTH = 800
	WIN_HEIGHT = 600
	screen = window.set_mode((WIN_WIDTH, WIN_HEIGHT))
	screen_rect = screen.get_rect()

	BLACK = (0, 0, 0)
	RED = (255, 0, 0)

	#------------------------------
	GUN_WIDTH = 50
	GUN_STEP = 3
	gun = pygame.image.load('./img/gun.jpg')
	gun_rect = gun.get_rect()
	gun_rect.bottom = screen_rect.bottom - 20
	gun_x = 0
	gun_move_right = False
	gun_move_left = False

	#------------------------------
	BULLIT_STEP = 1
	bullit = False
	bul_x = 0
	bul_y = 0

	#------------------------------
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if bul_y <= 0:
						bullit, bul_x, bul_y = bullitCreate(RED, gun_rect)
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					gun_move_left, gun_move_right = gunMove(event.key, True)
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					gun_move_left, gun_move_right = gunMove(event.key, False)

		gun_x = getGunStep(gun_move_right, gun_move_left, GUN_WIDTH, WIN_WIDTH, gun_x, GUN_STEP)
		if bul_y > 0:
			bul_y -= BULLIT_STEP
		else:
			bullit = False
		allRender(screen, BLACK, screen_rect, gun, gun_rect, gun_x, bullit, bul_x, bul_y, window)


#-----------------------------------------------------------------------------


def allRender(scr, bg, scr_rect, gun, gun_rect, gun_x, bullit, bul_x, bul_y, win):
	"""  All objects rendering  """
	scr.fill(bg)
	gunRender(scr, scr_rect, gun, gun_rect, gun_x)
	if bullit:
		bullitMove(scr, bullit, bul_x, bul_y)
	win.flip()


#------------------------------ GUN ------------------------------------------


def gunMove(key, isDown):
	"""  Gun handling keypress events  """
	if isDown:
		if key == pygame.K_RIGHT:
			gun_move_left = False
			gun_move_right = True
		elif key == pygame.K_LEFT:
			gun_move_right = False
			gun_move_left = True
	else:
		gun_move_left = False
		gun_move_right = False
	return gun_move_left, gun_move_right


def getGunStep(gun_move_right, gun_move_left, GUN_WIDTH, WIN_WIDTH, gun_x, GUN_STEP):
	"""  Gun moving  """
	if gun_move_right and GUN_WIDTH // 2 + gun_x < WIN_WIDTH // 2:
		gun_x += GUN_STEP
	if gun_move_left and WIN_WIDTH // 2 + gun_x > GUN_WIDTH // 2:
		gun_x -= GUN_STEP
	return gun_x


def gunRender(screen, screen_rect, gun, gun_rect, x):
	"""  Gun rendering  """
	gun_rect.centerx = screen_rect.centerx + x
	screen.blit(gun, gun_rect)


#---------------------------------- BULLIT -----------------------------------


def bullitCreate(color, gun_rect):
	"""  Bullit creating  """
	surf = pygame.Surface((6, 18))
	surf.fill(color)
	x = gun_rect.centerx - 3
	y = gun_rect.top - 9
	return surf, x, y


def bullitMove(screen, bullit, bul_x, bul_y):
	"""  Bullit moving  """
	screen.blit(bullit, (bul_x, bul_y))

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------


run()

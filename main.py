import sys
import pygame
from random import randint as rnd


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

	game = True
	winner = False

	#------------------------------
	score = 0
	font_score = pygame.font.Font(None, 24)

	health = 3

	#------------------------------
	GUN_WIDTH = 50
	GUN_STEP = 3
	gun = pygame.image.load('./img/gun.jpg')
	gun_rect = gun.get_rect()
	gun_rect.bottom = screen_rect.bottom - 20
	gun_x = 0
	gun_move_right = False
	gun_move_left = False

	sound1 = pygame.mixer.Sound('./sound/boom.ogg')

	#------------------------------
	BULLIT_STEP = 1
	bullits = []

	#------------------------------
	OPPONENT_STEP = 0.5
	opponent_amount = 1
	opponents = [opponentCreate(screen_rect, WIN_WIDTH, WIN_HEIGHT)]

	#------------------------------
	while game:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					sound1.play()
					bullits.append(bullitCreate(RED, gun_rect))
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					gun_move_left, gun_move_right = gunMove(event.key, True)
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					gun_move_left, gun_move_right = gunMove(event.key, False)

		gun_x = getGunStep(gun_move_right, gun_move_left, GUN_WIDTH, WIN_WIDTH, gun_x, GUN_STEP)

		for bullit in bullits:
			for opponent in opponents:
				if isHit(bullit, opponent):
					opponents.remove(opponent)
					score += 1
					if score < 150:
						if score == 10 or score == 30 or score == 60 or score == 100:
							opponent_amount, opponents = getOpponents(opponent_amount, opponents, score)
							for i in range(opponent_amount):
								opponents.append(opponentCreate(screen_rect, WIN_WIDTH, WIN_HEIGHT))
						else:
							opponents.append(opponentCreate(screen_rect, WIN_WIDTH, WIN_HEIGHT))
					else:
						game = False
						winner = True

			if bullit['y'] > 0:
				bullit['y'] -= BULLIT_STEP
			else:
				bullits.remove(bullit)

		for opponent in opponents:
			if isCollision(opponent, gun_rect):
				opponents.remove(opponent)
				health -= 1
				if health < 1:
					game = False
				else:
					healthRender(screen, health)
					score = 0
					opponent_amount = 1
					opponents = [opponentCreate(screen_rect, WIN_WIDTH, WIN_HEIGHT)]
			else:
				opponent = opponentMove(opponent, OPPONENT_STEP, WIN_WIDTH, WIN_HEIGHT)

		text_score = font_score.render('SCORE: ' + str(score), True, (255, 255, 255))

		allRender(screen, BLACK, screen_rect, gun, gun_rect, gun_x, bullits, opponents, text_score, health, window)


	while True:
		if winner:
			gameWin(screen, BLACK, screen_rect, window)
		else:
			gameOver(screen, BLACK, screen_rect, window)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()


#-----------------------------------------------------------------------------


def allRender(scr, bg, scr_rect, gun, gun_rect, gun_x, bullits, opponents, text_score, health, win):
	"""  All objects rendering  """
	scr.fill(bg)
	scr.blit(text_score, (scr_rect.width - 120, scr_rect.y + 30))
	healthRender(scr, health)
	gunRender(scr, scr_rect, gun, gun_rect, gun_x)
	if bullits:
		for bullit in bullits:
			bullitRender(scr, bullit)
	if opponents:
		for opponent in opponents:
			opponentRender(scr, opponent)
	win.flip()


#--------------------------------- END GAME ----------------------------------


def gameWin(scr, bg, scr_rect, win):
	scr.fill(bg)
	text = pygame.font.Font(None, 72).render('YOU WIN', True, (0, 255, 0))
	text_rect = text.get_rect()
	text_rect.centerx = scr_rect.centerx
	text_rect.centery = scr_rect.centery
	scr.blit(text, text_rect)
	win.flip()


def gameOver(scr, bg, scr_rect, win):
	scr.fill(bg)
	text = pygame.font.Font(None, 72).render('GAME OVER', True, (180, 0, 0))
	text_rect = text.get_rect()
	text_rect.centerx = scr_rect.centerx
	text_rect.centery = scr_rect.centery
	scr.blit(text, text_rect)
	win.flip()


#------------------------------ HEALTH ---------------------------------------


def healthRender(screen, n):
	"""  Create array of health  """
	for i in range(n):
		health = pygame.image.load('./img/health.jpg')
		screen.blit(health, (30 + 30 * i, 30))


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
	y = gun_rect.y - 18
	return {'obj': surf, 'x': x, 'y': y}


def bullitRender(screen, bullit):
	"""  Bullit moving  """
	screen.blit(bullit['obj'], (bullit['x'], bullit['y']))


def isHit(bullit, opponent):
	"""  return True if bullit -> opponent  """
	bul_x = bullit['x']
	bul_y = bullit['y']

	opp_x = opponent['x']
	opp_y = opponent['y']

	if opp_x - 6 <= bul_x <= opp_x + 30 and opp_y - 18 <= bul_y <= opp_y + 30:
		return True
	else:
		return False


#-------------------------------- OPPONENT -----------------------------------


def getOpponents(opponent_amount, opponents, score):
	"""  Calculate amount of opponents for creating new opponents  """
	if score == 10:
		opponent_amount = 2
		opponents = []
	elif score == 30:
		opponent_amount = 3
		opponents = []
	elif score == 60:
		opponent_amount = 4
		opponents = []
	elif score == 100:
		opponent_amount = 5
		opponents = []

	return opponent_amount, opponents


def opponentCreate(screen_rect, win_width, win_height):
	"""  Opponent creating  """
	surf = pygame.Surface((30, 30))
	pygame.draw.circle(surf, (rnd(0,255), rnd(0,255), rnd(0,255)), (15, 15), 15)
	x = screen_rect.centerx + rnd(-win_width//2, win_width//2 - 15)
	y = screen_rect.top + rnd(0, win_height//2)
	vx = ['right', 'left'][rnd(0, 1)]
	vy = ['top', 'bottom'][rnd(0, 1)]
	return {'obj': surf, 'x': x, 'y': y, 'vector_x': vx, 'vector_y': vy}


def opponentMove(opponent, step, win_width, win_height):
	"""  Opponent moving  """
	if opponent['vector_x'] == 'right':
		if opponent['x'] + 30 < win_width:
			opponent['x'] += step
		else:
			opponent['vector_x'] = 'left'
	else:
		if opponent['x'] > 0:
			opponent['x'] -= step
		else:
			opponent['vector_x'] = 'right'

	if opponent['vector_y'] == 'bottom':
		if opponent['y'] + 30 < win_height:
			opponent['y'] += step
		else:
			opponent['vector_y'] = 'top'
	else:
		if opponent['y'] > 0:
			opponent['y'] -= step
		else:
			opponent['vector_y'] = 'bottom'

	return opponent


def opponentRender(screen, opponent):
	"""  Opponent moving  """
	screen.blit(opponent['obj'], (opponent['x'], opponent['y']))


def isCollision(opponent, gun_rect):
	"""  return True if opponent -> gun  """
	opp_x = opponent['x']
	opp_y = opponent['y']

	gun_x = gun_rect.x
	gun_y = gun_rect.y + 25

	if gun_x - 30 < opp_x < gun_x + 50 and gun_y - 30 < opp_y < gun_y + 25:
		return True
	else:
		return False

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------


run()

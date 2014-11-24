import sys, pygame, time

pygame.init()

size = width, height = 500, 300 
speed = [1, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("mariostand.png")
ballrect = ball.get_rect()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	ballrect = ballrect.move(speed)

	screen.fill(black)
	screen.blit(ball, ballrect)
	pygame.display.flip()

	time.sleep (1.0/60)

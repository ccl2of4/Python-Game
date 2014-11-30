import pygame,sys

image = pygame.image.load (sys.argv[1])
image = pygame.transform.scale (image, (int (sys.argv[2]), int (sys.argv[3])) )
pygame.image.save (image, sys.argv[4])
#!/usr/bin/python

from sys import argv
import zbar
import Image
import cv
import pygame
from pygame.locals import *
from pygame.color import *

def draw_borders(screen, color):
	b1 = pygame.Surface((100, 20))
	b1.set_alpha(100)
	b1.fill(THECOLORS[color])

	b2 = pygame.Surface((20, 80))
	b2.set_alpha(100)
	b2.fill(THECOLORS[color])

	b3 = pygame.Surface((100, 20))
	b3.set_alpha(100)
	b3.fill(THECOLORS[color])

	b4 = pygame.Surface((20, 80))
	b4.set_alpha(100)
	b4.fill(THECOLORS[color])

	b5 = pygame.Surface((100, 20))
	b5.set_alpha(100)
	b5.fill(THECOLORS[color])

	b6 = pygame.Surface((20, 80))
	b6.set_alpha(100)
	b6.fill(THECOLORS[color])

	b7 = pygame.Surface((100, 20))
	b7.set_alpha(100)
	b7.fill(THECOLORS[color])

	b8 = pygame.Surface((20, 80))
	b8.set_alpha(100)
	b8.fill(THECOLORS[color])

	screen.blit(b1, (20, 20))
	screen.blit(b2, (20, 40))
	screen.blit(b3, (520, 20))
	screen.blit(b4, (600, 40))
	screen.blit(b5, (20, 440))
	screen.blit(b6, (20, 360))
	screen.blit(b7, (520, 440))
	screen.blit(b8, (600, 360))
# draw_borders

# pygame
pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('PyReader - @ricardokrieg')
screen = pygame.display.get_surface()
clock = pygame.time.Clock()
running = True

# pyzbar
scanner = zbar.ImageScanner()
scanner.parse_config('enable')
decoded = False
code = ''

# opencv
capture = cv.CreateCameraCapture(0)

while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
	# for

	frame = cv.QueryFrame(capture)
	if frame is not None:
		frame_to_pg = cv.CreateImage((640, 480), cv.IPL_DEPTH_8U, 3)
		cv.CvtColor(frame, frame_to_pg, cv.CV_RGB2BGR)
		to_pg = Image.fromstring("RGB", cv.GetSize(frame_to_pg), frame_to_pg.tostring())

		pg_img = pygame.image.frombuffer(to_pg.tostring(), to_pg.size, to_pg.mode)
		screen.blit(pg_img, (0, 0))

		if decoded:
			draw_borders(screen, 'green')

			code_surface = pygame.font.SysFont(None, 48).render(code, True, THECOLORS['white'], THECOLORS['blue'])
			screen.blit(code_surface, (0, 0))
		else:
			draw_borders(screen, 'red')

			pil = Image.fromstring("RGB", cv.GetSize(frame), frame.tostring()).convert('L')
			width, height = pil.size
			raw = pil.tostring()

			image = zbar.Image(width, height, 'Y800', raw)
			scanner.scan(image)

			for symbol in image:
			    print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
			    code = symbol.data
			    decoded = True
		# if
	# if

	pygame.display.flip()
	clock.tick(60)
# while
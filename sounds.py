import pygame

class Sounds():
	"""A class to manage game sounds."""

	def __init__(self):
		"""Load sounds"""
		pygame.mixer.init()
		# Background sound.
		pygame.mixer.music.load('sounds/background.mp3')
		pygame.mixer.music.play(-1)
		#Play sound when player loses one ship.
		
		self.sound1 = pygame.mixer.Sound('sounds/Explosion.mp3')
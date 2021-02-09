import pygame
import pygame.font


class Inscription():
	"""Draw inscription "YouLost."""

	def __init__(self, ai_game):
		"""Initialize the insription."""
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		
		self.text_color = (255, 82, 62)
		self.font = pygame.font.SysFont(None, 150)

		self.prep_You_Lost()

	def prep_You_Lost(self):
		"""Turn the inscription into render image."""
		self.image = self.font.render("You Lost", True, self.text_color)
		self.image_rect = self.image.get_rect()

		# Set position.
		self.image_rect.center = self.screen_rect.center
		self.image_rect.y = self.ai_game.play_button.rect.y // 2

	def draw_inscriptions(self):
		'''draw inscriptions'''
		self.screen.blit(self.image, self.image_rect)
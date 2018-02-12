import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class which represents a single army's alien."""

	def __init__(self, ai_settings, screen):
		"""Begins the alien and defines its initial postition."""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# Loads the alien's image and defines its rect attribute
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		# Begins each new alien close to the top on the left side
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		# Stores the correct alien's position
		self.x = float(self.rect.x)
		
	def blitme(self):
		"""Draws the alien on its current position."""
		self.screen.blit(self.image, self.rect)
		
	def check_edges(self):
		"""Returns True is the alien is in the scree's edge."""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
			
	def update(self):
		"""Moves the alien to the right or left."""
		self.x += (self.ai_settings.alien_speed_factor * 
									self.ai_settings.fleet_direction)
		self.rect.x = self.x

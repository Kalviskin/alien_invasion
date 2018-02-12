import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self, ai_settings, screen):
		"""Starts the spaceship and defines its initial position."""
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# Loads the spaceship image and gets its rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		# Starts each new spaceship on the central bottom of the screen	
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		# Stores a decimal value for the center of the spaceship
		self.center = float(self.rect.centerx)
				
		# Moving flags
		self.moving_right = False
		self.moving_left = False
		
	def update(self):
		"""
		Updates the spaceship position according to the moving flags.
		"""
		# Updates the Spaceship's center value, not the rectangle
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
			
		# Updates the rect object according to self.center
		self.rect.centerx = self.center			
		
	def blitme(self):
		"""Draws the spaceship on its current position."""
		self.screen.blit(self.image, self.rect)
	
	def center_ship(self):
		"""Centres the spaceship on the screen."""
		self.center = self.screen_rect.centerx

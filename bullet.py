import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class that manages the bullets shot by the spaceship."""
	
	def __init__(self, ai_settings, screen, ship):
		"""
		Creates an object of the bullet on the the spaceship current 
		position.
		"""
		super(Bullet, self).__init__()
		self.screen = screen
		
		# Creates a rectangle for the project in (0,0) then defines the
		# correct position
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
			ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		# Stores the bullet current position with a decimal value
		self.y = float(self.rect.y)
		
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor
		
	def update(self):
		"""Moves the the bullet up on the screen."""
		# Updates the bullet decimals position
		self.y -= self.speed_factor
		# Updates the rect's position
		self.rect.y = self.y
		
	def draw_bullet(self):
		"""Draws the bullet on the screen."""
		pygame.draw.rect(self.screen, self.color, self.rect)

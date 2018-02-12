class Settings():
	"""A class to store all the settings of Alien Invasion"""
	
	def __init__(self):
		"""It starts the game's settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		# Spaceship settings
		self.ship_speed_factor = 1.5
		self.ship_limit = 3
		
		# Bullets settings
		self.bullet_speed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 3
		
		# Aliens sttings
		self.fleet_drop_speed = 10
		
		# Rate in which the game's speed raises
		self.speedup_scale = 1.1
		# Rate in which the score for each alien increases
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		"""Starts the settings which change during the game."""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		
		# fleet_direction equals to 1 represents right; -1 represents
		# left
		self.fleet_direction = 1 
		
		# Score
		self.alien_points = 50
		
	def increase_speed(self):
		"""Raises speed settings."""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)

import json

class GameStats():
	"""Stores statistic data from Alien Invasion."""
	
	def __init__(self, ai_settings):
		"""Starts the statstic data."""
		self.ai_settings = ai_settings
		self.reset_stats()
		
		# Starts Alien Invasion in a True state
		self.game_active = False
		
		# High score should never be reseted
		h_score = 'high_score.json'
		try:
			with open(h_score) as f_obj:
				self.high_score = json.load(f_obj)
		except json.decoder.JSONDecodeError:
			with open(h_score, 'w') as f_obj:
				f_obj.write('0')			
				
	def reset_stats(self):
		"""
		Starts the statistic dara which can change during the game.
		"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
		

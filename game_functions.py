import sys
from time import sleep
import json

import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, stats, 
														ship, bullets):
	"""Responds to keys pushings."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		rec_high_score(stats)
		sys.exit()
			
def fire_bullet(ai_settings, screen, ship, bullets):
	"""Shots a bullet if it does not cross the limit."""
	# Creates a new bullet and add it to the bullet's group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
					
def check_keyup_events(event, ship):
	"""responds to keys releases."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, 
													 aliens, bullets):
	"""Responds to mouse and keyboard pressings."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			rec_high_score(stats)
			sys.exit()
			
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, stats, 
														 ship, bullets)	
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
			
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb,
				  play_button, ship, aliens, bullets, mouse_x, mouse_y)
			
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
									 aliens, bullets, mouse_x, mouse_y):
	"""Starts a new game when the player clicks Play."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# Restarts the game's settings
		ai_settings.initialize_dynamic_settings()
		
		# Hides mouse's cursor
		pygame.mouse.set_visible(False)
		
		# Restarts the statistic data of the game
		stats.reset_stats()
		stats.game_active = True
		
		# Restarts scoreboard's images
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		# Emptys the aliens and bullets list
		aliens.empty()
		bullets.empty()
		
		# Creates a new fleet and centres the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
														   play_button):
	"""Updates the screen images and alternes to the new screen."""
	# Redraws the screen on each passage through the loop
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	
	# Redraws all the bullets in the back of spaceship and the aliens
	for bullets in bullets.sprites():
		bullets.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	
	# Drawns score information
	sb.show_score()
	
	# Drawns Play button if the games is inative
	if not stats.game_active:
		play_button.draw_button()
	
	# Let the most recente screen visible
	pygame.display.flip()
	
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Updates the bullet's position and get rid the old bullets."""
	# Updates the bullet's position
	bullets.update()
	
	# Gets rid of all the bullets that disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
													aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
													  aliens, bullets):
	"""Responds to collisions between bullets and aliens."""
	# Removes any bullet and alien which had collised
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	
	if len(aliens) == 0:
		# Destroys existent bullets, increases game speed and creates a 
		# new fleet
		bullets.empty()
		ai_settings.increase_speed()
		
		# Increases level
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings, screen, ship, aliens)
				
def get_number_aliens_x(ai_settings, alien_width):
	"""Determines the number of aliens that fits in one line."""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""
	Determines the number of lines with aliens that fit in the screen.
	"""
	available_space_y = (ai_settings.screen_height - 
									  (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows								  
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	# Creates an alien and places it on the line
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
def create_fleet(ai_settings, screen, ship, aliens):
	"""Creates a comṕlete alien army."""
	# Creates an alien and calcules the number of aliens in one line
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, 
		alien.rect.height)
	
	# Creates an alien fleet
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,
				row_number)
		
def update_aliens(aliens):
	"""Updates the position of all the fleet aliens."""
	aliens.update()
	
def check_fleet_edges(ai_settings, aliens):
	"""Responds properly if any alien reached to edge."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Makes all the fleet go down and changes its direction."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""
	Responds to the fact of the spaceship have been shotted by an alien.
	"""
	if stats.ships_left > 0:
		# Uncrease ships_left
		stats.ships_left -= 1
		
		# Updates scoreboard
		sb.prep_ships()
	
		# Emptys the aliens and bullets list
		aliens.empty()
		bullets.empty()
		
		# Creates a new fleet and centralizes the spaceship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		# Takes a break
		sleep(0.5)	
	
	else: 
		stats.game_active = False
		rec_high_score(stats)
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, 
															   bullets):
	"""Verifies if any alien reached to the screen's bottom."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treats this case in the same way which is made when 
			# spaceship is hitted
			ship_hit(ai_settings, screen, stats, sb, ship, 
														aliens, bullets)
			break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, 
															 bullets):
	"""
	Verifies if the fleet is in one of the edges then updates the 
	position of all the aliens in the fleet.
	"""
	
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	# Verifies if there was colision between aliens and the ship
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
		
	# Verifies if there is any alien which hit the screen's bottom
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, 
																bullets)
	
def check_high_score(stats, sb):
	"""Verifies if there is a new high score."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		
def rec_high_score(stats):
	high_score = 'high_score.json'
	with open(high_score, 'w') as f_obj:
		json.dump(stats.high_score, f_obj) 

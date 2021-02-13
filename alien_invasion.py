import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sounds import Sounds
from inscription import Inscription

class AlienInvasion():
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        '''Initialize the game, and create game resources.'''
        pygame.init()

        self.sounds = Sounds()

        self.settings = Settings(self)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
            self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        # Create the instance to store game statistics.
        self.stats = GameStats(self)
        # Create the scoreboard
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, 'Play')

        self.you_lost = Inscription(self)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()


    def _check_events(self):
        '''Watch for keyboard and mouse events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()
            

    def _start_game(self):
        # Reset the game statistics.
        self.stats.reset_stats()
        # Reset dinamic settings.
        self.settings.initialize_dynamic_settings()
        # Reset score.
        self.sb.prep_score()
        # Reset level.
        self.sb.prep_level()
        # Reset lives.
        self.sb.prep_ships()
        
        # Get rid of any remeining bullets and aliens.
        self.aliens.empty()
        self.bullets.empty()

        self.stats.game_active = True

        # Create a new fleet and set ship position on center.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to Keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()
        elif event.key == pygame.K_LSHIFT:
            self.ship.acceleration_flag = True

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_LSHIFT:
            self.ship.acceleration_flag = False

    def _fire_bullet(self):
        """Create a new bullet and add it in to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bulet = Bullet(self)
            self.bullets.add(new_bulet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bulles."""
        # Update pullet position.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_colision()

    def _check_bullet_alien_colision(self):
        """Respond to bullet-alien collision."""
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # If all aliens is dead.
        # Destroy existing bullets and create new fleet.
        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()
            self._create_fleet()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create the fleet of alien"""
        # Create an alien and find the number of aliens in a row.
        # Space In between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size #size of alien
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width) # exactly amount of alien in row

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height) # exactly amount of rows

        # Create the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size #size of alien
        alien.x = alien_width + 2 * alien_width * alien_number # Alien's position in row
        alien.rect.x = alien.x
        alien.rect.y = alien_height + (alien_height * 2) * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet
        """
        self._check_fleet_edges() # Check the edge
        self.aliens.update() # Update position

        # Look for alien-ship collision.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Looks for alien-bottom collision.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond if any alien have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by any alien."""
        # Explosion sound
        self.sounds.sound1.play()

        if self.stats.ships_left > 0:
            # Decrease ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and set ship position on center.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            # Write new high score in file
            self.stats.update_high_score()
            
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any alien reached the bottom on the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same if the ship got hit.
                self._ship_hit()
                break

    def _update_screen(self):
        '''Update images on the screen, and flip to the new screen'''
        #Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        # Draws ships
        self.ship.blitme()

        # Draws bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draws all aliens in aliens group.
        self.aliens.draw(self.screen)

        # Draw the score
        self.sb.show_score()

        # Draw the play button if game inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
            if self.stats.ships_left == 0:
                # Draw inscription "You Lost"
                self.you_lost.draw_inscriptions()

        #Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
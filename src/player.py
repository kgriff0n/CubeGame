import colorsys
import math
import time

import pygame

from bullet import Bullet

pygame.font.init()
POPPINS = pygame.font.Font("font/Poppins.ttf", 18)
DEJAVU = pygame.font.Font("font/DejaVuSans.ttf", 14)


def adjust_saturation(rgb_color, saturation_shift):
    r, g, b = rgb_color[0] / 255.0, rgb_color[1] / 255.0, rgb_color[2] / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = (s + saturation_shift) % 1.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)


class Player:
    def __init__(self, x, y, width, height, color):
        self.username = "Waiting..."
        self.health = 3
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (self.x, self.y, self.width, self.height)
        self.vel = 3

        self.bullets = []
        self.last_bullet_time = time.time()

        self.invincibility = 60  # 1s invincibility on spawn
        self.shield = False
        self.shield_time = 0
        self.shield_cooldown = 0

        self.kill_count = 0

    def draw(self, win, main_player=False):
        # Draw player
        if self.invincibility > 0:
            # Animation when shoot
            color = adjust_saturation(self.color, 0.5)
            pygame.draw.rect(win, color, self.rect)
        else:
            pygame.draw.rect(win, self.color, self.rect)
        # Draw shield
        if self.shield:
            pygame.draw.circle(win, adjust_saturation(self.color, 0.5),
                               (self.x + self.width / 2, self.y + self.height / 2), 65, 5)
        # Draw pseudo
        img = POPPINS.render(self.username, True, self.color)
        win.blit(img, (self.x - ((img.get_width() - self.width) / 2), self.y - self.height / 2))
        # Draw health
        health_bar = ""
        for i in range(3):
            if i < self.health:
                health_bar += "♥"
            else:
                health_bar += "♡"
        img = DEJAVU.render(health_bar, True, self.color)
        win.blit(img, (self.x - ((img.get_width() - self.width) / 2), self.y - self.height / 1.5))
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(win)

        if main_player:
            # Draw bullets count
            bullets_remaining = 10 - len(self.bullets)
            img = POPPINS.render(f"Bullets: {bullets_remaining}", True, (0, 0, 0))
            win.blit(img, (10, pygame.display.get_surface().get_height() - img.get_height() * 2))
            # Draw shield state
            if self.shield_cooldown == 0:
                shield_state = "Ready"
            else:
                shield_state = self.shield_cooldown // 60
            img = POPPINS.render(f"Shield: {shield_state}", True, (0, 0, 0))
            win.blit(img, (10, pygame.display.get_surface().get_height() - img.get_height()))

    def tick(self):
        self.update_bullets()
        self.update_shield()
        self.decrease_invincibility()

    def update_bullets(self):
        # Remove bullet
        self.bullets = [bullet for bullet in self.bullets if not bullet.should_remove()]
        # Update pos
        for bullet in self.bullets:
            bullet.move()

    def decrease_invincibility(self):
        if self.invincibility > 0:
            self.invincibility -= 1

    def update_shield(self):
        if self.shield_time > 0:
            self.shield_time -= 1
        else:
            self.shield = False

        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1

    def check_collision(self, list_players):
        # Check bullets collisions
        for bullet in self.bullets:
            if bullet.hit_something(list_players):
                self.kill_count += 1
        # Check self collisions
        for player_index in list_players:
            other_player: Player = list_players[player_index]
            for bullet in other_player.bullets:
                if self.invincibility == 0 and bullet.collide(self):
                    # exit(0)
                    self.health -= 1
                    self.invincibility += 60
                    # if self.health == 0:
                    # exit(0)

    def input(self):
        old_pos = (self.x, self.y)

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_z]:
            self.y -= self.vel
        if keys_pressed[pygame.K_s]:
            self.y += self.vel
        if keys_pressed[pygame.K_q]:
            self.x -= self.vel
        if keys_pressed[pygame.K_d]:
            self.x += self.vel
        if keys_pressed[pygame.K_SPACE]:
            if self.last_bullet_time + 0.3 < time.time() and len(self.bullets) < 10:
                dx = pygame.mouse.get_pos()[0] - (self.x + 25)
                dy = pygame.mouse.get_pos()[1] - (self.y + 25)
                distance = math.sqrt(dx ** 2 + dy ** 2)
                vx = dx / distance
                vy = dy / distance
                self.bullets.append(Bullet(self.x + 25, self.y + 25, self.color, vx, vy))
                # Cooldown
                self.last_bullet_time = time.time()
        if keys_pressed[pygame.K_a]:
            if self.shield_cooldown == 0:
                self.shield = True
                self.shield_cooldown = 1800
                self.shield_time = 180
                self.invincibility = 180

        # Windows collision
        if self.x < 0 or self.y < 0 \
                or self.x > (pygame.display.get_surface().get_width() - self.width) \
                or self.y > (pygame.display.get_surface().get_height() - self.height):
            self.x, self.y = old_pos
        self.update_char_rect()

    def update_char_rect(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Player):
            return self.color == o.color
        return False

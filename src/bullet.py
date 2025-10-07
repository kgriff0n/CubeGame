import pygame


class Bullet:
    def __init__(self, x, y, color, vx, vy):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = color
        self.vel = 8
        self.vx = vx
        self.vy = vy
        self.time = 0

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vel * self.vx
        self.y += self.vel * self.vy
        self.time += 1

    def collide(self, player):
        if player.x < self.x < player.x + player.width and player.y < self.y < player.y + player.height:
            return True
        return

    def hit_something(self, list_players):
        """
        Checks if the bullet hit something (players for now)
        Returns true only if the player is killed by the bullet
        Otherwise, returns false
        """
        for player_index in list_players:
            other_player = list_players[player_index]
            if self.collide(other_player):
                self.time = 300
                if other_player.health == 1 and other_player.invincibility < 5:
                    return True

        return False

    def should_remove(self):
        return self.time >= 300

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Bullet):
            return self.color == o.color
        return False

import pygame
import socket
import pickle

from player import Player # for PyInstaller

WIDTH = 700
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.DOUBLEBUF)
pygame.display.set_caption("Game")

pygame.font.init()
POPPINS = pygame.font.Font("font/Poppins.ttf", 16)


class Window:
    def __init__(self, window_display):
        self._window = window_display

    @property
    def window(self):
        return self._window

    def draw_window(self, player, list_players):
        self.window.fill((255, 255, 255))  # Fill the screen with white
        player.draw(self.window, True)
        for player_index in list_players:
            player_to_draw = list_players[player_index]
            player_to_draw.draw(self.window)
        self.draw_ranking(player, list_players)
        pygame.display.update()

    def draw_ranking(self, main_player, list_players):
        players_copy = dict(list_players)
        players_copy["self"] = main_player
        # Draw ranking
        ranking = sorted(players_copy.values(), key=lambda player: player.kill_count, reverse=True)

        width = pygame.display.get_surface().get_width()
        height = 10

        img = POPPINS.render("Ranking", True, (0, 0, 0))
        self.window.blit(img, (width - img.get_width() - 10, height))
        height += img.get_height()

        for player in ranking:
            img = POPPINS.render(f"{player.username}: {player.kill_count}", True, player.color)
            self.window.blit(img, (width - img.get_width() - 10, height))
            height += img.get_height()

class Network:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player = self.connect()

    def connect(self):
        try:
            self.socket_client.connect((self.server_ip, self.server_port))
            return pickle.loads(self.socket_client.recv(2048))
        except Exception as e:
            print("[ERROR] Error trying to connect to server", e)

    def disconnect(self):
        self.socket_client.close()

    def send(self, data):
        try:
            self.socket_client.send(pickle.dumps(data))
            return pickle.loads(self.socket_client.recv(2048))
        except Exception as e:
            print("[ERROR] Error trying to send data to server.", e)

def main():
    config = {}
    with open('client.conf', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

    win = Window(window)
    n = Network(config["ip"], int(config["port"]))
    clock = pygame.time.Clock()
    player = n.player
    player.username = config["username"]
    while player.health > 0:
        clock.tick(60)
        list_players = n.send(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        player.input()
        player.tick()
        player.check_collision(list_players)
        win.draw_window(player, list_players)
    # Disconnect and restart when player die
    n.disconnect()
    main()


if __name__ == '__main__':
    main()

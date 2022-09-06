from random import randint
from the_quest import *
import pygame


class HullPoints:
    """
    Guarda los puntos de vida de la nave y los pinta
    """

    def __init__(self):
        self.initialize()
        pygame.font.init()
        self.typography = pygame.font.SysFont('urwbookman', 50)
        self.typography_endgame = pygame.font.SysFont('urwbookman', 100)

    def ckeck_gameover_condition(self):
        if self.points == MAX_HULL_HITPOINTS:
            print("Ship Destroyed!, GAME OVER")
            self.destroyed = True
        else:
            print(
                f"Collision! {MAX_HULL_HITPOINTS - self.points} hull points left!")

    def initialize(self):
        self.points = 0
        self.destroyed = False

    def draw(self, screen):
        text = pygame.font.Font.render(
            self.typography, str(self.points), True, C_WHITE)
        pos_x = (WIDTH - text.get_width())/4
        pos_y = LATERAL_MARGIN
        pygame.surface.Surface.blit(screen, text, (pos_x, pos_y))

        if self.destroyed == True:
            text = pygame.font.Font.render(
                self.typography_endgame, "Game Over", True, C_WHITE)
            pos_x = (WIDTH - text.get_width())/2
            pos_y = (HEIGHT - text.get_height())/2
            pygame.surface.Surface.blit(screen, text, (pos_x, pos_y))


class SpaceShip(pygame.Rect):

    UP = True
    DOWN = False

    hull_damage = HullPoints()

    def __init__(self, x, y):
        super(SpaceShip, self). __init__(x, y, SHIP_LENGTH, SHIP_WIDTH)
        self.speed = 5

    def move(self, direction):
        """
        Mueve la nave arriba o abajo según que tecla se pulse
        """

        if direction == self.UP:
            self.y = self.y - self.speed
            if self.y < 0:
                self.y = 0
        else:
            self.y = self.y + self.speed
            if self.y > HEIGHT - SHIP_WIDTH:
                self.y = HEIGHT - SHIP_WIDTH

    def hit_hull(self):
        self.hull_damage.points += 1


class Asteroid(pygame.Rect):
    def __init__(self):
        super(Asteroid, self).__init__(WIDTH-ASTEROID_SIZE, randint(HEIGHT -
                                                                    (HEIGHT-ASTEROID_SIZE), HEIGHT-ASTEROID_SIZE), ASTEROID_SIZE, ASTEROID_SIZE)

    def move(self):
        self.x = self.x - ASTEROID_SPEED

    # Resetea la posicion del asteroide al borde de la pantalla a altura aleatoria
    def reset(self):
        self.x = WIDTH
        self.y = randint(HEIGHT - (HEIGHT-ASTEROID_SIZE), HEIGHT-ASTEROID_SIZE)


class Scoreboard:
    """
    guarda la puntuacion y la pinta
    """

    def __init__(self):
        self.initialize()
        pygame.font.init()
        self.typography = pygame.font.SysFont('urwbookman', 50)
        self.typography_endgame = pygame.font.SysFont('urwbookman', 100)

    def check_win_condition(self):
        if self.points == WIN_SCORE:
            self.win = True
            print("WIN!")

    def add_score(self):
        """
        Marca punto
        """
        self.points += 1
        print(f"{self.points} Asteroids dodged!")

    def initialize(self):
        self.points = 0
        self.win = False

    def draw(self, screen):
        text = pygame.font.Font.render(
            self.typography, str(self.points), True, C_WHITE)
        pos_x = ((WIDTH - text.get_width())/4) + WIDTH/2
        pos_y = LATERAL_MARGIN
        pygame.surface.Surface.blit(screen, text, (pos_x, pos_y))

        if self.win == True:
            text = pygame.font.Font.render(
                self.typography_endgame, "You Win!", True, C_WHITE)
            pos_x = (WIDTH - text.get_width())/2
            pos_y = (HEIGHT - text.get_height())/2
            pygame.surface.Surface.blit(screen, text, (pos_x, pos_y))


class TheQuest:

    score = Scoreboard()

    def __init__(self):
        print("Building object EarthEscape")
        pygame.init()
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Preparacion para pintar texto

        self.space_ship = SpaceShip(
            LATERAL_MARGIN,                         # coord x (left)
            (HEIGHT-LATERAL_MARGIN)/2)              # coord y (top)

        self.asteroid = Asteroid()

    def collide(self):
        """
        Comprueba si el asteroide colisiona con la nave, resetea la posición del asteroide y resta un punto de vida
        """
        if pygame.Rect.colliderect(self.asteroid, self.space_ship):
            self.space_ship.hit_hull()
            self.space_ship.hull_damage.ckeck_gameover_condition()
            if not self.space_ship.hull_damage.destroyed:
                self.asteroid.reset()

    def main_loop(self):
        print("In main loop")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #    if event.key == pygame.K_ESCAPE:
                    #        print("Exiting")
                    #        return
                    if event.key == pygame.K_r:
                        self.score.initialize()
                        self.space_ship.hull_damage.initialize()

                if event.type == pygame.QUIT:
                    print("Exiting")
                    return

            key_status = pygame.key.get_pressed()
            if key_status[pygame.K_UP]:
                self.space_ship.move(SpaceShip.UP)
            if key_status[pygame.K_DOWN]:
                self.space_ship.move(SpaceShip.DOWN)

            if self.score.win == False and self.space_ship.hull_damage.destroyed == False:
                self.asteroid.move()
                self.collide()
            if self.asteroid.x <= 0:
                self.score.add_score()
                self.score.check_win_condition()
                self.asteroid.reset()

            self.screen.fill(C_BLACK)
            if not self.space_ship.hull_damage.destroyed:
                pygame.draw.rect(self.screen, C_WHITE, self.space_ship)
            pygame.draw.rect(self.screen, C_WHITE, self.asteroid)
            # dibuja los puntos para ganar (asteroides esquivados)
            self.score.draw(self.screen)
            # dibuja los puntos para perder (golpes a la nave)
            self.space_ship.hull_damage.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = TheQuest()

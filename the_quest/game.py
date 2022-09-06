from turtle import width
import pygame

from the_quest import HEIGHT, WIDTH


class TheQuest:
    def __init__(self):
        print("Starting game")
        pygame.init()
        pygame.display.set_mode((WIDTH, HEIGHT))


if __name__ == "__main__":
    TheQuest()

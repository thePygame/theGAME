import pygame


class Level:
    def __init__(self, game):
       self.level = 0

    def checkLevel(self, distance):
       if(distance > 100):
          self.leve = 1
       

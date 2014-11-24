import sys, pygame, time
import constants
from Game import Game
from Player import Player
from Entity import Entity


game = Game ()

player = Player ("images/mariostand.png")
platform = Entity ("images/platform.png",0,300,200,20)
platform.set_affected_by_gravity (False)

game.add_entity (player)
game.add_entity (platform)

game.run ()
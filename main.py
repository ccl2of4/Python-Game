import sys, pygame, time
import constants
from Game import Game
from Player import Player
from Entity import Entity


game = Game ()

player = Player ("images/mariostand.png")
player.set_delegate (game)

platform = Entity ("images/platform.png",0,300,200,20)
platform.set_affected_by_gravity (False)
platform.set_delegate (game)

game.add_entity (player)
game.add_entity (platform)

game.run ()
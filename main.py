import sys, pygame, time
from Game import Game
from Player import Player
from Entity import Entity
from Camera import Camera
from UserController import UserController
from AIController import AIController
from Gun import Gun
from Bomb import Bomb
from StatusDisplay import StatusDisplay
from LifeController import LifeController

game = Game (800, 400)
camera = Camera (800, 400)
game.set_camera (camera)

player = Player (50,0,46,80,
	default = 'images/mario_stand.png',
	stand='images/mario_stand.png',
	walk='images/mario_walk.png',
	run='images/mario_run.png',
	jump='images/mario_jump.png',)
player.set_delegate (game)
player_controller = UserController (player)

player_ai = Player (100,0,46,80,
	default = 'images/mario_stand.png',
	stand='images/mario_stand.png',
	walk='images/mario_walk.png',
	run='images/mario_run.png',
	jump='images/mario_jump.png',)
player_ai.set_delegate (game)
player_ai_controller = AIController (player_ai)
player_ai_controller.set_target_entity (player)

player_ai.set_life_controller (LifeController ())
player_ai_display = StatusDisplay (0,0,100,50)
player_ai_display.set_delegate (game)
player_ai.set_status_display (player_ai_display)
game.add_entity (player_ai_display)

gun = Gun (150,250,40,5,default='images/platform.png')
gun.set_delegate (game)

bomb = Bomb (200,0,10,10,default='images/platform.png')
bomb.set_delegate (game)

platform = Entity (0,300,2000,20,default='images/platform.png')
platform.set_gravity (0)
platform.set_delegate (game)

platform1 = Entity (600,150,500,20,default='images/platform.png')
platform1.set_gravity (0)
platform1.set_delegate (game)

platform2 = Entity (450,250,20,100,default='images/platform.png')
platform2.set_gravity (0)
platform2.set_delegate (game)

for i in range (0, 10) :
	p = Entity (700 + 40*i, 290 - 10*i, 50, 10, default='images/platform.png')
	p.set_gravity (0)
	p.set_delegate (game)
	game.add_entity (p)

player.set_life_controller (LifeController ())
player_display = StatusDisplay (0,0,100,50)
player_display.set_delegate (game)
player.set_status_display (player_display)
game.add_entity (player_display)

game.add_entity (player)
game.add_entity (player_ai)
game.add_entity (platform)
#game.add_entity (platform1)
game.add_entity (platform2)
game.add_entity (gun)
game.add_entity (bomb)

game.add_controller (player_controller)
#game.add_controller (player_ai_controller)

game.set_main_entity (player)

game.run ()
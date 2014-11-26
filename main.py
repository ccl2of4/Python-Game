import sys, pygame, time
from Game import Game
from Player import Player
from Entity import Entity
from Camera import Camera
from UserInputEntityController import UserInputEntityController
from AIEntityController import AIEntityController
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
player.set_name ("Main")
game.spawn_entity (player)
game.set_main_entity (player)

player_c = UserInputEntityController (player)
game.add_controller (player_c)
player.set_life_controller (LifeController ())
player.set_status_display (StatusDisplay (100,50))

for i in range (1000,3000,200) :
	player_ai = Player (i,0,46,80,
		default = 'images/mario_stand.png',
		stand='images/mario_stand.png',
		walk='images/mario_walk.png',
		run='images/mario_run.png',
		jump='images/mario_jump.png',)
	player_ai.set_name ("AI")
	player_ai_c = AIEntityController (player_ai)
	player_ai_c.set_target_entity (player)
	game.add_controller (player_ai_c)
	game.spawn_entity (player_ai)
	player_ai.set_life_controller (LifeController ())
	player_ai.set_status_display (StatusDisplay (100,50))

gun = Gun (150,250,40,5,default='images/platform.png')
game.spawn_entity (gun)

bomb = Bomb (200,0,10,10,default='images/platform.png')
game.spawn_entity (bomb)

platform = Entity (0,300,5000,20,default='images/platform.png')
platform.set_gravity (0)
game.spawn_entity (platform)

platform = Entity (450,250,20,100,default='images/platform.png')
platform.set_gravity (0)
game.spawn_entity (platform)

for i in range (0, 10) :
	p = Entity (700 + 40*i, 290 - 10*i, 50, 10, default='images/platform.png')
	p.set_gravity (0)
	game.spawn_entity (p)

game.run ()
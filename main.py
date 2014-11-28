import sys, pygame, time
from Game import Game
from Character import Character
from Entity import Entity
from Camera import Camera
from UserInputEntityController import UserInputEntityController
from AIEntityController import AIEntityController
from Gun import Gun
from Bomb import Bomb
from StatusDisplay import StatusDisplay
from LifeController import LifeController
from LevelReader import LevelReader
from Bullet import Bullet
from ExplosiveBullet import ExplosiveBullet

def load_level (file_path) :
	reader = LevelReader ()
	game = reader.read (file_path)
	game.run ()


def create_level () :
	game = Game ()
	camera = Camera ()
	game.set_camera (camera)

	player = Character (
		default = 'images/mario_stand.png',
		stand='images/mario_stand.png',
		walk='images/mario_walk.png',
		run='images/mario_run.png',
		jump='images/mario_jump.png',)
	player.set_name ("Main")
	game.spawn_entity (player)
	game.set_main_entity (player)
	player.set_life_controller (LifeController ())
	status_display = StatusDisplay (10,340)
	status_display.set_client (player)
	game.spawn_entity_absolute (status_display)
	player_c = UserInputEntityController (player)
	game.add_controller (player_c)
	
	for i in range (1000,3000,200) :
		player_ai = Character (i,0,
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
		player_ai.set_status_display (StatusDisplay (width=120,height=50))
	
	gun = Gun (150,250, default='images/platform.png')
	magazine = []
	for i in range (50) :
		magazine.append (Bullet (default='images/platform.png'))
	gun.set_magazine (magazine)

	game.spawn_entity (gun)

	bomb = Bomb (200,0, default='images/platform.png')
	game.spawn_entity (bomb)

	platform = Entity (0,300,5000,20,default='images/platform.png')
	platform.set_gravity (0)
	game.spawn_entity (platform)

	platform = Entity (450,250,20,100,default='images/platform.png')
	platform.set_gravity (0)
	game.spawn_entity (platform)

	'''
	for i in range (0, 1000) :
		p = Entity (300 -i, 200, 1, 10, default='images/platform.png')
		p.set_gravity (0)
		game.spawn_entity (p)
	'''
	'''
	for i in range (0, 50) :
		p = Entity (300, 200 - i, 50, 1, default='images/platform.png')
		p.set_gravity (0)
		game.spawn_entity (p)
	'''

	for i in range (0, 10) :
		p = Entity (700 + 40*i, 290 - 10*i, 50, 10, default='images/platform.png')
		p.set_gravity (0)
		game.spawn_entity (p)

	game.run ()


if (len (sys.argv) == 2) :
	load_level (sys.argv[1])
else :
	create_level ()
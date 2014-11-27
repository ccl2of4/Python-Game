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

def string_to_int (str) :
	return int (str)

class LevelReader :
	def __init__ (self) :
		self.current_platform = None

	def read (self, file_path) :
		file = open (file_path, 'r')
		
		game = Game (800,400)
		game.set_camera (Camera (800,400))


		current_entity = None
		
		for line in file :
			line = line.strip ()
			if line == 'main' :
				assert game.get_main_entity () == None
				assert current_entity == None

				player = Player (
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

				current_entity = player

			elif line == 'platform' :
				assert current_entity == None
				platform = Entity (default='images/platform.png')
				platform.set_gravity (0)
				game.spawn_entity (platform)

				current_entity = platform

			elif line == 'player' :
				assert game.get_main_entity () != None
				assert current_entity == None
				player_ai = Player (
					default = 'images/mario_stand.png',
					stand='images/mario_stand.png',
					walk='images/mario_walk.png',
					run='images/mario_run.png',
					jump='images/mario_jump.png',)
				player_ai.set_name ("AI")
				player_ai_c = AIEntityController (player_ai)
				player_ai_c.set_target_entity (game.get_main_entity ())
				game.add_controller (player_ai_c)
				game.spawn_entity (player_ai)
				player_ai.set_life_controller (LifeController ())
				player_ai.set_status_display (StatusDisplay (100,50))

				current_entity = player_ai

			else :
				coords = line.split ()
				assert (len (coords) == 4)
				coords = map (string_to_int, coords)
				x,y,width,height = coords
				current_entity.rect = pygame.Rect (*coords)
				current_entity.width, current_entity.height = width, height
				current_entity = None


		return game
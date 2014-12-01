import sys, pygame, time
from game import Game
from character import Character
from entity import Entity
from camera import Camera
from userinputentitycontroller import UserInputEntityController
from aientitycontroller import AIEntityController
from firearm import Firearm
from bomb import Bomb
from statusdisplay import StatusDisplay
from bullet import Bullet
from explosivebullet import ExplosiveBullet
from pointofinterest import PointOfInterest
from perishableentity import PerishableEntity
from shotgunshell import ShotgunShell
from moveableentity import MoveableEntity
from automaticfirearm import AutomaticFirearm
from entityspawner import EntitySpawner
from compositeentity import CompositeEntity
import json

##
#
#	GUN SPRITES
#
#	http://dustination.deviantart.com/gallery/33496765/Gun-Sprites
#
##
global function_mappings

def read (file_path) :
	game = None

	with open (file_path, 'r') as f :
		data = json.load (f)
		game = _create_game (data)

	return game

def _create_group (game, data) :
	entities = []
	count = data['count']
	entity = data['entity']
	category = entity['category']

	x_logic = None
	y_logic = None

	if 'x' in data :
		x_logic = data['x']
	if 'y' in data :
		y_logic = data['y']

	func = function_mappings[category]
	for i in range (count) :
		entity = func (game, entity)
		if x_logic != None :
			entity.rect.x = eval (x_logic)
		if y_logic != None :
			entity.rect.y = eval (y_logic)
		entities.append (entity)

	return entities

def _create_composite (game, data) :
	assert (False)
	composite_entity = CompositeEntity ()
	entities = []

	for entity in data['entities'] :
		category = entity['category']
		res = function_mappings[category] (game, entity)
		try :
			entities.extend (res)
		except :
			entities.append (res)

	try :
		composite_entity.rect.x, composite_entity.rect.y = data['x'], data['y']
	except :
		pass

	composite_entity.set_inner_entities (entities)
	return composite_entity

def _create_player (game, data) :
	assert game.get_main_entity () == None
	player = Character (
		default = 'images/player_stand.png',
		stand='images/player_stand.png',
		walk='images/player_walk.png',
		run='images/player_run.png',
		jump='images/player_jump.png',)
	player.set_anchor_points (hand=(37,152))
	player.set_name ("Main")
	player.set_controller (UserInputEntityController ())
	game.set_main_entity (player)

	status_display = StatusDisplay ()
	status_display.set_client (player)
	game.spawn_entity_absolute (status_display)

	try :
		player.rect.x, player.rect.y = data['x'], data['y']
	except :
		pass

	return player

def _create_platform (game, data) :
	platform = Entity (default='images/platform.png')

	try :
		platform.rect.x, platform.rect.y = data['x'], data['y']
	except :
		pass

	return platform

def _create_wood (game, data) :
	block = Entity (default='images/wood.png')

	try :
		block.rect.x, block.rect.y = data['x'], data['y']
	except :
		pass

	return block

def _create_ground (game, data) :
	block = Entity (default='images/ground.png')

	try :
		block.rect.x, block.rect.y = data['x'], data['y']
	except :
		pass

	return block

def _create_roof (game, data) :
	block = Entity (default='images/roof.png')

	try :
		block.rect.x, block.rect.y = data['x'], data['y']
	except :
		pass

	return block

def _create_30_cal (game, data) :
	p30_cal = Bullet (default='images/30_cal.png')
	return p30_cal

def _create_buckshot (game, data) :
	buckshot = ShotgunShell (default='images/bullet.png')
	return buckshot

def _create_870 (game, data) :
	r870 = Firearm (default='images/870.png')
	r870.set_anchor_points (muzzle=(147,4), grip=(54,14))
	magazine = []

	try :
		r870.rect.x, r870.rect.y = data['x'], data['y']
	except :
		pass

	for projectile in data['magazine'] :
		category = projectile['category']
		res = function_mappings[category] (game, projectile)
		try :
			magazine.extend (res)
		except :
			magazine.append (res)

	r870.set_magazine (magazine)

	return r870

def _create_m60 (game, data) :
	m60 = AutomaticFirearm (default='images/m60.png')
	m60.set_anchor_points (muzzle=(175,15), grip=(62,30))
	magazine = []

	try :
		m60.rect.x, m60.rect.y = data['x'], data['y']
	except :
		pass

	for projectile in data['magazine'] :
		category = projectile['category']
		res = function_mappings[category] (game, projectile)
		try :
			magazine.extend (res)
		except :
			magazine.append (res)

	m60.set_magazine (magazine)

	return m60

def _create_entity_spawner (game, data) :
	entity_spawner = EntitySpawner ()
	entities = []

	try :
		entity_spawner.rect.x, entity_spawner.rect.y = data['x'], data['y']
	except :
		pass
	
	for entity in data['contents'] :
		category = entity['category']
		res = function_mappings[category] (game, entity)
		try :
			entities.extend (res)
		except :
			entities.append (res)

	entity_spawner.set_entities (entities)
	
	return entity_spawner

def _create_zombie (game, data) :
	assert len (game.get_defend_points ()) > 0
	zombie = Character (
		default = 'images/zombie_stand.png',
		stand='images/zombie_stand.png',
		walk='images/zombie_walk.png',
		run='images/zombie_run.png',
		jump='images/zombie_jump.png',)
	zombie.set_anchor_points (hand=(37,152))
	zombie.set_name ("AI")
	zombie.set_hostile (True)
	zombie_c = AIEntityController ()
	zombie.set_controller (zombie_c)
	zombie_c.set_target_entity (game.get_defend_points ()[0])
	game.get_enemies().append (zombie)
	zombie.set_status_display (StatusDisplay ())

	try :
		zombie.rect.x, zombie.rect.y = data['x'], data['y']
	except :
		pass

	return zombie

def _create_defend_point (game, data) :
	defend_point = PointOfInterest ()
	game.get_defend_points().append (defend_point)
	
	try :
		defend_point.rect.x, defend_point.rect.y = data['x'], data['y']
	except :
		pass

	return defend_point

def _create_game (data) :
	game = Game (800, 450)
	game.set_camera (Camera (800,450))


	for entity in data :
		category = entity['category']

		game_entity = function_mappings[category](game, entity)
		try :
			for s_game_entity in game_entity :
				game.spawn_entity (s_game_entity)
		except :
			game.spawn_entity (game_entity)

	return game

function_mappings = {
	'group' : _create_group,
	'roof' : _create_roof,
	'player' : _create_player,
	'platform' : _create_platform,
	'composite' : _create_composite,
	'ground' : _create_ground,
	'wood' : _create_wood,
	'm60' : _create_m60,
	'870' : _create_870,
	'zombie' : _create_zombie,
	'defend point' : _create_defend_point,
	'entity spawner' : _create_entity_spawner,
	'.30 cal' : _create_30_cal,
	'buckshot' : _create_buckshot
}
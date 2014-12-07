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

global sprite_mappings
global function_mappings

def read (file_path) :
	game = None

	with open (file_path, 'r') as f :
		data = json.load (f)
		game = _create_game (data)

	return game

def _get_coords (data) :
	try :
		x, y = data['coords'][0], data['coords'][1]
	except :
		return (0,0)
	return x, y

def _unpack_sprites (data) :
	pass
def _unpack_anchors (data) :
	pass

def _create_group (game, data) :
	entities = []
	count = data['count']
	entity = data['entity']
	category = entity['category']

	x_logic = None
	y_logic = None

	if 'coords' in data :
		x_logic = data['coords'][0]
		y_logic = data['coords'][1]

	func = function_mappings[category]
	for i in range (count) :
		entity = func (game, entity)
		if x_logic != None and y_logic != None :
			pos = eval (x_logic), eval (y_logic)
			entity.set_pos (pos)
		entities.append (entity)

	return entities

def _create_player (game, data) :
	assert game.get_main_entity () == None

	player = Character (
		default = 'images/player_stand.png',
		stand='images/player_stand.png',
		walk='images/player_walk.png',
		run='images/player_run.png',
		jump='images/player_jump.png',)
	player.set_anchor_points (hand=(62,150))
	player.set_name ("Player")
	player.set_controller (UserInputEntityController ())
	player.set_jump_acceleration (-20.0)
	game.set_main_entity (player)

	status_display = StatusDisplay ()
	status_display.set_client (player)
	game.spawn_entity_absolute (status_display)

	player.rect.topleft = _get_coords (data)


	return player

def _create_platform (game, data) :
	platform = Entity (default='images/platform.png')
	platform.set_pos (_get_coords (data))

	return platform

def _create_wood (game, data) :
	wood = PerishableEntity (default='images/wood.png')

	wood.set_pos (_get_coords (data))

	return wood

def _create_ground (game, data) :
	ground = Entity (default='images/ground.png')
	ground.set_pos (_get_coords (data))

	return ground

def _create_roof (game, data) :
	roof = Entity (default='images/roof.png')
	roof.set_pos (_get_coords (data))

	return roof

def _create_30_cal (game, data) :
	p30_cal = Bullet (default='images/30_cal.png')
	p30_cal.set_pos (_get_coords (data))
	p30_cal.set_name (".30 cal")
	return p30_cal

def _create_buckshot (game, data) :
	buckshot = ShotgunShell ()
	buckshot.set_pos (_get_coords (data))
	buckshot.set_name ("buckshot")
	return buckshot

def _create_870 (game, data) :
	r870 = Firearm (default='images/870.png')
	r870.set_anchor_points (muzzle=(147,4), grip=(54,14))
	r870.set_name ("870")
	magazine = []

	r870.set_pos (_get_coords (data))

	for projectile in data['magazine'] :
		category = projectile['category']
		res = function_mappings[category] (game, projectile)
		try :
			magazine.extend (res)
		except :
			magazine.append (res)

	r870.set_magazine (magazine)

	return r870

def _create_m1911 (game, data) :
	m1911 = Firearm (default='images/m1911.png')
	m1911.set_anchor_points (muzzle=(29,4), grip=(15,9))
	m1911.set_name ("m1911")
	magazine = []

	m1911.set_pos (_get_coords (data))

	for projectile in data['magazine'] :
		category = projectile['category']
		res = function_mappings[category] (game, projectile)
		try :
			magazine.extend (res)
		except :
			magazine.append (res)

	m1911.set_magazine (magazine)

	return m1911

def _create_m60 (game, data) :
	m60 = AutomaticFirearm (default='images/m60.png')
	m60.set_anchor_points (muzzle=(175,15), grip=(62,30))
	m60.set_name ("m60")
	magazine = []

	m60.set_pos (_get_coords (data))

	for projectile in data['magazine'] :
		category = projectile['category']
		res = function_mappings[category] (game, projectile)
		try :
			magazine.extend (res)
		except :
			magazine.append (res)

	m60.set_magazine (magazine)

	return m60

def _create_m67 (game, data) :
	m67 = Bomb (default='images/m67.png')
	m67.set_anchor_points (grip=(7,7))
	m67.set_pos (_get_coords (data))
	m67.set_name ("m67")
	return m67

def _create_entity_spawner (game, data) :
	entity_spawner = EntitySpawner ()
	entities = []

	entity_spawner.set_pos (_get_coords (data))
	
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
	zombie.set_name ("Zombie")
	zombie.set_hostile (True)
	zombie_c = AIEntityController ()
	zombie.set_controller (zombie_c)
	zombie_c.set_target_entity (game.get_defend_points ()[0])
	game.get_enemies().append (zombie)
	zombie.set_status_display (StatusDisplay ())

	zombie.set_pos (_get_coords (data))

	return zombie

def _create_defend_point (game, data) :
	defend_point = PointOfInterest ()
	game.get_defend_points().append (defend_point)
	defend_point.set_pos (_get_coords (data))

	return defend_point

def _create_composite_entity (game, data) :
	composite_entity = CompositeEntity ()
	entities = []

	for entity in data['entities'] :
		category = entity['category']
		res = function_mappings[category] (game, entity)
		try :
			entities.extend (res)
		except :
			entities.append (res)

	composite_entity.set_entities (entities)
	
	return composite_entity

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


with open ('sprites.json', 'r') as f :
		sprite_mappings = json.load (f)

function_mappings = {
	'group' : _create_group,
	'roof' : _create_roof,
	'player' : _create_player,
	'platform' : _create_platform,
	'ground' : _create_ground,
	'wood' : _create_wood,
	'm60' : _create_m60,
	'870' : _create_870,
	'm1911' : _create_m1911,
	'm67' : _create_m67,
	'zombie' : _create_zombie,
	'defend point' : _create_defend_point,
	'entity spawner' : _create_entity_spawner,
	'.30 cal' : _create_30_cal,
	'buckshot' : _create_buckshot,
	'composite entity' : _create_composite_entity
}
import pygame

import resource

from perishableentity import PerishableEntity
from weapon import Weapon
from entity import *
from statusdisplay import *
from lifecontroller import *
from notificationcenter import NotificationCenter
import notificationcenter

global running_anim_duration
running_anim_duraction = 5

global walking_anim_duration
walking_anim_duration = 10


##############
#notifications
##############

global character_cannot_drop_weapon_notification
character_cannot_drop_weapon_notification = 'character cannot drop weapon notification'

global character_picked_up_weapon_notification
character_picked_up_weapon_notification = 'character picked up weapon notification'

class Character (PerishableEntity, StatusDisplayClient) :
	def __init__(self,x=0,y=0,width=46,height=80, **images) :

		#used for animation
		self.walking = False
		self.running = False
		self.jumping = False
		self.running_duration = 0
		self.walking_duration = 0

		#default physics coefficients
		self.jump_acceleration = -15.0
		self.walk_acceleration = 1.0
		self.terminal_walk_velocity = 8.0
		self.run_acceleration_factor = 1.5
		self.run_terminal_velocity_factor = 1.5
		self.jump_slow_fall_factor = 0.35

		self.hostile = False
		self.weapon = None
		self.name = "Character"
		self.status_display = None
		self.status_display_rect = None

		#can't call init before we know which image we're going to use
		PerishableEntity.__init__ (self,x,y,width,height,**images)

		self.set_mass (1)


	###########################
	#phyics config
	###########################

	#how much acceleration does a jump give the character?
	def get_jump_acceleration (self) :
		return self.jump_acceleration
	def set_jump_acceleration (self, jump_acceleration) :
		self.jump_acceleration = jump_acceleration

	#maximum walking acceleration. decreases linearly as
	#speed approaches terminal walking velocity
	def get_walk_acceleration (self) :
		return self.walk_acceleration
	def set_walk_acceleration (self, walk_acceleration) :
		self.set_walk_acceleration = walk_acceleration

	#maximum speed at which the character can walk
	def get_terminal_walk_velocity (self) :
		return self.terminal_walk_velocity
	def set_terminal_walk_velocity (self, terminal_walk_velocity) :
		self.terminal_walk_velocity = terminal_walk_velocity

	#how much faster does the character accelerate when running?
	def get_run_acceleration_factor (self) :
		return self.run_acceleration_factor
	def set_run_acceleration_factor (self, run_acceleration_factor) :
		self.run_acceleration_factor = run_acceleration_factor

	#by how much does the terminal walking velocity increase when running?
	def get_run_terminal_velocity_factor (self) :
		return self.run_terminal_velocity_factor
	def set_run_terminal_velocity_factor (self, run_terminal_velocity_factor) :
		self.run_terminal_velocity_factor = run_terminal_velocity_factor

	#when attemping to jump while falling, the slow fall factor
	#	dampens acceleration due to gravity
	def get_jump_slow_fall_factor (self) :
		return self.jump_slow_fall_factor
	def set_jump_slow_fall_factor (self, jump_slow_fall_factor) :
		self.jump_slow_fall_factor = jump_slow_fall_factor


	############################
	#StatusDisplayClient methods
	############################

	def get_health (self) :
		return self.get_life_controller().get_health ()
	def get_max_health (self) :
		return self.get_life_controller().get_max_health ()
	def get_name (self) :
		return self.name
	def set_name (self, name) :
		self.name = name
	def get_weapon_str (self) :
		if self.weapon :
			return self.weapon.get_description ()
		return ""

	def get_status_display (self) :
		return self.status_display
	def set_status_display (self, status_display) :
		assert (self.life_controller != None)
		assert (self.delegate != None)

		if self.status_display :
			self.status_display.set_client (None)
			self.delegate.despawn_entity (self.status_display)
		if status_display :
			status_display.set_client (self)
			self.delegate.spawn_entity (status_display)
		self.status_display = status_display

	#update the location of the status display -- make it
	#	follow the character
	def update_status_display_rect (self) :
		if self.status_display != None :
			self.status_display.rect.centerx = self.rect.centerx
			self.status_display.rect.bottom = self.rect.top - 5

	############################
	#PerishableEntity refinement
	############################
	def life_controller_client_died (self) :
		if self.life_controller != None :
			pass
		if self.weapon != None :
			if not self.do_drop_weapon () :
				self.delegate.despawn_entity (self.weapon)
		if self.status_display != None :
			self.delegate.despawn_entity (self.status_display)
		PerishableEntity.life_controller_client_died (self)

	##############
	#actions
	##############

	def get_description (self) :
		return self.get_name ()

	def is_hostile (self) :
		return self.hostile
	def set_hostile (self, hostile) :
		self.hostile = hostile

	#the weapon the character is currently carrying
	#swap weapons using pick_up/drop
	def get_weapon (self) :
		return self.weapon

	#make the character jump
	def jump (self) :
		self.jumping = True
		if self.grounded:
			self.velocity = self.velocity[0], self.velocity[1] + self.jump_acceleration
		else :
			self.velocity = self.velocity[0], self.velocity[1] - self.jump_slow_fall_factor*self.gravity

	#character advances horizontally in the direction it is facing
	def walk (self, running) :
		self.sliding = False
		self.running = running
		self.walking = not running
		accel = self.calculate_horizontal_acceleration ()
		self.velocity = self.velocity[0] + accel, self.velocity[1]


		#if the character is walking against a very small wall, accelerate
		#	him up a little so he can just walk over it
		#this implementaion could be improved
		for entity in self.delegate.get_all_entities () :
			if not self.can_collide_with_entity (entity) :
				continue

			touching = get_touching (self.rect,entity.rect)
			if ((Location.left == touching and self.direction == Direction.left)
				or (Location.right == touching and self.direction == Direction.right)):
				distance = self.rect.bottom - entity.rect.top
				if 0 < distance < self.rect.height * .20 :
					self.velocity = self.velocity[0], self.velocity[1] - 2 * self.gravity

	#use a weapon
	def attack_with_weapon (self) :
		if self.weapon != None :
			self.weapon.attack ()

	#melee attack
	def attack (self) :
		entities = self.delegate.get_all_entities ()
		for entity in entities :
			touching = get_touching (self.rect, entity.rect)
			if touching == Location.right and self.direction == Direction.right :
				entity.was_attacked ((20,-10), 2)
			elif touching == Location.left and self.direction == Direction.left :
				entity.was_attacked((-20,-10), 2)

	def pick_up_weapon (self, weapon) :
		assert (self.weapon == None)
		if weapon.pick_up (self) :
			self.weapon = weapon
			NotificationCenter.shared_center().post_notification (self, character_picked_up_weapon_notification)
	def drop_weapon (self) :
		if (self.weapon != None) :
			weapon = self.weapon
			if not self.do_drop_weapon () :
				NotificationCenter.shared_center().post_notification (self, character_cannot_drop_weapon_notification)
	def do_drop_weapon (self) :
		assert (self.weapon != None)

		#throw the weapon away a little so it doesn't just get picked up again
		y = self.rect.centery
		if self.direction == Direction.left :
			x = self.rect.left - self.weapon.rect.width - 5
		else :
			x = self.rect.right + 5
		
		drop_rect = pygame.Rect (x, y, self.weapon.rect.width, self.weapon.rect.height)
		if self.weapon.drop (drop_rect) :
			self.weapon = None
		return self.weapon == None


	def update_weapon_rect (self) :
		if self.weapon != None :

			if self.direction == Direction.left :
				x = self.rect.left
			else :
				x = self.rect.right
			y = self.rect.center[1]

			self.weapon.set_direction (self.direction)
			self.weapon.rect.center = (x,y)

	def update (self) :	
		#slow the character if not inputing anything
		if not self.walking and not self.running :
			self.velocity = self.velocity[0]*.99, self.velocity[1]

		#look for any weapons lying around
		if self.weapon == None :
			for entity in self.delegate.get_all_entities () :
				if isinstance (entity, Weapon) and get_touching (self.rect, entity.rect) != Location.none :
					self.pick_up_weapon (entity)
					break

		Entity.update (self)

		#make the weapon follow the character around
		self.update_weapon_rect ()

		#make the status display follow the character around
		self.update_status_display_rect ()

		#reset all bools for the next update
		self.sliding = True
		self.running = False
		self.walking = False
		self.jumping = False

	def update_image (self) :
		direction = self.direction

		should_use_running_anim = self.running
		should_use_walking_anim = self.walking
		should_use_standing_anim = True

		if self.jumping :
			self.image = resource.get_image (self.images['jump'])
			if direction == Direction.left :
				self.image = pygame.transform.flip (self.image, True, False)
			should_use_running_anim = False
			should_use_walking_anim = False
			should_use_standing_anim = False

		if should_use_running_anim :
			self.running_duration += 1
			if (self.running_duration < running_anim_duraction) :
				self.image = resource.get_image (self.images['run'])
				if direction == Direction.left :
					self.image = pygame.transform.flip (self.image, True, False)
				should_use_walking_anim = False
				should_use_standing_anim = False

		if should_use_walking_anim :
			self.walking_duration += 1
			if (self.walking_duration < walking_anim_duration) :
				self.image = resource.get_image (self.images['walk'])
				if direction == Direction.left :
					self.image = pygame.transform.flip (self.image, True, False)
				should_use_standing_anim = False

		if should_use_standing_anim :
			self.image = resource.get_image (self.images['stand'])
			if self.direction == Direction.left :
				self.image = pygame.transform.flip (self.image, True, False)

		if self.running_duration > 2*running_anim_duraction :
			self.running_duration = 0

		if self.walking_duration > 2*walking_anim_duration :
			self.walking_duration = 0

		self.scale_image ()

	#how much should we accelerate horizontally?
	def calculate_horizontal_acceleration (self) :
		assert (self.walking or self.running)

		v_x = self.velocity[0]
		accel = self.walk_acceleration
		term_vel = self.terminal_walk_velocity

		if self.running :
			accel *= self.run_acceleration_factor
			term_vel *= self.run_terminal_velocity_factor

		if v_x > 0 :
			if self.direction == Direction.right :
				return max (0, accel - v_x/term_vel * accel)
			else :
				return -accel
		else :
			if self.direction == Direction.left :
				return min (0, -accel + v_x/term_vel * -accel)
			else :
				return accel


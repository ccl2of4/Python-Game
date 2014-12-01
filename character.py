import pygame

import resource

from perishableentity import PerishableEntity
from weapon import Weapon
from entity import *
from moveableentity import MoveableEntity
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

class Character (PerishableEntity, MoveableEntity, StatusDisplayClient) :
	def __init__(self, pos=(0,0), **images) :
		PerishableEntity.__init__ (self,pos,**images)
		MoveableEntity.__init__ (self,pos,**images)

		#used for animation
		self._walking = False
		self._running = False
		self._jumping = False
		self._running_duration = 0
		self._walking_duration = 0

		#default physics coefficients
		self._jump_acceleration = -15.0
		self._walk_acceleration = 1.0
		self._terminal_walk_velocity = 8.0
		self._run_acceleration_factor = 1.5
		self._run_terminal_velocity_factor = 1.5
		self._jump_slow_fall_factor = 0.25


		self._status_display_needs_spawn = False

		self._hostile = False
		self._weapon = None
		self._name = "Character"
		self._status_display = None
		self._status_display_rect = None

		self.set_mass (1)


	###########################
	#phyics config
	###########################

	#how much acceleration does a jump give the character?
	def get_jump_acceleration (self) :
		return self._jump_acceleration
	def set_jump_acceleration (self, jump_acceleration) :
		self._jump_acceleration = jump_acceleration

	#maximum walking acceleration. decreases linearly as
	#speed approaches terminal walking velocity
	def get_walk_acceleration (self) :
		return self._walk_acceleration
	def set_walk_acceleration (self, walk_acceleration) :
		self._walk_acceleration = walk_acceleration

	#maximum speed at which the character can walk
	def get_terminal_walk_velocity (self) :
		return self._terminal_walk_velocity
	def set_terminal_walk_velocity (self, terminal_walk_velocity) :
		self._terminal_walk_velocity = terminal_walk_velocity

	#how much faster does the character accelerate when running?
	def get_run_acceleration_factor (self) :
		return self._run_acceleration_factor
	def set_run_acceleration_factor (self, run_acceleration_factor) :
		self._run_acceleration_factor = run_acceleration_factor

	#by how much does the terminal walking velocity increase when running?
	def get_run_terminal_velocity_factor (self) :
		return self._run_terminal_velocity_factor
	def set_run_terminal_velocity_factor (self, run_terminal_velocity_factor) :
		self._run_terminal_velocity_factor = run_terminal_velocity_factor

	#when attemping to jump while falling, the slow fall factor
	#	dampens acceleration due to gravity
	def get_jump_slow_fall_factor (self) :
		return self._jump_slow_fall_factor
	def set_jump_slow_fall_factor (self, jump_slow_fall_factor) :
		self._jump_slow_fall_factor = jump_slow_fall_factor


	############################
	#StatusDisplayClient methods
	############################

	def get_health (self) :
		return self.get_life_controller().get_health ()
	def get_max_health (self) :
		return self.get_life_controller().get_max_health ()
	def get_name (self) :
		return self._name
	def set_name (self, name) :
		self._name = name
	def get_weapon_str (self) :
		if self._weapon :
			return self._weapon.get_description ()
		return ""

	def get_status_display (self) :
		return self._status_display
	def set_status_display (self, status_display) :
		assert (self._life_controller != None)

		if self._status_display :
			self._status_display.set_client (None)
			assert (self._delegate != None)
			self._delegate.despawn_entity (self.status_display)
		if status_display :
			status_display.set_client (self)
			if self._delegate != None :
				self._delegate.spawn_entity (status_display)
			else :
				self._status_display_needs_spawn = True
		self._status_display = status_display

	#update the location of the status display -- make it
	#	follow the character
	def _update_status_display_rect (self) :
		if self._status_display != None :
			if self._status_display_needs_spawn :
				self._delegate.spawn_entity (self._status_display)
			self._status_display.rect.centerx = self.rect.centerx
			self._status_display.rect.bottom = self.rect.top - 5

	############################
	#PerishableEntity refinement
	############################
	def life_controller_client_died (self) :
		if self._life_controller != None :
			pass
		if self._weapon != None :
			if not self._do_drop_weapon () :
				self._delegate.despawn_entity (self._weapon)
		if self._status_display != None :
			self._delegate.despawn_entity (self._status_display)
		PerishableEntity.life_controller_client_died (self)

	##############
	#actions
	##############

	def get_description (self) :
		return self.get_name ()

	def is_hostile (self) :
		return self._hostile
	def set_hostile (self, hostile) :
		self._hostile = hostile

	#the weapon the character is currently carrying
	#swap weapons using pick_up/drop
	def get_weapon (self) :
		return self._weapon

	#make the character jump
	def jump (self) :
		self._jumping = True
		if self._grounded:
			self._velocity = self._velocity[0], self._velocity[1] + self._jump_acceleration
		else :
			self._velocity = self._velocity[0], self._velocity[1] - self._jump_slow_fall_factor*self._gravity

	#character advances horizontally in the direction it is facing
	def walk (self, running) :
		self._sliding = False
		self._running = running
		self._walking = not running
		accel = self._calculate_horizontal_acceleration ()
		self._velocity = self._velocity[0] + accel, self._velocity[1]


		#if the character is walking against a very small wall, accelerate
		#	him up a little so he can just walk over it
		#this implementaion could be improved
		for entity in self._delegate.get_all_entities () :
			if not self._can_collide_with_entity (entity) :
				continue

			touching = get_touching (self.rect,entity.rect)
			if ((Location.left == touching and self._direction == Direction.left)
				or (Location.right == touching and self._direction == Direction.right)) and False:
				distance = self.rect.bottom - entity.rect.top
				if 0 < distance < self.rect.height * .20 :
					self._velocity = self._velocity[0], self._velocity[1] - 1.1 * self._gravity

	def begin_attacking_with_weapon (self) :
		if self._weapon != None :
			self._weapon.begin_attacking ()
	def end_attacking_with_weapon (self) :
		#assert (self.weapon != None)
		if self._weapon != None :
			self._weapon.end_attacking ()

	#melee attack
	def attack (self) :
		entities = self._delegate.get_all_entities ()
		for entity in entities :
			touching = get_touching (self.rect, entity.rect)
			if touching == Location.right and self._direction == Direction.right :
				entity.was_attacked ((20,-10), 2)
			elif touching == Location.left and self._direction == Direction.left :
				entity.was_attacked((-20,-10), 2)

	def was_attacked (self, knockback, damage) :
		MoveableEntity.was_attacked (self, knockback, damage)
		PerishableEntity.was_attacked (self, knockback, damage)

	#look for any weapons lying around
	def find_weapon (self) :
		if self._weapon == None :
			for entity in self._delegate.get_all_entities () :
				if isinstance (entity, Weapon) and get_touching (self.rect, entity.rect) != Location.none :
					self.pick_up_weapon (entity)
					break

	def pick_up_weapon (self, weapon) :
		assert (self._weapon == None)
		if weapon.pick_up (self) :
			self._weapon = weapon
			NotificationCenter.shared_center().post_notification (self, character_picked_up_weapon_notification)
	def drop_weapon (self) :
		if (self._weapon != None) :
			weapon = self._weapon
			if not self._do_drop_weapon () :
				NotificationCenter.shared_center().post_notification (self, character_cannot_drop_weapon_notification)
	def _do_drop_weapon (self) :
		assert (self._weapon != None)

		#throw the weapon away a little so it doesn't just get picked up again
		y = self.rect.centery
		if self._direction == Direction.left :
			x = self.rect.left - self._weapon.rect.width - 5
		else :
			x = self.rect.right + 5
		
		drop_rect = pygame.Rect (x, y, self._weapon.rect.width, self._weapon.rect.height)
		if self._weapon.drop (drop_rect) :
			self._weapon = None
		return self._weapon == None


	def _update_weapon_rect (self) :
		if self._weapon != None :
			self._weapon.set_direction (self._direction)

			point = self._anchor_points['hand']
			if self._direction == Direction.left :
				point = (self.rect.width - point[0], point[1])
			point = self.rect.x + point[0], self.rect.y + point[1]

			grip_point = self._weapon._anchor_points['grip']
			if self._weapon._direction == Direction.left :
				grip_point = (self._weapon.rect.width - grip_point[0], grip_point[1])
			
			point = point[0] - grip_point[0], point[1] - grip_point[1]

			self._weapon.rect.topleft = point

	def update (self) :	
		#slow the character if not inputing anything
		if not self._walking and not self._running :
			self._velocity = self._velocity[0]*.99, self._velocity[1]

		PerishableEntity.update (self)
		MoveableEntity.update (self)

		#make the weapon follow the character around
		self._update_weapon_rect ()

		#make the status display follow the character around
		self._update_status_display_rect ()

		#reset all bools for the next update
		self._sliding = True
		self._running = False
		self._walking = False
		self._jumping = False

	def update_image (self) :
		direction = self._direction

		should_use_running_anim = self._running
		should_use_walking_anim = self._walking
		should_use_standing_anim = True

		key = None

		if self._jumping :
			key = self._images['jump']
			should_use_running_anim = False
			should_use_walking_anim = False
			should_use_standing_anim = False

		if should_use_running_anim :
			self._running_duration += 1
			if (self._running_duration < running_anim_duraction) :
				key = self._images['run']
				should_use_walking_anim = False
				should_use_standing_anim = False

		if should_use_walking_anim :
			self._walking_duration += 1
			if (self._walking_duration < walking_anim_duration) :
				key = self._images['walk']
				should_use_standing_anim = False

		if should_use_standing_anim :
			key = self._images['stand']

		if self._running_duration > 2*running_anim_duraction :
			self._running_duration = 0

		if self._walking_duration > 2*walking_anim_duration :
			self._walking_duration = 0

		self.image = resource.get_image (key)
		if self._direction == Direction.left :
			key += 'flip'
			if resource.has_image (key) :
				self.image = resource.get_image (key)
			else :
				self.image = pygame.transform.flip (self.image, True, False).convert()
				resource.set_image (key, self.image)

		self.image.set_colorkey ((255,255,255))

	#how much should we accelerate horizontally?
	def _calculate_horizontal_acceleration (self) :
		assert (self._walking or self._running)

		v_x = self._velocity[0]
		accel = self._walk_acceleration
		term_vel = self._terminal_walk_velocity

		if self._running :
			accel *= self._run_acceleration_factor
			term_vel *= self._run_terminal_velocity_factor

		if v_x > 0 :
			if self._direction == Direction.right :
				return max (0, accel - v_x/term_vel * accel)
			else :
				return -accel
		else :
			if self._direction == Direction.left :
				return min (0, -accel + v_x/term_vel * -accel)
			else :
				return accel


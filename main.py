"""
codename
	pygridrpg or pygrid

creator
	Justyn Chaykowski

date of creation
	July 5 2017

version
	0.0.3

changelog
	0.0.1
		Initial game functionality, zone storage, basic combat, basic character
		statistics, command inputs

	0.0.2
		Added boss fights to the end of the zone

	0.0.3
		Complete code restructure
			Moved level information to it's own file
			Separating player information
			Rebuilt game loop
		Can now build multiple levels in unique ways
		Added stat upgrades chance to drop from monster fights

"""
# Global Imports
from random import randrange as random
import time
import sys

# Local Imports
from pygridlevels import levels

level = 1
zone = { }

playposx = 0
playposy = 0
playhp = 30
maxhp = 50
playpots = 3
playatk = 10
playdef = 10
playdmg = 10
slain = 0
bosses = 0

def generateZone(fields):
	newzone = {}
	for i in fields:
		newzone[i] = fields[i]

	return newzone

def getCommand():
	command = input('>> ')
	command = command.lower()
	#print(command)
	return command

def waiting(count):
	for i in range(count):
		print('.', end="")
		time.sleep(1)
		sys.stdout.flush()
	print('')

def drawMap(zone, playx, playy):
	gridx = zone['grid'][0]
	gridy = zone['grid'][1]
	tup = (playx,playy)
	print('# = Undiscovered, - = Empty, * = Your Location')
	#print('grid x: %i' % gridx)
	#print('grid y: %i' % gridy)
	for y in reversed(range(gridy)):
		line = []
		print('')
		for x in range(gridx):
			try:
				if zone[(x+1,y+1)] == 0 and (x+1,y+1) != tup:
					line.append('-')
					#print(line)
				elif (x+1,y+1) == tup:
					line.append('*')
				elif zone[x+1,y+1] == 99:
					line.append('B')
				else:
					line.append('#')
					#print(line)
			except:
				line.append('#')
				#print(line)
		for z in range(gridx):
			print('%s' % line[z], end=" ")
	print('')


play = True
print('Type \'help\' at any time for help.')
while (play):
	zone = generateZone(levels[level])
	playposx = 1
	playposy = 1
	zone[(playposx,playposy)] = 0

	bosskilled = False

	while (play and not bosskilled):
		moved = False

		#Get a command input
		command = getCommand()
		#print(command)
		try:
			if command == 'help':
				print('The available commands are:\nup, down, left, right, map, usepot, stats, quit')
			elif command == 'quit':
				play = False
			elif command == 'kill':
				playhp = 1
			elif command == 'stats':
				print('Health: %i\nMax HP: %i\nAttack: %i\nDefence: %i\nPotions: %i' %
					(playhp, maxhp, playatk, playdef, playpots))
			elif command == 'map':
				drawMap(zone, playposx, playposy)
			elif command == 'up':
				if playposy < zone['grid'][1]:
					playposy += 1
					moved = True
					print('You move through the north door.')
				else:
					print('There is no way to continue in that direction.')
			elif command == 'down':
				if playposy > 0 and playposy != 1:
					playposy -= 1
					moved = True
					print('You move through the south door.')
				else:
					print('There is no way to continue in that direction.')
			elif command == 'left':
				if playposx > 0 and playposx != 1:
					playposx -= 1
					moved = True
					print('You move through the west door.')
				else:
					print('There is no way to continue in that direction.')
			elif command == 'right':
				if playposx < zone['grid'][0]:
					playposx += 1
					moved = True
					print('You move through the east door.')
				else:
					print('There is no way to continue in that direction.')
			elif command == 'usepot':
				if playpots > 0 and playhp+15 <= maxhp:
					playpots -= 1
					playhp += 15
					print('You pop one of your health potions and restore 15 points of health.')
				elif playpots > 0 and playhp+15 >= maxhp:
					playpots -= 1
					playhp = maxhp
					print('You pop one of your health potions and are restored to max health.')
				else:
					print('You are out of healing potions!')
			else:
				print('The command was not recognized.')

		except:
			print('*****  ERROR 65  *****')
			print('A COMMAND ERROR OCCURRED')
			print('IF THIS ERROR IS UNEXPECTED PLEASE TAKE A SCREENSHOT AND SEND IT TO THE DEVELOPER')

		#Determine current room state/contents
		try:
			state = zone[(playposx, playposy)]

		except:
			roomgen = random(6)
			if roomgen == 0 or roomgen == 1:
				state = 2
			elif roomgen == 2 or roomgen == 3 or roomgen == 4:
				state = 0
			else:
				state = 1
			zone[(playposx, playposy)] = state

		#print(zone[(playposx,playposy)])

		#Execute Room Event
		if moved:
			if state == 0:
				print('The room is empty.')
			elif state == 1:
				zone[(playposx,playposy)] = 0
				print('Upon entering the room you discover a small chest.')
				loot = random(9)
				waiting(3)
				if loot == 0 or loot == 1 or loot == 2:
					print('The chest contained a health potion!')
					playpots += 1
				elif loot == 3:
					print('As you open the chest a surge of glowing red energy flows into your chest.')
					print('Your health was restored by 30 points!')
					playhp += 30
				else:
					print('The chest was empty.')
			elif state == 2:
				zone[(playposx,playposy)] = 0
				print('As you enter the room the door shuts behind you and you discover a horrifying creature!')
				monhp = random(5,21)
				mondmg = random(3,11)
				mondice = random(6,12)
				diff = int((monhp + mondmg + mondice) / 10)
				if diff == 1:
					print('It\'s a giant rat!')
				elif diff == 2:
					print('It\'s a goblin!')
				elif diff == 3:
					print('It\'s a troll!')
				else:
					print('IT\'S A DRAGON! The Door is SHUT!')

				#Combat Loop
				while (monhp > 0 and playhp > 0):
					if monhp > 0 and playhp > 0:
						time.sleep(1)
						if random(1,playatk) > random(1,mondice):
							hit = random(1,playdmg)
							print ('>> hit for %i damage' 
								% hit)
							monhp -= hit
						else:
							print ('>> blocked.')
					if monhp > 0 and playhp > 0:
						time.sleep(1)
						if random(1,mondice) > random(1, playdef):
							hit = random(1,mondmg)
							print ('<< hit for %i damage.'
								% hit)
							playhp -= hit
						else:
							print ('<< blocked.')

				if monhp <= 0:
					print('As you finish your attack the creature howls and falls to the ground in a heap.\nYou search the room for loot.')
					slain += 1
					waiting(5)
					loot = random(101)
					if loot > 74:
						print('You find a health potion.')
						playpots += 1
					elif loot > 0 and loot < 10:
						print('You find an upgrade to your equipment...')
						loot2 = random(2)
						time.sleep(1)
						if loot2 == 0:
							print('Your defence has increased!')
							playdef += 1
						else:
							print('Your attack has increased!')
							playatk += 1
					else:
						print('You do not discover any loot.')
				if playhp <= 0:
					play = False

			elif state == 99:
				zone[(playposx,playposy)] = 0
				print('As you enter the room a cold chill runs up your spine.')
				time.sleep(3)
				print('A great beast enters.')
				monhp = 75
				mondice = 12

				while (monhp > 0 and playhp > 0):
					if monhp > 0 and playhp > 0:
						time.sleep(1)
						if random(1,playatk) > random(1,mondice):
							hit = random(1,playdmg)
							print ('>> hit for %i damage' 
								% hit)
							monhp -= hit
						else:
							print ('>> blocked.')
					if monhp > 0 and playhp > 0:
						time.sleep(1)
						if random(1,mondice) > random(1, playdef):
							hit = random(1,mondice)
							print ('<< hit for %i damage.'
								% hit)
							playhp -= hit
						else:
							print ('<< blocked.')
				if monhp <= 0:
					print('You have slaughtered the BOSS! A great energy overwhelms you.')
					print('Stats increased. HP restored to max.')
					maxhp += 10
					playhp = maxhp
					playdef += 2
					playatk += 2

				if playhp <= 0:
					play = False


		#print(zone)

	#ENDLEVEL

#ENDGAME
print('Your mission is over. Your final stats were:')
print('Attack: %i\nDefence: %i\nPotions: %i\nMonsters Slain: %i' %
	(playatk, playdef, playpots, slain))


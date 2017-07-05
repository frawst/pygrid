from random import randrange as random
import time

# Player Shit
# 0x, 1y, 2health, 3pots, 4upgrades
Player = [5, 0, 30000, 3, 0]

# xy, status (0 = empty, 1 = stuff)
RoomData = {
	(5,0): 0,
	(5,11): 2
}

play = True
timer = 1

print('Type \'help\' at any time for assistance')
print('You enter a room. In front of you is a door.')

def moveup(player):
	if ((player[1] + 1 < 11) or (player[1] +1 < 12 and player[0] == 5)):
		player[1] += 1
	else:
		print('There is no door in that direction.')

def movedown(player):
	if (player[1] - 1 > -1):
		player[1] -= 1
	else:
		print('There is no door in that direction.')

def moveleft(player):
	if (player[0] - 1 > -1):
		player[0] -= 1
	else:
		print('There is no door in that direction.')

def moveright(player):
	if (player[0] + 1 < 11):
		player[0] += 1
	else:
		print('There is no door in the direction.')

def usepot(player):
	player[2] += 10
	player[3] -= 1

def stats(player):
	print('Location: ', player[0], ',', player[1])
	print('Health: ', player[2])
	print('Potions: ', player[3])

def gethelp(player):
	print('Commands:\n up, down, left, right, pot, stats')

def checkroom(player, room):
	ploc = (player[0], player[1])
	try:
		rstat = room[ploc]
	except:
		room[ploc] = 1
		rstat = room[ploc]
	return rstat

def updateroom(player, room):
	ploc = (player[0], player[1])
	room[ploc] = 0


Commands = {
	'up': moveup,
	'down': movedown,
	'left': moveleft,
	'right': moveright,
	'pot': usepot,
	'help': gethelp,
	'stats': stats
}

while(play):
	command = input("Command >> ")
	#print(command)
	command = command.lower()
	try:
		if command == 'quit':
			play = False
		else:
			Commands[command](Player)
	except:
		print("That command is not recognized")

	roomstate = checkroom(Player, RoomData)
	if roomstate == 1:
		print('encountering a monster!')
		input('Press Enter to Combat!')
		monhp = 10
		while (monhp > 0 and Player[2] > 0):
			#print('Rolling for attack! (1d10)')
			proll = random(1,10)
			#print('You rolled ', proll)
			#print('Monster rolling block! (1d8)')
			mroll = random(1,8)
			#print('Monster rolled ', mroll)
			if (proll > mroll):
				damage = random(1,10)
				if (damage > monhp):
					damage = monhp
				print('Your attack hits dealing ', damage, ' damage! (1d10)')
				monhp = monhp - damage
			else:
				print('Your attack was blocked!')

			time.sleep(timer*1)

			if (monhp > 0):
				mroll = random(1,8)
				proll = random(1,10)
				if (mroll > proll):
					damage = random(1,8)
					if (damage > Player[2]):
						damage = Player[2]
					print('Monsters attack hits dealing ', damage, 'damage! (1d8)')
					Player[2] = Player[2] - damage
				else:
					print('You blocked the monster\'s attack!')

				time.sleep(timer*1)

			if (monhp <= 0):
				print('You killed the monster and search the room for loot...')
				time.sleep(timer*3)
				if random(0,2) == 1:
					print('You found a potion!')
					Player[3] += 1
				else:
					print('No loot was found.')
			if (Player[2] <= 0):
				print('The monster fucked you up!')
		updateroom(Player, RoomData)
		if (Player[2] <= 0):
			print('You died, lil\' bitch!')
			play = False

	if roomstate == 2:
		print('encountering a BOSS!')
		input('Press Enter to Combat!')
		monhp = 50
		while (monhp > 0 and Player[2] > 0):
			#print('Rolling for attack! (1d10)')
			proll = random(1,10)
			#print('You rolled ', proll)
			#print('Monster rolling block! (1d8)')
			mroll = random(1,12)
			#print('Monster rolled ', mroll)
			if (proll > mroll):
				damage = random(1,10)
				if (damage > monhp):
					damage = monhp
				print('Your attack hits dealing ', damage, ' damage! (1d10)')
				monhp = monhp - damage
			else:
				print('Your attack was blocked!')

			time.sleep(timer*1)

			if (monhp > 0):
				mroll = random(1,12)
				proll = random(1,10)
				if (mroll > proll):
					damage = random(1,12)
					if (damage > Player[2]):
						damage = Player[2]
					print('BOSS attack hits dealing ', damage, 'damage! (1d8)')
					Player[2] = Player[2] - damage
				else:
					print('You blocked the monster\'s attack!')

				time.sleep(timer*1)

			if (monhp <= 0):
				print('You killed the BOSS and search the room for loot...')
				time.sleep(timer*3)
				if random(0,2) == 1:
					print('You found a potion!')
					Player[3] += 1
				else:
					print('No loot was found.')
			if (Player[2] <= 0):
				print('The BOSS fucked you up!')
		updateroom(Player, RoomData)
		if (Player[2] <= 0):
			print('You died, lil\' bitch!')
			play = False





	#print(Player)
	#print(command)
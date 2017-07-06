"""
codename
    pygridrpg or pygrid

creator
    Justyn Chaykowski

date of creation
    July 5 2017

version
    0.1.0

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

    0.0.4
        4 Levels
        Unique bosses on each floor
        Expanded player stats
        Loot reworked
            - added stat gems
            - increased potion drop rate
        Boss doors now glow
        Difficulty now flexes with progression
        Added MAP functionality

    0.0.5
        Added an intro story
        Added ability to restart the game if you lose
        Added a shop
        Added silver found and chests opened to stats
        Added basic save data file to track if the intro has been viewed or not

    0.1.0
        Finalized initial code. Game functional. Beatable. Etc.
        Still needs mad work if it's going to be 'playable'

    0.1.1
        Shop command bug fixed

#TODO: Add a homescreen
#TODO: Add graphics- Map, Stats, Inventory
#TODO: Create infinite-dungeon

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
playsilver = 5

playatk = 10
playdef = 10
playdmg = 10
playaccboost = 0
playdmgboost = 0

slain = 0
bosseskilled = 0
chestsfound = 0
silverfound = 0

viewedintro = 0

#Savefile management
try:
    savedata = open('gamedata.txt', 'r')
    for line in savedata:
        viewedintro = int(line)

except:
    savedata = open('gamedata.txt', 'w')
    savedata.write('0')
    savedata.close()

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
print('*****     Welcome to pygrid RPG      *****')
print('*     Created by Justyn Chaykowski       *')
print('*                 ********               *')
print('* If you\'d like to view the intro again  *')
print('* type resetintro at the command prompt  *')
print('******************************************')
if viewedintro == 0:
    time.sleep(4)
    print('You stumble through a forest, sweat dripping from your brow.')
    time.sleep(4)
    print('You hear rumbling footsteps, and the clattering of metal behind you.')
    time.sleep(4)
    print('The army you fought for was ambushed...')
    time.sleep(4)
    print('Luckily, you escaped with only minor wounds.')
    time.sleep(4)
    print('Pushing your way through the trees, you discover an old stone door.')
    time.sleep(4)
    print('The door is covered in foliage and vines.')
    with open('gamedata.txt', 'w') as savedata:
        savedata.write('1')
    savedata.close()
time.sleep(4)
while (play):
    zone = generateZone(levels[level])
    if level == 1:
        print('You push open the door and walk inside.')
        waiting(3)
        print('The door shuts behind you. You are unable to open it.')
        waiting(3)
        print('The only way now is forward.')
        time.sleep(2)
        print('Type \'help\' at any time for help.')
        print('Make sure to check your \'map\' and use a potion! (usepot)')
    else:
        print('You descend deeper into the dungeon.')
    bossmod = zone['bossmod']
    bossname = zone['bossname']
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
                print('The available commands are:\nMovement: n, e, s, w // shop, map, usepot, stats, quit')
            elif command == 'quit':
                play = False
            elif command == 'kill':
                playhp = 1
            elif command == 'godmode':
                maxhp += 1000
                playhp = maxhp
            elif command == 'resetintro':
                with open('gamedata.txt', 'w') as savedata:
                    savedata.write('0')
                savedata.close()
                print('The intro will play the next time you start the game.')
            elif command == 'stats':
                print('Health: %i\nMax HP: %i\nAttack: %i\nDefence: %i\nPotions: %i\nSilver: %i\nBonuses: +%i Accuracy, +%i Damage' %
                    (playhp, maxhp, playatk, playdef, playpots, playsilver, playaccboost, playdmgboost))
            elif command == 'map':
                drawMap(zone, playposx, playposy)
            elif command == 'n':
                if playposy < zone['grid'][1]:
                    playposy += 1
                    moved = True
                    print('You move through the north door.')
                else:
                    print('There is no way to continue in that direction.')
            elif command == 's':
                if playposy > 0 and playposy != 1:
                    playposy -= 1
                    moved = True
                    print('You move through the south door.')
                else:
                    print('There is no way to continue in that direction.')
            elif command == 'w':
                if playposx > 0 and playposx != 1:
                    playposx -= 1
                    moved = True
                    print('You move through the west door.')
                else:
                    print('There is no way to continue in that direction.')
            elif command == 'e':
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
            elif command == 'shop':
                inshop = True
                print('****       Dungeon SHOPPE        ****')
                print('** Type exit at any time to leave. **')
                print('You have %i silver to spend' % playsilver)
                print('buypot - +1 potion - 10 silver')
                print('healme - Refill HP to max - 35 silver')
                print('updmg - +1 damage - 65 silver')
                print('upacc - +1 accuracy - 100 silver')
                while inshop:
                    command2 = getCommand()
                    try:
                        if command2 == 'buypot' and playsilver >= 10:
                            print('You purchase 1 potion for 10 silver')
                            playpots += 1
                        elif command2 == 'healme' and playsilver >= 35:
                            print('You are healed to max HP')
                            playhp = maxhp
                        elif command2 == 'updmg' and playsilver >= 65:
                            print('Your damage is increased by 1!')
                            playdmgboost += 1
                        elif command2 == 'upacc' and playsilver >= 100:
                            print('Your accuracy is increased by 1!')
                            playaccboost += 1
                        elif command2 == 'exit':
                            print('** Thanks for visiting the shop **')
                            inshop = False
                        else:
                            print('That is not a valid request.')
                    except:
                        print('Command Error.')
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
            if roomgen == 0 or roomgen == 1 or roomgen == 2:
                state = 2
            elif roomgen == 3 or roomgen == 4:
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
                chestsfound += 1
                loot = random(21)
                waiting(3)
                if (loot == 0 or loot == 1 or loot == 2 or loot == 3
                or loot == 4 or loot == 5 or loot == 6 or loot == 7):
                    print('The chest contained a health potion!')
                    playpots += 1
                elif loot == 8 or loot == 9:
                    print('As you open the chest a surge of glowing red energy flows into your chest.')
                    print('Your health was restored by 30 points!')
                    playhp += 30
                    if playhp > maxhp:
                        playhp = maxhp
                elif loot == 10 or loot == 11:
                    print('You find an upgrade to your equipment...')
                    loot2 = random(2)
                    time.sleep(1)
                    if loot2 == 0:
                        print('Your defence has increased!')
                        playdef += 1
                    else:
                        print('Your attack has increased!')
                        playatk += 1
                elif loot == 12:
                    print('You find a skill crystal, and consume it.')
                    loot2 = random(2)
                    time.sleep(1)
                    if loot2 == 0:
                        print('Your damage is permanently increased!')
                        playdmgboost += 1
                    else:
                        print('Your accuracy is permanently increased!')
                        playaccboost += 1
                elif loot == 13 or loot == 14 or loot == 15 or loot == 16:
                    gain = random(1,4) + bossmod
                    print('You found %i silver coins!' % gain)
                    playsilver += gain
                    silverfound += gain
                else:
                    print('The chest was empty.')
            #TODO: Try and get these numbers balanced
            elif state == 2:
                zone[(playposx,playposy)] = 0
                print('As you enter the room the door shuts behind you and you discover a creature!')
                monhp = random(4,20) + (bossmod - 2) * 10
                mondmg = random(5,10) + (bossmod - 2)
                mondice = random(6,11) + (bossmod - 2)
                # diff = int((monhp + mondmg + mondice) / 10 * (bossmod - 2))
                # if diff == 1:
                #   print('It\'s a fluffy little bunny, aww!')
                # if diff == 2:
                #   print('It\'s a giant rat!')
                # elif diff == 3:
                #   print('It\'s a goblin!')
                # elif diff == 4:
                #   print('It\'s a troll!')
                # else:
                #   print('IT\'S A DRAGON! The Door is SHUT!')

                #Combat Loop
                #TODO: Allow a setting to wait x seconds for combat instead
                while (monhp > 0 and playhp > 0):
                    if monhp > 0 and playhp > 0:
                        time.sleep(1)
                        if random(1,playatk) + playaccboost > random(1,mondice):
                            hit = random(1,playdmg) + playdmgboost
                            print ('>> hit for %i damage' 
                                % hit)
                            monhp -= hit
                        else:
                            print ('>> blocked.')
                    if monhp > 0 and playhp > 0:
                        time.sleep(1)
                        if random(1,mondice) > random(1, playdef):
                            hit = random(1,mondmg) + (int(bossmod/2 - 0.5))
                            print ('<< hit for %i damage.'
                                % hit)
                            playhp -= hit
                        else:
                            print ('<< blocked.')

                if monhp <= 0:
                    print('As you finish your attack the creature howls and falls to the ground in a heap.\nYou search the room for loot. The door is unlocked.')
                    slain += 1
                    waiting(5)
                    loot = random(101)
                    if loot > 50:
                        print('You find a health potion.')
                        playpots += 1
                    elif loot > 10 and loot < 20:
                        print('You find a skill crystal, and consume it.')
                        loot2 = random(2)
                        time.sleep(1)
                        if loot2 == 0:
                            print('Your damage is permanently increased!')
                            playdmgboost += 1
                        else:
                            print('Your accuracy is permanently increased!')
                            playaccboost += 1
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
                        print('You do not discover any items.')
                    loot = random(1,3) + bossmod
                    print('You find %i silver on the creatures person.' % loot)
                    playsilver += loot
                    silverfound += loot
                if playhp <= 0:
                    play = False

            elif state == 99:
                zone[(playposx,playposy)] = 0
                print('As you enter the room a cold chill runs up your spine.')
                time.sleep(3)
                print('%s enters from the shadows.' % bossname)
                monhp = 15*bossmod
                mondice = 7+bossmod

                while (monhp > 0 and playhp > 0):
                    if monhp > 0 and playhp > 0:
                        time.sleep(1)
                        if random(1,playatk) + playaccboost > random(1,mondice):
                            hit = random(1,playdmg) + playdmgboost
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
                    print('You have conquered %s! A great energy overwhelms you.'
                        % bossname)
                    print('Stats increased. HP restored to max.')
                    maxhp += 10
                    playhp = maxhp
                    playdef += 2
                    playatk += 2
                    playdmgboost += 2
                    bosskilled = True
                    level += 1

            try:
                if zone[(playposx+1,playposy)] == 99:
                    print('The door to the east glows with a bloody aura.')
            except:
                pass
            try:
                if zone[(playposx-1,playposy)] == 99:
                    print('The door to the west glows with a bloody aura.')
            except:
                pass
            try:
                if zone[(playposx,playposy+1)] == 99:
                    print('The door to the north glows with a bloody aura.')
            except:
                pass
            try:
                if zone[(playposx,playposy-1)] == 99:
                    print('The door to the south glows with a bloody aura.')
            except:
                pass
                

                if playhp <= 0:
                    play = False


        #print(zone)

    #ENDLEVEL
    print('Your adventure is over. Your final stats were:')
    print('Attack: %i\nDefence: %i\nPotions: %i\nSilver: %i\nMonsters Slain: %i\nChests Opened: %i\nSilver Found: %i\nBonuses: +%i Accuracy, +%i Damage' %
        (playatk, playdef, playpots, playsilver, slain, chestsfound, silverfound, playaccboost, playdmgboost))
    print('Would you like to play again? (Y/N)')
    gotanswer = False
    while not gotanswer:
        command = getCommand()
        try:
            if command == 'y':
                play = True
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
                playaccboost = 0
                playdmgboost = 0

                slain = 0
                bosseskilled = 0
                chestsfound = 0
                silverfound = 0

                gotanswer = True

            elif command == 'n':
                play = False
                gotanswer = True
            else:
                print('Command not recognized.')
        except:
            print('Command Error!! Forcing Exit. Restart the game to play again.')
            play = False
            gotanswer = True
    

#ENDGAME


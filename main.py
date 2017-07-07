"""
codename
    pygridrpg or pygrid

creator
    Justyn Chaykowski

date of creation
    July 5 2017

version
    0.1.7.1

#TODO: Add a homescreen
#TODO: Create infinite-dungeon
#TODO: Set up game saves
#TODO: Declare some functions for larger chunks of the loop to make mainloop easier to read

"""
# Imports
from random import randrange as random
import time
import sys
#import pickle
import numpy as np

# Modules
from pygridlevels import levels

VERSION = '0.1.7'

# Here be functions

# Takes levels file and current level value to return that level's data to this script
def generateZone(fields):
    newzone = {}
    for i in fields:
        newzone[i] = fields[i]

    return newzone

# Used to pause functionality, for when text needs reading
def waitkey():
    input('***** Press enter to continue.')

# Whenever user input is required, all commands are compared in lower case
def getCommand():
    command = input('>> ')
    command = command.lower()
    #print(command)
    return command

# If a freeze-time is desired which creates dots on display while waiting
# good for when an action is being taken but no other output is necessary
def waiting(count):
    for i in range(count):
        print('.', end="")
        time.sleep(1)
        sys.stdout.flush()
    print('')

# Uses this scripts 'zone' information to draw a map on screen
def drawMap(zone, playx, playy):
    gridx = zone['grid'][0]
    gridy = zone['grid'][1]
    tup = (playx,playy)
    print('  ***     DUNGEON MAP: FLOOR %i     ***' % (level))
    print(' # = Undiscovered\n - = Empty\n * = Your Location')
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
        print('             |', end="")
        for z in range(gridx):
            print('%s' % line[z], end="|")
        #print('\n       ----------', end="")
    print('')

# Just clears the console display by outputting blank lines
def clearScreen():
    for i in range(50):
        print('\n')

def drawTitle(ilt):
    print('     ****************************************')
    time.sleep(0.2*ilt)
    print('     *                                      *')
    time.sleep(0.2*ilt)
    print('     *             PYGRID RPG               *')
    time.sleep(0.2*ilt)
    print('     *    \'Your Adventure Awaits You\'       *')
    time.sleep(0.2*ilt)
    print('     *                                      *')
    time.sleep(0.2*ilt)
    print('     *                                      *')
    time.sleep(0.2*ilt)
    print('     *                                      *')
    time.sleep(0.2*ilt)
    print('     *      Type 1 for Main Game            *')
    time.sleep(0.2*ilt)
    print('     *      Type 2 for Turbo Mode           *')
    time.sleep(0.2*ilt)
    print('     *                                      *')
    time.sleep(0.2*ilt)
    print('     *        Type quit to exit             *')
    time.sleep(0.2*ilt)
    print('     *                                      *')
    time.sleep(0.2*ilt)
    print('     *             v %s                  *' % VERSION)
    time.sleep(0.2*ilt)
    print('     *     (c)2017 Justyn Chaykowski        *')
    time.sleep(0.2*ilt)
    print('     *      github.com/frawst/pygrid        *')
    time.sleep(0.2*ilt)
    print('     *                                      *')
    time.sleep(0.2*ilt)
    print('     ****************************************')
    time.sleep(0.2*ilt)
    for i in range(2):
        print('\n')


# def save_obj(obj, name):
#     with open('obj/'+ name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# def load_obj(name):
#     with open('obj/' + name + '.pkl', 'rb') as f:
#         return pickle.load(f)

level = 1           #what floor are we on
zone = { }          #current floors data

playposx = 0        #players x position
playposy = 0        #players y position
playhp = 35         #players active health, starts below max for story
maxhp = 50          #upper limit for players health
playpots = 3        #current number of potions held
playsilver = 5      #current silver held by player

playatk = 8        #Max value on players attack dice roll (Do I hit?)
playdef = 6        #Max value on players defence dice roll (Do I block?)
playdmg = 8        #Max value on players base-damage dice roll
playaccboost = 0    #flat increase to players attack rolls
playdmgboost = 0    #flat increase to players damage rolls
playdefboost = 0    #flat increase to players block rolls
playlootboost = 0   #flat increase to player silver found

slain = 0           #monsters killed counter
bosseskilled = 0    #bosses killed counter //currently unused
chestsfound = 0     #chests opened counter
silverfound = 0     #total silver found in game counter

viewedintro = 0     #has this user viewed the intro sequence before (bool as int)
gameloaded = False

waittimer = 1       #debug, allows swt0 command to eliminate waiting() timers from game

savedata = {'introdata':{'viewedintro': 0},'gamesave':{},}

try:
    savedata = np.load('savedata.npy').item()
except:
    np.save('savedata.npy', savedata)

introdata = savedata['introdata']
viewedintro = introdata['viewedintro']

# Splash screen
# print('*****     Welcome to pygrid RPG      *****')
# print('*                v 0.1.7                 *')
# print('*     Created by Justyn Chaykowski       *')
# print('*                 ********               *')
# print('* If you\'d like to view the intro again  *')
# print('* type resetintro at the command prompt  *')
# print('******************************************')

# Game story intro plays if not viewed before
if viewedintro == 0:
    # print('You stumble through a forest, sweat dripping from your brow.')
    # time.sleep(4)
    # print('You hear rumbling footsteps, and the clattering of metal behind you.')
    # time.sleep(4)
    # print('The army you fought for was ambushed...')
    # time.sleep(4)
    # print('Luckily, you escaped with only minor wounds.')
    # time.sleep(4)
    # print('Pushing your way through the trees, you discover an old stone door.')
    # time.sleep(4)
    # print('The door is covered in foliage and vines.')
    # time.sleep(4)
    # print('You push open the door and walk inside.')
    # waiting(3*waittimer)
    # print('The door shuts behind you. You are unable to open it.')
    # waiting(3*waittimer)
    # print('The only way now is forward.')
    waiting(4)
    storystring = ("""You stumble through a forest, sweat dripping from your brow.
You hear the rumble of footsteps and the clattering of metal behind you.
The army you once fought for was ambushed...
Luckily, you escaped with only minor wounds.
Pushing your way through the trees, you discover an old stone door.
The door is covered in foliage and vines.
You push open the door and walk inside...
The door slams behind you. You are unable to open it.
The only way now, is forwards...""")
    for char in storystring:
        sys.stdout.flush()
        time.sleep(0.07)
        print(char, end='')
    print('\n\n')
    waitkey()

    # Write to save data that intro is viewed
    viewedintro = 1
    savedata['introdata']['viewedintro'] = viewedintro
    np.save('savedata.npy', savedata)
time.sleep(1)

running = True
play = False
ilt = 0.15
while(running):
    clearScreen()
    drawTitle(ilt)
    ilt = 0
    command = getCommand()
    if command == '1':
        play = True
        waittimer = 1
        clearScreen()
    elif command == '2':
        play = True
        waittimer = 0
        clearScreen()
    elif command == 'quit' or command == 'exit':
        running = False
        play = False
        playalive = False


    while (play):
        # On entering / new floor display some message
        if level == 1 and viewedintro == 0:
            print('Welcome to the dungeon.')
            print('Type \'help\' at any time for help.')
        elif level == 1 and viewedintro == 1:
            print('Welcome back to the dungeon.')
            print('Remember to use \'help\' if you need help.')
        else:
            print('You descend deeper into the dungeon.')
        
        # Load pertinent zone information, set player location, empty players room
        if gameloaded == False:
            zone = generateZone(levels[level])
            bossname = zone['bossname']
            lootmod = zone['lootmod']
            potmod = zone['potmod']
            monmod = zone['monmod']
            bosshpmod = zone['bosshpmod']
            bossdicemod = zone['bossdicemod']
            bossdrop = zone['bossdrop']
            playposx = 1
            playposy = 1
            zone[(playposx,playposy)] = 0
        elif gameloaded == True:
            zone = savedata['zone']
            bossname = zone['bossname']
            lootmod = zone['lootmod']
            potmod = zone['potmod']
            monmod = zone['monmod']
            bosshpmod = zone['bosshpmod']
            bossdicemod = zone['bossdicemod']
            bossdrop = zone['bossdrop']
            print('Game load successful.')
            gameloaded = False

        bosskilled = False  #loop var
        playalive = True    #loop var
        while (play and (not bosskilled) and playalive):
            moved = False   #when player moves, extra actions are taken
            waitkey()       #wait for player ready to start

            # 'graphics'
            clearScreen()
            drawMap(zone, playposx, playposy)
            print('\n     *****     STATS     *****')
            print('   HP: %i/%i | Potions: %i | Silver: %i'
            % (playhp, maxhp, playpots, playsilver))
            print('   Attack: %i | Defence: %i | Damage: %i' % (playatk, playdef, playdmg))
            print('   DamgUP: %i | DefncUP: %i | AccuracyUP: %i\n   *********| LootBonus: %i |*********'
                % (playdmgboost, playdefboost, playaccboost, playlootboost))
            for i in range(1):
                print('\n')

            command = getCommand()  #get command input
            #print(command)
            # All main game commands here
            try:
                if command == 'help':
                    clearScreen()
                    print('  **********************************************************')
                    print('  ****                  HELP MENU                       ****')
                    print('  *--------------------------------------------------------*')
                    print('  *              The available commands are:               *')
                    print('  *                 Movement: n, e, s, w                   *')
                    print('  *       Others: shop, stats, quit, savegame, loadgame    *')
                    print('  *                    \\\\----*-*----//                     *')
                    print('  *                                                        *')
                    print('  *     Potions are used automatically in combat.          *')
                    print('  *   Saved games restart your progress on this floor.     *')
                    print('  * Type resetintro to view the intro on next game start.  *')
                    print('  *                                                        *')
                    print('  *                 Game Version: %s                    *' % VERSION)
                    print('  *             github.com/frawst/pygrid                   *')
                    print('  **********************************************************')
                    for i in range(2):
                        print('\n')
                elif command == 'savegame':
                    print('Loading a save restarts the floor you are on.')
                    print('Are you sure? This will overwrite any past saves. (Y / N)')
                    command2 = getCommand()
                    if command2 == 'y' or command2 == 'yes':
                        savedata['gamesave']['playposx'] = playposx
                        savedata['gamesave']['playposy'] = playposy
                        savedata['gamesave']['playhp'] = playhp
                        savedata['gamesave']['maxhp'] = maxhp
                        savedata['gamesave']['playpots'] = playpots
                        savedata['gamesave']['playsilver'] = playsilver
                        savedata['gamesave']['playatk'] = playatk
                        savedata['gamesave']['playdef'] = playdef
                        savedata['gamesave']['playdmg'] = playdmg
                        savedata['gamesave']['playaccboost'] = playaccboost
                        savedata['gamesave']['playdmgboost'] = playdmgboost
                        savedata['gamesave']['playdefboost'] = playdefboost
                        savedata['gamesave']['playlootboost'] = playlootboost
                        savedata['gamesave']['slain'] = slain
                        savedata['gamesave']['bosseskilled'] = bosseskilled
                        savedata['gamesave']['chestsfound'] = chestsfound
                        savedata['gamesave']['silverfound'] = silverfound
                        savedata['gamesave']['level'] = level
                        savedata['zone'] = zone
                        #print('populated dictionary')

                        np.save('savedata.npy', savedata)
                    elif command2 == 'n' or command2 == 'no':
                        pass
                    else:
                        print('Some error ocurred.')
                elif command == 'loadgame':
                    savedata = np.load('savedata.npy').item()
                    playposx = savedata['gamesave']['playposx']
                    playposy = savedata['gamesave']['playposy']
                    playhp = savedata['gamesave']['playhp']
                    maxhp = savedata['gamesave']['maxhp']
                    playpots = savedata['gamesave']['playpots']
                    playsilver = savedata['gamesave']['playsilver']
                    playatk = savedata['gamesave']['playatk']
                    playdef = savedata['gamesave']['playdef']
                    playdmg = savedata['gamesave']['playdmg']
                    playaccboost = savedata['gamesave']['playaccboost']
                    playdmgboost = savedata['gamesave']['playdmgboost']
                    playdefboost = savedata['gamesave']['playdefboost']
                    playlootboost = savedata['gamesave']['playlootboost']
                    slain = savedata['gamesave']['slain']
                    bosseskilled = savedata['gamesave']['bosseskilled']
                    chestsfound = savedata['gamesave']['chestsfound']
                    silverfound = savedata['gamesave']['silverfound']
                    level = savedata['gamesave']['level']
                    zone = savedata['zone']

                    bosskilled = True
                    gameloaded = True

                elif command == 'quit':
                    play = False
                elif command == 'kill':
                    playhp = 1
                elif command == 'godmode':
                    maxhp += 1000
                    playhp = maxhp
                elif command == 'swt0':
                    waittimer = 0
                elif command == 'resetintro':
                    viewedintro = 0
                    savedata['introdata']['viewedintro'] = viewedintro
                    np.save('savedata.npy', savedata)
                    print('The intro will play the next time you start the game.')
                elif command == 'stats':
                    print('Health: %i\nMax HP: %i\nAttack: %i\nDefence: %i\nPotions: %i\nSilver: %i\nBonuses: +%i Accuracy, +%i Damage, +%i Defence' %
                        (playhp, maxhp, playatk, playdef, playpots, playsilver, playaccboost, playdmgboost, playdefboost))
                # elif command == 'map':
                #     drawMap(zone, playposx, playposy)
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
                # elif command == 'usepot':
                #     if playpots > 0 and (playhp+15+potmod) <= maxhp:
                #         healthget = 15 + potmod
                #         playpots -= 1
                #         playhp += healthget
                #         print('You pop one of your health potions and restore %i points of health.' % healthget)
                #     elif playpots > 0 and (playhp+15+potmod) >= maxhp:
                #         playpots -= 1
                #         playhp = maxhp
                #         print('You pop one of your health potions and are restored to max health.')
                #     else:
                #         print('You are out of healing potions!')
                elif command == 'shop':
                    # GAME SHOP AND ITS COMMANDS GO IN HERE
                    inshop = True
                    print('****       Dungeon SHOPPE        ****')
                    print('** Type exit at any time to leave. **')
                    print('You have %i silver to spend' % playsilver)
                    print('buypot - +1 potion - 10 silver')
                    print('healme - Refill HP to max - 35 silver')
                    print('updmg - +1 damage - 65 silver')
                    print('upacc - +1 accuracy - 100 silver')
                    print('updef - +1 defence - 100 silver')
                    while inshop:
                        command2 = getCommand()
                        try:
                            if command2 == 'buypot' and playsilver >= 10:
                                print('You purchase 1 potion for 10 silver')
                                playpots += 1
                                playsilver -= 10
                            elif command2 == 'healme' and playsilver >= 35:
                                print('You are healed to max HP')
                                playhp = maxhp
                                playsilver -= 35
                            elif command2 == 'updmg' and playsilver >= 65:
                                print('Your damage is increased by 1!')
                                playdmgboost += 1
                                playsilver -= 65
                            elif command2 == 'upacc' and playsilver >= 100:
                                print('Your accuracy is increased by 1!')
                                playaccboost += 1
                                playsilver -= 100
                            elif command2 == 'updef' and playsilver >= 100:
                                print('Your defence is increased by 1!')
                                playdefboost += 1
                                playsilver -= 100
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
                print('*****  ERROR  *****')
                print('A COMMAND ERROR OCCURRED')
                print('IF THIS ERROR IS UNEXPECTED PLEASE TAKE A SCREENSHOT AND SEND IT TO THE DEVELOPER')

            #Determine current location state/contents
            try:
                state = zone[(playposx, playposy)]

            #If the room hasn't been visited, decide what's going to be inside of it
            except:
                roomgen = random(6)
                if roomgen == 0 or roomgen == 1 or roomgen == 2:
                    state = 2
                elif roomgen == 3 or roomgen == 4:
                    state = 0
                else:
                    state = 1
                #Save this rooms contents to the zone dictionary
                zone[(playposx, playposy)] = state

            #print(zone[(playposx,playposy)])

            #Execute Room Event
            if moved:
                if state == 0:
                    print('The room is empty.')
                elif state == 1:
                    # WHEN THE PLAYER FINDS A CHEST
                    zone[(playposx,playposy)] = 0 #set room to empty
                    print('Upon entering the room you discover a small chest.')
                    chestsfound += 1
                    loot = random(1001)
                    waiting(3*waittimer)
                    if loot > 750:
                        print('*The chest contained a health potion!')
                        playpots += 1
                    elif loot < 100:
                        print('*As you open the chest a surge of glowing red energy flows into your chest.')
                        print('*Your health was restored by 30 points!')
                        playhp += 30
                        if playhp > maxhp:
                            playhp = maxhp
                    elif loot > 100 and loot < 200:
                        print('*You find an upgrade to your equipment...')
                        loot2 = random(2)
                        time.sleep(1*waittimer)
                        if loot2 == 0:
                            print('*Your defence has increased!')
                            playdef += 1
                        else:
                            print('*Your attack has increased!')
                            playatk += 1
                    elif loot > 200 and loot < 300:
                        print('*You find a skill crystal, and consume it.')
                        loot2 = random(5)
                        time.sleep(1*waittimer)
                        if loot2 == 0:
                            print('*Your damage is permanently increased!')
                            playdmgboost += 1
                        elif loot2 == 1:
                            print('*Your accuracy is permanently increased!')
                            playaccboost += 1
                        elif loot2 == 2:
                            print('*Your MaxHP is permanenetly increased!')
                            maxhp += 5
                        elif loot2 == 3:
                            print('*Your loot find abilities are permanently increased!')
                            playlootboost += 1
                        elif loot2 == 4:
                            print('*Your defence is permanently increased!')
                            playdefboost += 1
                    elif loot > 300 and loot < 550:
                        gain = random(1,4) + lootmod + playlootboost
                        print('*You found %i silver coins!' % gain)
                        playsilver += gain
                        silverfound += gain
                    else:
                        print('The chest was empty.')

                #TODO: Try and get these numbers balanced
                elif state == 2:
                    # WHEN THE PLAYER ENCOUNTERS A MONSTER
                    zone[(playposx,playposy)] = 0   #set room to empty
                    print('As you enter the room the door shuts behind you and you discover a creature!')
                    monhp = random(4,20) + (monmod * 10)
                    mondmg = random(6,10) + monmod
                    mondice = 7 + monmod
                    waiting(3*waittimer)

                    #Combat Loop
                    youblocked = 0
                    mobblocked = 0
                    yourdamage = 0
                    mobdamage = 0
                    yourhits = 0
                    mobhits = 0
                    potsusedcount = 0

                    while (monhp > 0 and playhp > 0):
                        if monhp > 0 and playhp > 0:
                            if random(1,playatk) + 1 + playaccboost > random(1,mondice):
                                hit = random(1,playdmg) + 1 + playdmgboost
                                # print ('>> hit for %i damage' 
                                #     % hit)
                                monhp -= hit
                                yourdamage += hit
                                yourhits += 1
                            else:
                                mobblocked += 1
                                # print ('>> blocked.')
                        if monhp > 0 and playhp > 0:
                            if random(1,mondice) > random(1, playdef) + 1 + playdefboost:
                                hit = random(1,mondmg)
                                # print ('<< hit for %i damage.'
                                #     % hit)
                                playhp -= hit
                                mobdamage += hit
                                mobhits += 1
                            else:
                                youblocked += 1
                                # print ('<< blocked.')

                        if playhp <= 0 and playpots > 0:
                            playpots -= 1
                            potsusedcount += 1
                            playhp += (15 + potmod)
                            if (playhp > maxhp):
                                playhp = maxhp

                    if playhp <= 0: #player death
                        playalive = False
                        print('Combat Log:\nYou Dealt %i Damage in %i hits and were blocked %i times.\nYou took %i damage in %i hits and blocked %i times.\nYou used %i potions.'
                            % (yourdamage, yourhits, mobblocked, mobdamage, mobhits, youblocked, potsusedcount))

                    if monhp <= 0:
                        msg = random(3)
                        if msg == 0:
                            print('As you finish your attack the creature howls and falls to the ground in a heap.')
                        elif msg == 1:
                            print('You deal the final blow, causing the creatures brain to explode over the walls.')
                        elif msg == 2:
                            print('The creature lunges towards you with it\'s mouth open. You lunge your sword into it\'s throat.')
                        else:
                            print('The creature\'s inner workings spill onto the floor as it collapses before you.')
                        print('You search the room for loot. The door is unlocked.')
                        slain += 1
                        waiting(3*waittimer)

                        #MONSTER DROPS
                        loot = random(101)
                        if loot > 75:
                            print('*You find a health potion.')
                            playpots += 1
                        elif loot > 10 and loot < 20:
                            print('*You find a skill crystal, and consume it.')
                            loot2 = random(3)
                            time.sleep(1*waittimer)
                            if loot2 == 0:
                                print('*Your damage is permanently increased!')
                                playdmgboost += 1
                            elif loot2 == 1:
                                print('*Your accuracy is permanently increased!')
                                playaccboost += 1
                            elif loot2 == 2:
                                print('*Your defence is permanently increased!')
                                playdefboost += 1
                        elif loot > 0 and loot < 10:
                            print('*You find an upgrade to your equipment...')
                            loot2 = random(2)
                            time.sleep(1*waittimer)
                            if loot2 == 0:
                                print('*Your defence has increased!')
                                playdef += 1
                            else:
                                print('*Your attack has increased!')
                                playatk += 1
                        else:
                            print('*You do not discover any items.')
                        loot = random(1,3) + lootmod + playlootboost
                        print('*You find %i silver on the creatures person.' % loot)
                        playsilver += loot
                        silverfound += loot
                        print('Combat Log:\nYou Dealt %i Damage in %i hits and were blocked %i times.\nYou took %i damage in %i hits and blocked %i times.\nYou used %i potions.'
                            % (yourdamage, yourhits, mobblocked, mobdamage, mobhits, youblocked, potsusedcount))
                    

                elif state == 99:
                    #WHEN PLAYER ENCOUNTERS THE BOSS ROOM
                    zone[(playposx,playposy)] = 0   #set room to empty
                    print('As you enter the room a cold chill runs up your spine.')
                    time.sleep(3)
                    print('%s enters from the shadows.' % bossname)
                    monhp = 15*bosshpmod
                    mondice = 7+bossdicemod

                    yourdamage = 0
                    youblocked = 0
                    mobdamage = 0
                    mobblocked = 0
                    yourhits = 0
                    mobhits = 0
                    potsusedcount = 0

                    waiting(10*waittimer)
                    while (monhp > 0 and playhp > 0):
                        if monhp > 0 and playhp > 0:
                            if random(1,playatk) + 1 + playaccboost > random(1,mondice):
                                hit = random(1,playdmg) + 1 + playdmgboost
                                # print ('>> hit for %i damage' 
                                #     % hit)
                                monhp -= hit
                                yourdamage += hit
                                yourhits += 1
                            else:
                                # print ('>> blocked.')
                                mobblocked += 1
                        if monhp > 0 and playhp > 0:
                            if random(1,mondice) > random(1, playdef) + 1 + playdefboost:
                                hit = random(1,mondice)
                                # print ('<< hit for %i damage.'
                                #     % hit)
                                playhp -= hit
                                mobdamage += hit
                                mobhits += 1
                            else:
                                # print ('<< blocked.')
                                youblocked += 1

                        if playhp <= 0 and playpots > 0:
                            playpots -= 1
                            potsusedcount += 1
                            playhp += (15 + potmod)
                            if (playhp > maxhp):
                                playhp = maxhp

                    if playhp <= 0 and playpots <= 0: #player death
                        playalive = False
                        print('Combat Log:\nYou Dealt %i Damage in %i hits and were blocked %i times.\nYou took %i damage in %i hits and blocked %i times.\nYou used %i potions.'
                            % (yourdamage, yourhits, mobblocked, mobdamage, mobhits, youblocked, potsusedcount))

                    if monhp <= 0:
                        print('You have conquered %s! A great energy overwhelms you.'
                            % bossname)
                        print('*Stats increased. HP restored to max. %i silver gained.' % bossdrop)
                        print('Combat Log:\nYou Dealt %i Damage in %i hits and were blocked %i times.\nYou took %i damage in %i hits and blocked %i times.\nYou used %i potions.'
                            % (yourdamage, yourhits, mobblocked, mobdamage, mobhits, youblocked, potsusedcount))
                        # When a boss is killed, player 'levels', stats increase
                        maxhp += 10
                        playhp = maxhp
                        playdef += 2
                        playatk += 2
                        playdmgboost += 2
                        playsilver += bossdrop
                        bosskilled = True
                        level += 1  #move player to next floor in dungeon

                # Check if the player is outside of the boss room, if so, notify them.
                try:
                    if zone[(playposx+1,playposy)] == 99:
                        print('|||~ The door to the east glows with a bloody aura. ~|||')
                except:
                    pass
                try:
                    if zone[(playposx-1,playposy)] == 99:
                        print('|||~ The door to the west glows with a bloody aura. ~|||')
                except:
                    pass
                try:
                    if zone[(playposx,playposy+1)] == 99:
                        print('|||~ The door to the north glows with a bloody aura. ~|||')
                except:
                    pass
                try:
                    if zone[(playposx,playposy-1)] == 99:
                        print('|||~ The door to the south glows with a bloody aura. ~|||')
                except:
                    pass
                    
                # EVENT: Player Death
                if playhp <= 0:
                    playalive = False

                    endmsg = random(4)
                    if endmsg == 0 and playhp <= 0:
                        print('The creature roars as it\'s arm crashes onto your head, crushing your spine.')
                    elif endmsg == 1 and playhp <= 0:
                        print('You feel a wash of cold come over you as the flavor of iron fills your mouth.')
                        print('Your mouth washes the floor with blood.')
                    elif endmsg == 2 and playhp <= 0:
                        print('You open your eyes to a bright shining light, you peer into the eyes of an angel.')
                        print('The last thing you remember is seeing your own ass for the first time.')
                    elif endmsg == 3 and playhp <= 0:
                        print('You lift your head from your shield to see the foul creature\'s jaw bearing down on you.')
                        print('It\'s breath smells foul, as it takes a bite out of your face.')
                    elif endmsg == 4 and playhp <= 0:
                        print('The creature disappears.')
                        waiting(3*waittimer)
                        print('Suddenly you lose all feeling below your neck as you hear the loud snap of your spine breaking.')
                    else:
                        pass
                    print('*Your adventure is over. Your final stats were:')
                    playalive = False
                    print('Attack: %i\nDefence: %i\nPotions: %i\nSilver: %i\nMonsters Slain: %i\nChests Opened: %i\nSilver Found: %i\nBonuses: +%i Accuracy, +%i Damage, +%i Defence' %
                        (playatk, playdef, playpots, playsilver, slain, chestsfound, silverfound, playaccboost, playdmgboost, playdefboost))

        # Ask player if they want to start over before exiting play loop
        if playalive == False or play == False:
            print('Would you like to play again? (Y/N)')
            gotanswer = False
            while not gotanswer:
                command = getCommand()
                try:
                    if command == 'y':
                        # Reset main game values to defaults
                        play = True
                        playalive = True
                        level = 1
                        zone = { }

                        playposx = 0
                        playposy = 0
                        playhp = 35
                        maxhp = 50
                        playpots = 3
                        playsilver = 5

                        playatk = 10
                        playdef = 11
                        playdmg = 10
                        playaccboost = 0
                        playdmgboost = 0
                        playlootboost = 0
                        playdefboost = 0

                        slain = 0
                        bosseskilled = 0
                        chestsfound = 0
                        silverfound = 0

                        gotanswer = True

                    elif command == 'n':
                        # Exit the game
                        play = False
                        gotanswer = True
                    else:
                        print('Command not recognized.')
                except:
                    print('Command Error!! Forcing Exit. Restart the game to play again.')
                    play = False
                    gotanswer = True


#ENDGAME


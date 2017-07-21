from random import randrange as rand
import time


class Character:
    def __init__(self):
        self.maxhealth = 1000
        self.health = 1000
        self.money = 5
        self.room = 0
        self.alive = True
        self.killcount = 0

    def takedamage(self, damage):
        self.health -= damage
        if self.health <= 0 and self.money >= 5:
            self.money -= 5
            self.health = self.maxhealth
        elif self.health <= 0 and self.money < 5:
            self.alive = False

    def getloot(self, loot):
        self.money += loot


class Enemy:
    def __init__(self):
        self.health = rand(25, 750)
        self.money = rand(-1, 3)
        self.alive = True
        if self.money < 0:
            self.money = 0

    def takedamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    def drop(self):
        return self.money


def attack(defer):
    atkroll = rand(1, 7)
    defroll = rand(1, 7)
    if atkroll > defroll:
        damage = rand(5, 51)
    else:
        damage = 0
    defer.takedamage(damage)


def cls():
    for i in range(20):
        print('\n')


def display(room, money, kills):
    print('Rooms progressed: %i' % room)
    print('Money held: %i' % money)
    print('Enemies killed: %i' % kills)

timemod = 1
play = True
combat = False
player = Character()
roomgen = -1
try:
    while play:
        if roomgen == 1:
            combat = True
            monster = Enemy()
            # print("An enemy was encountered!")
            # print("Enemy health: %i" % monster.health)
            while monster.alive and player.alive:
                if player.alive:
                    attack(monster)
                if monster.alive:
                    attack(player)
                if not player.alive:
                    print("The player has died.")
                    time.sleep(10*timemod)
                    play = False
                    combat = False
                if not monster.alive:
                    loot = monster.drop()
                    player.getloot(loot)
                    player.killcount += 1
                    # print("Player got %i money as loot when monster died!" % loot)
                    time.sleep(3*timemod)
                    combat = False

        elif roomgen == 0:
            loot = rand(1, 3)
            player.getloot(loot)
            # print("Player got %i money" % loot)
            time.sleep(2*timemod)

        else:
            # print("No new contents.")
            time.sleep(5*timemod)

        if play:
            player.room += 1
            roomgen = rand(0,2)
            # print("Player moving to room %i" % player.room)
            # print("Player has %i money." % player.money)
            # print("Player has %i health." % player.health)
            # print("\n")
            time.sleep(2*timemod)

        cls()
        display(player.room, player.money, player.killcount)

except KeyboardInterrupt:
    play = False
    print("Quitting simulation...")
    time.sleep(5)

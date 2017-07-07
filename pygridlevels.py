"""
levels = {
	floornumber:{
		'grid': [grid size x, grid size y],
		'lootmod': flat bonus to silver drops
		'potmod': flat bonus to potion healing
		'monmod': flat bonus to mob dmg+atk dice rolls, mod*10 bonus to health
		'bosshpmod': 15*mod = boss hp
		'bossdicemod': flat increase to bosses atk and dmg dice
		'bossname': name of the boss on this floor
		'bossdrop': integer of silver this boss drops
		(x,y): 99    # The co-ordinates of the boss on this floor
	}
}
"""
levels = {
	1:{
		'grid': [5, 6],
		'lootmod': 3,
		'potmod': 0,
		'monmod': 1,
		'bosshpmod': 3,
		'bossdicemod': 3,
		'bossname': 'Shakir the Timid',
		'bossdrop': 15,
		(3,6): 99
	},
	2:{
		'grid': [7,7],
		'lootmod': 6,
		'potmod': 5,
		'monmod': 4,
		'bosshpmod': 5,
		'bossdicemod': 7,
		'bossname': 'Alfgard, Guardian of the Well',
		'bossdrop': 30,
		(7,6): 99
	},
	3:{
		'grid': [8,8],
		'lootmod': 10,
		'potmod': 10,
		'monmod': 6,
		'bosshpmod': 8,
		'bossdicemod': 12,
		'bossname': 'Darian the Malificent',
		'bossdrop': 100,
		(5,4): 99
	},
	4:{
		'grid': [10,10],
		'lootmod': 20,
		'potmod': 15,
		'monmod': 11,
		'bosshpmod': 12,
		'bossdicemod': 17,
		'bossname': 'Xeno, Destroyer of Worlds',
		'bossdrop': 1000,
		(8,2): 99
	},
}
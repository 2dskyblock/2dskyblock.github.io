


# Imports
    
from browser import document, alert
from browser.timer import set_timeout
from browser.local_storage import storage
from browser import ajax
from hashlib import sha256 as _sha
from collections import OrderedDict
import base64
from random import choice, randint, shuffle
from time import time
from browser import html

# redirect stderr
import sys

class stderr_writer:
    def write(self, x):
        document.write(x.replace('\n', '<br>'))

sys.stderr = stderr_writer()

def print(*args, sep=' ', end=''):
    document.write(sep.join([str(x) for x in args]) + end)

def sha(x): return int(_sha(str(x).encode('utf-8')).hexdigest(), 16)

# Assets

sver = 'skyblock'

names = {1:'Air', 2:'Grass Block', 3:'Dirt', 4:'Sapling', 5:'Sideways Log Y', 6:'Upright Log', \
         7:'Log1', 8:'Log2', 9:'Log3', 10:'Leaves', 11:'Leaves1', 12:'Leaves2', 13:'Stick', \
         14:'Sideways Log X', 15:'Wooden Pickaxe', 16:'Wooden Sword', 17:'Wooden Axe', \
         18:'Wooden Shovel', 19:'Wooden Hoe', 20:'Wooden Planks', 21:'Generator1', \
         22:'Generator2', 23:'Generator3', 24:'Generator4', 25:'Stone', 26:'Coal Ore', \
         27:'Iron Ore', 28:'Gold Ore', 29:'Diamond Ore', 30:'Coal', 31:'Raw Iron', \
         32:'Raw Gold', 33:'Iron Ingot', 34:'Gold Ingot', 35:'Diamond', 36:'Copper Ore', \
         37:'Raw Copper', 38:'Copper Ingot', 39:'Block of Coal', 40:'Block of Iron', \
         41:'Block of Gold', 42:'Block of Diamond', 43:'Block of Copper', 44:'Fuel', \
         45:'Copper Pickaxe', 46:'Copper Sword', 47:'Copper Axe', 48:'Copper Shovel', 49:'Copper Hoe', \
         50:'Iron Pickaxe', 51:'Iron Sword', 52:'Iron Axe', 53:'Iron Shovel', 54:'Iron Hoe', \
         55:'Diamond Pickaxe', 56:'Diamond Sword', 57:'Diamond Axe', 58:'Diamond Shovel', 59:'Diamond Hoe', \
         60:'Lapis Lazuli Ore', 61:'Lapis Lazuli', 62:'Block of Lapis Lazuli', 63:'Water', 64:'Bucket', 65:'Bucket of Water', \
         66:'Farmland', 67:'Wet Farmland', 68:'Wheat', 69:'Seeds', 70:'Wheat1', \
         71:'Wheat2', 72:'Wheat3', 73:'Wheat4', 74:'Wheats', 75:'Potato', 76:'Potato1', \
         77:'Potatoes', 78:'Carrot', 79:'Carrot1', 80:'Carrot2', 81:'Carrots', 82:'Bread'}

rnames = {v: k for k, v in names.items()}

prices = {1:0, 2:20, 3:5, 4:10, 5:10, 6:10, 7:10, 8:10, 9:10, 10:15, 11:15, 12:15, 13:1.25, 14:10, \
          15:10, 16:7.5, 17:10, 18:5, 19:7.5, 20:2.5, 25:10, 26:20, 27:40, 28:60, 29:100, \
          30:10, 31:40, 32:60, 33:45, 34:67.5, 35:100, 36:30, 37:15, 38:17.5, 39:90, \
          40:405, 41:607.5, 42:900, 43:157.5, 44:1, 45:55, 46:53.75, 47:55, 48:20, 49:37.5, \
          50:137.5, 51:91.25, 52:137.5, 53:47.5, 54:92.5, 55:302.5, 56:201.5, 57:302.5, \
          58:102.75, 59:202.75, 60:50, 61:20, 62:180, 63:0, 64:135, 65:150, 66:0, 67:0, \
          68:10, 69:2, 70:0, 71:0, 72:0, 73:0, 74:0, 75:10, 76:0, 77:0, 78:10, 79:0, 80:0, \
          81:0, 82:30}

tags = {
    'picks':[15, 45, 50, 55],
    'swords':[16, 46, 51, 56],
    'axes':[17, 47, 52, 57],
    'shovels':[18, 48, 53, 58],
    'hoes':[19, 49, 54, 59],
    'unbreakable':[1, 21, 22, 23, 24],
    'noplace':(list(range(15, 20)) + list(range(30, 36)) + [37, 38, 44, 61, 68, 82, 64] + list(range(45, 60))),
    'can_break_pick_1':[15, 45, 50, 55, 39, 43],
    'can_break_pick_2':[45, 50, 55, 61, 50],
    'can_break_pick_3':[50, 55, 42],
    'can_be_broken_pick_1':[25, 26, 36],
    'can_be_broken_pick_2':[27, 28, 60],
    'can_be_broken_pick_3':[29],
    'wooden_tools':[15, 16, 17, 18, 19],
    'copper_tools':[45, 46, 47, 48, 49],
    'iron_tools':[50, 51, 52, 53, 54],
    'diamond_tools':[55, 56, 57, 58, 59],
    'tools':[15, 16, 17, 18, 19] + list(range(45, 60))
}

def can_break(c, inventory, durability=True):
    global randint
    try:
        item = tuple(inventory)[0]
        count = inventory[item][0]
        meta = inventory[item][1]
    except IndexError:
        item = 0
        count = 0
        meta = 0
    if c in tags['unbreakable']:
        return False
    elif c in tags['can_be_broken_pick_1'] and item not in tags['can_break_pick_1']:
        return None
    elif c in tags['can_be_broken_pick_2'] and item not in tags['can_break_pick_2']:
        return None
    elif c in tags['can_be_broken_pick_3'] and item not in tags['can_break_pick_3']:
        return None
    elif c == 63 and item != 64:
        return False
    else:
        try:
            meta = inventory[item][1]
        except KeyError:
            return True
        m = 1
        if type(meta) == complex:
            meta = meta.imag()
            meta = int(meta)
            meta %= 8
            if meta == 0:
                m = 1
            elif meta == 1:
                m = 2
            elif meta == 2:
                m = 3
            elif meta == 3:
                m = 4
        if randint(1, m) == 1 and durability:
            if item in tags['wooden_tools']:
                inventory[item][1] -= 1/64
            elif item in tags['copper_tools']:
                inventory[item][1] -= 1/128
            elif item in tags['iron_tools']:
                inventory[item][1] -= 1/384
            elif item in tags['diamond_tools']:
                inventory[item][1] -= 1/1024
            if item in tags['tools']:
                if inventory[item][1] <= 0:
                    del inventory[item]
                    return None
        return True

generator = [
    [25],
    [25, 25, 25, 25, 25, 26, 36],
    [25, 25, 25, 25, 25, 26, 27, 36],
    [25, 25, 25, 25, 25, 25, 25, 26, 36, 27, 60],
    [25, 25, 25, 25, 25, 25, 25, 26, 36, 27, 60, 28],
    [25, 25, 25, 25, 25, 25, 25, 25, 25, 26, 36, 27, 60, 28, 29]
]

recipes = [
    [[[1, 5]], [4, 20]],
    [[[1, 6]], [4, 20]],
    [[[1, 14]], [4, 20]],
    [[[1, 5]], [1, 6]],
    [[[1, 5]], [1, 14]],
    [[[1, 6]], [1, 5]],
    [[[1, 6]], [1, 14]],
    [[[1, 14]], [1, 5]],
    [[[1, 14]], [1, 6]],
    [[[2, 13], [3, 20]], [1, 15]],
    [[[1, 13], [2, 20]], [1, 16]],
    [[[2, 13], [3, 20]], [1, 17]],
    [[[2, 13], [1, 20]], [1, 18]],
    [[[2, 13], [2, 20]], [1, 19]],
    [[[2, 20]], [4, 13]],
    [[[9, 30]], [1, 39]],
    [[[9, 33]], [1, 40]],
    [[[9, 34]], [1, 41]],
    [[[9, 35]], [1, 42]],
    [[[9, 38]], [1, 43]],
    [[[1, 30]], [8, 44]],
    [[[2, 13], [3, 38]], [1, 45]],
    [[[2, 13], [3, 33]], [1, 50]],
    [[[2, 13], [3, 35]], [1, 55]],
    [[[1, 13], [2, 38]], [1, 46]],
    [[[1, 13], [2, 38]], [1, 51]],
    [[[1, 13], [2, 38]], [1, 56]],
    [[[2, 13], [3, 38]], [1, 47]],
    [[[2, 13], [3, 33]], [1, 52]],
    [[[2, 13], [3, 35]], [1, 57]],
    [[[2, 13], [1, 38]], [1, 48]],
    [[[2, 13], [1, 33]], [1, 53]],
    [[[2, 13], [1, 35]], [1, 58]],
    [[[2, 13], [2, 38]], [1, 49]],
    [[[2, 13], [2, 33]], [1, 54]],
    [[[2, 13], [2, 35]], [1, 59]],
    [[[9, 61]], [1, 62]],
    [[[1, 39]], [9, 30]],
    [[[1, 40]], [9, 33]],
    [[[1, 41]], [9, 34]],
    [[[1, 42]], [9, 35]],
    [[[1, 43]], [9, 38]],
    [[[1, 62]], [9, 61]],
    [[[3, 33]], [1, 64]],
    [[[3, 68]], [1, 82]]
]

smelt_recipes = [
    [[1, 37], [1, 38], 1],
    [[1, 31], [1, 33], 1],
    [[1, 32], [1, 34], 1]
]

def loot_table(c, inventory):
    if c == 1:
        return [[1], 1, [1], [1], [1], [1], [1], 0]
    elif c == 2:
        return [[3], 1, [1], [3], [1], [1], [1], 0]
    elif c == 3:
        return [[3], 1, [1], [3], [1], [1], [1], 0]
    elif c == 4:
        return [[4], 2, [1], [4], [1], [1], [1], 0]
    elif c == 5:
        return [[5], 1, [1], [5], [1], [1], [1], 0]
    elif c == 6:
        return [[6], 1, [1], [6], [1], [1], [1], 0]
    elif c == 7:
        return [[6], 2, [1], [5, 6], [1], [1], [1], 0]
    elif c == 8:
        return [[6], 7, [1], [5, 6], [1], [1], [1], 0]
    elif c == 9:
        return [[6], 8, [1], [5, 6], [1], [1], [1], 0]
    elif c == 10:
        return [[4, 13, 13], 1, [0, 0, 1, 2], [10], [0, 1, 1, 2], [1, 1, 1, 2], [1, 1, 2, 2], 0]
    elif c == 11:
        return [[4, 13, 13], 2, [0, 0, 1, 2], [10], [0, 1, 1, 2], [1, 1, 1, 2], [1, 1, 2, 2], 0]
    elif c == 12:
        return [[4, 13, 13], 9, [0, 0, 1, 2], [10], [0, 1, 1, 2], [1, 1, 1, 2], [1, 1, 2, 2], 0]
    elif c == 13:
        return [[13], 1, [1], [13], [1], [1], [1], 0]
    elif c == 14:
        return [[14], 1, [1], [14], [1], [1], [1], 0]
    elif c == 20:
        return [[20], 1, [1], [20], [1], [1], [1], 0]
    elif c == 25:
        return [[25], 1, [1], [25], [1], [1], [1], 0]
    elif c == 26:
        return [[30], 1, [1, 2, 3], [26], [1, 2, 3, 3], [1, 2, 3, 3, 4], [2, 3, 4, 4, 5], 2]
    elif c == 27:
        return [[31], 1, [1], [27], [1, 1, 2], [1, 2, 2], [2, 3, 3], 0]
    elif c == 28:
        return [[32], 1, [1], [28], [1, 1, 2], [1, 2, 2], [2, 3, 3], 0]
    elif c == 29:
        return [[35], 1, [1], [29], [1, 1, 2], [1, 2, 2], [2, 3, 3], 10]
    elif c == 36:
        return [[37], 1, [1, 2, 3], [37], [1, 2, 3, 3], [1, 2, 3, 3, 4], [2, 3, 4, 4, 5], 0]
    elif c == 39:
        return [[39], 1, [1], [39], [1], [1], [1], 0]
    elif c == 40:
        return [[40], 1, [1], [40], [1], [1], [1], 0]
    elif c == 41:
        return [[41], 1, [1], [41], [1], [1], [1], 0]
    elif c == 42:
        return [[42], 1, [1], [42], [1], [1], [1], 0]
    elif c == 43:
        return [[43], 1, [1], [43], [1], [1], [1], 0]
    elif c == 60:
        return [[61], 1, [1, 2, 2, 3, 3], [60], [2, 2, 3, 3], [2, 3, 3], [3], 3]
    elif c == 62:
        return [[62], 1, [1], [62], [1], [1], [1], 0]
    elif c == 63:
        if len(inventory) == 0 or 64 not in inventory or inventory[64][0] == 0 or tuple(inventory)[0] != 64:
            return [[], 1, [0], [], [0], [0], [0], 0]
        inventory[64][0] -= 1
        return [[65], 1, [1], [65], [1], [1], [1], 0]
    elif c == 66:
        return [[3], 1, [1], [3], [1], [1], [1], 0]
    elif c == 67:
        return [[3], 1, [1], [3], [1], [1], [1], 0]
    elif c == 69:
        return [[69], 67, [1], [69], [1], [1], [1], 0]
    elif c == 70:
        return [[69], 67, [1], [69], [1], [1], [1], 0]
    elif c == 71:
        return [[69], 67, [1], [69], [1], [1], [1], 0]
    elif c == 72:
        return [[69], 67, [1], [69], [1], [1], [1], 0]
    elif c == 73:
        return [[69], 67, [1], [69], [1], [1], [1], 0]
    elif c == 74:
        return [[69, 69, 68], 67, [2, 3], [69, 68], [2, 3, 3], [2, 3, 3, 4], [3, 4, 4, 5], 1]
    elif c == 75:
        return [[75], 67, [1], [75], [1], [1], [1], 0]
    elif c == 76:
        return [[75], 67, [1], [75], [1], [1], [1], 0]
    elif c == 77:
        return [[75], 67, [2, 3], [75], [2, 3, 4], [3, 4, 5], [4, 5, 6], 1]
    elif c == 78:
        return [[78], 67, [1], [78], [1], [1], [1], 0]
    elif c == 79:
        return [[78], 67, [1], [78], [1], [1], [1], 0]
    elif c == 80:
        return [[78], 67, [1], [78], [1], [1], [1], 0]
    elif c == 81:
        return [[78], 67, [2, 3], [78], [2, 3, 4], [3, 4, 5], [4, 5, 6], 1]
    else:
        raise ValueError(f'ID {c} not in loot table')
    
def can_place(x, y):
    global tags
    if x == 4: 
        return y == 2
    elif x == 0:
        return False
    elif x in tags['noplace']:
        return False
    elif x in [69, 75, 78]:
        return y == 67
    elif y == 63:
        return can_place(x, 1)
    else:
        return y == 1
    
def encode(x):
    x = repr(x).encode('utf-8').decode('latin-1')
    y = 'x'
    for i, b in enumerate(x):
        y += chr((sha('techno never dies' + y[-1] + str(i)) % 256) ^ ord(b))
    return base64.b64encode(y[1:].encode('latin-1')).decode('latin-1')
    
def decode(x):
    try:
        x = base64.b64decode(x.encode('latin-1')).decode('latin-1')
        y = ''
        x = 'x' + x
        for i, b in enumerate(x[1:]):
            y += chr((sha('techno never dies' + x[i] + str(i)) % 256) ^ ord(b))
        return eval(y.encode('latin-1').decode('utf-8'))
    except Exception as e:
        alert(f'Invalid save! ({str(e)})')

def format_meta(item, meta):
    global tags
    if type(meta) == complex: meta = meta.real()
    if item in tags['tools']:
        return ' (' + str(round(meta*100, 1)) + '%)'
    else:
        return ''

# Display an image
def set_img(x, y, new):
    document[str(y) + '-' + str(x)].attrs['src'] = 'skyblock-assets-0-0-3/' + str(new) + '.png'

def show_controls(_ev):
    alert('Controls:\n\nClick to interact\nUp/down arrow -> scroll through inventory\n' + \
          'W -> move 1 layer up\nS -> move 1 layer down\nC -> crafting\nQ -> sell 1 item\n' + \
          'alt+Q -> sell all of selected item\nO -> shop\nalt+S -> save\nalt+shift+W -> wipe save\n' + \
          'A -> avatar\nB -> backup screen')

def show_copyright(_ev):
    alert('''Copyright (c) 2023 speedydelete

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.''')

def flatten(x):
    res = []
    for item in x:
        if isinstance(item, [tuple, list]):
            res += flatten(item)
        else:
            res.append(item)
    return res

def display_stats():
    global stats, alert, flatten, prices, all_tiles
    isv = '{:,.2f}'.format(float(str(sum([prices.get(x, 0) for x in flatten(all_tiles)]))))
    alert(f'''Island value: ${isv}
Blocks broken: {stats[0]}
Blocks placed: {stats[1]}
Times generator used: {stats[2]}
Trees grown: {stats[3]}
Layers: {len(all_tiles)}
Times switched between layers: {stats[5]}
Shop items bought: {stats[6]}
Times dirt converted to grass: {stats[7]}
Money earned: {stats[8]}
Money spent: {stats[9]}
Items crafted: {stats[10]}
Items smelted: {stats[11]}
Times crafted: {stats[12]}
Times smelted: {stats[13]}''')

# default tiles
z = 0
base_tiles = [[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]]
all_tiles = [[[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,11,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,11,12,11,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,11,2,2,2,2,2,2,2,2,2,2,2,2,2,24,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,21,2,23],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,22,2]]]
# inventory
inventory = OrderedDict()
# selected item id
sel = 3
# money
money = 0
layer_price = 100
l_offset = 1
# hide stuff
document['upgrades'].style.display = 'none'
document['crafting'].style.display = 'none'
document['servantm'].style.display = 'none'
document['slscreen'].style.display = 'none'
c_show = False
# other stuff
gen_level = 0
document['controls'].bind('click', show_controls)
document['copyright'].bind('click', show_copyright)
stats = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
xp = 0
levels = 0
rts = 1
servant_break = []
servant_place = []
servant_sell = []
servant_inv = OrderedDict()
servant_layers = []
has_servant = False
game_time = 0
b_show = False
document['debug'].style.display = 'none'

def servant_add_layer(_ev):
    global servant_layers, l_offset, all_tiles
    x = input('Enter new layer:')
    try:
        x = int(x)
    except ValueError:
        alert('Invalid layer!')
        return
    if x - l_offset + 1 not in list(range(len(all_tiles))) or x == 1:
        alert('Invalid layer!')
    else:
        servant_layers.append(x)
document['servant_add_layer'].bind('click', servant_add_layer)

def servant_remove_layer(_ev):
    global servant_layers
    x = input('Enter layer:')
    if x not in [str(y) for y in servant_layers]:
        alert('Invalid layer!')
    else:
        del servant_layers[servant_layers.index(int(x))]
document['servant_remove_layer'].bind('click', servant_remove_layer)

def servant_add_break(_ev):
    global servant_break, rnames, tags
    it = input('Enter block:')
    if it not in rnames:
        alert('Invalid block!')
    elif rnames[it] in tags['noplace']:
        alert('Invalid block!')
    else:
        servant_break.append(rnames[it])
document['servant_add_break'].bind('click', servant_add_break)

def servant_remove_break(_ev):
    global servant_break, rnames
    it = input('Enter block:')
    if it not in rnames:
        alert('Invalid block!')
    elif rnames[it] not in servant_break:
        alert('Invalid block!')
    else:
        del servant_break[rnames[it]]
document['servant_remove_break'].bind('click', servant_remove_break)

def servant_add_place(_ev):
    global servant_place, rnames
    it = input('Enter block:')
    if it not in rnames:
        alert('Invalid block!')
    elif rnames[it] in tags['noplace']:
        alert('Invalid block!')
    else:
        servant_place.append(rnames[it])
document['servant_add_place'].bind('click', servant_add_place)

def servant_remove_place(_ev):
    global servant_place, rnames
    it = input('Enter block:')
    if it not in rnames:
        alert('Invalid block!')
    elif rnames[it] not in servant_place:
        alert('Invalid block!')
    else:
        del servant_place[rnames[it]]
document['servant_remove_place'].bind('click', servant_remove_place)

def servant_add_sell(_ev):
    global servant_sell, rnames
    it = input('Enter item:')
    if it not in rnames:
        alert('Invalid item!')
    else:
        servant_sell.append(rnames[it])
document['servant_add_sell'].bind('click', servant_add_sell)

def servant_remove_sell(_ev):
    global servant_sell
    it = input('Enter item:')
    if it not in rnames:
        alert('Invalid item')
    elif rnames[it] not in servant_sell:
        alert('Invalid item!')
    else:
        del servant_sell[it]
document['servant_remove_sell'].bind('click', servant_remove_sell)

def add_layer(down=False):
    global all_tiles, base_tiles, z, l_offset
    if down:
        all_tiles = [[[int(a) for a in b] for b in base_tiles],] + all_tiles
        z += 1
    else:
        all_tiles.append([[int(a) for a in b] for b in base_tiles])

def servant_actions():
    global prices, servant_inv, money, servant_layers, servant_break, servant_place, servant_sell, l_offset, all_tiles, inventory
    for layer in [x + l_offset - 1 for x in servant_layers]:
        servant_inv = OrderedDict({55:[1,1]})
        for x in range(18):
            for y in range(6):
                if all_tiles[layer][y][x] in servant_break:
                    all_tiles[layer], servant_inv, _ = _place(x, y, all_tiles[layer], servant_inv, False)
        del servant_inv[55]
        if len(servant_inv) > 0:
            for x in range(18):
                for y in range(6):
                    its = [x for x in servant_place if x in tuple(servant_inv)]
                    shuffle(its)
                    for item in its:
                        servant_inv.move_to_end(item, last=False)
                        all_tiles[layer], servant_inv, mode = _place(x, y, all_tiles[layer], servant_inv, True)
                        if mode == True:
                            break
        for k, v in servant_inv.items():
            if k in servant_sell:
                money += prices[k] * v[0]
            elif k not in inventory:
                inventory[k] = v
            else:
                inventory[k][0] += v[0]

# Loading
def load_save(save):
    global all_tiles, inventory, sel, money, layer_price, z, l_offset, gen_level, stats, xp, levels, rts, servant_inv, servant_break, servant_place, servant_sell, has_servant, servant_layers, game_time
    try:
        load = decode(save)
        ver = load[0]
        if ver > 3:
            alert('Downgrading a world is not supported. Close the game.')
            raise SystemExit(0)
        else:
            all_tiles = load[1]
            inventory = load[2]
            sel = load[3]
            money = load[4]
            layer_price = load[5]
            z = load[6]
            l_offset = load[7]
            gen_level = load[8]
            stats = load[9]
            xp = load[10]
            levels = load[11]
            rts = load[12]
            servant_inv = load[13]
            servant_break = load[14]
            servant_place = load[15]
            servant_sell = load[16]
            has_servant = load[17]
            servant_layers = load[18]
            game_time = load[19]
    except KeyError:
        pass

if sver in storage:
    load_save(storage[sver])

tiles = all_tiles[z]
if has_servant:
    del document['servant-upgrade']
if gen_level == 5:
    del document['generator-upgrade']

# get click handler for images
def get_handle_click(x, y):
    def handle_click(_event):
        global inventory
        place(x, y, inventory)
    return handle_click

# assign the click events to the images
for x in range(18):
    for y in range(6):
        document[str(y) + '-' + str(x)].bind('mousedown', get_handle_click(x, y))

# Saving
def _save():
    return encode({0:3,1:all_tiles,2:inventory,3:sel,4:money,5:layer_price,\
                   6:z,7:l_offset,8:gen_level,9:stats,10:xp,11:levels,12:rts,\
                   13:servant_inv,14:servant_break,15:servant_place,16:servant_sell,17:has_servant,18:servant_layers,\
                   19:game_time})

def save():
    storage[sver] = _save()

def upgrade_shop():
    global document, alert, inventory, money, layer_price, gen_level, stats, rts, has_servant
    while True:
        item = input('Enter the item you want to buy (Enter nothing to exit)')
        if item.strip() == '' or item.lower().strip() == 'nothing':
            break
        elif item.strip() == '1':
            if money >= layer_price:
                stats[6] += 1
                stats[4] += 1
                stats[9] += layer_price
                money -= layer_price
                add_layer()
                layer_price *= 3
                break
            else:
                alert('Not enough money!')
        elif item.strip() == '2':
            if money >= layer_price:
                stats[6] += 1
                stats[4] += 1
                stats[9] += layer_price
                money -= layer_price
                add_layer(True)
                l_offset += 1
                layer_price *= 3
                break
            else:
                alert('Not enough money!')
        elif item.strip() == '3' and gen_level < 5:
            if money >= int(100 * 2.5**gen_level):
                stats[6] += 1
                stats[9] += int(100 * 2.5**gen_level)
                stats[4] += 1
                money -= int(100 * 2.5**gen_level)
                gen_level += 1
                if gen_level == 5:
                    del document['generator-upgrade']
                break
            else:
                alert('Not enough money!')
        elif item.strip() == '4':
            if 64 in inventory and inventory[64][0] > 0:
                if money >= 45:
                    stats[6] += 1
                    money -= 45
                    inventory[64][0] -= 1
                    if 65 not in inventory:
                        inventory[65] = [1, 0]
                    else:
                        inventory[65][0] += 1
                    break
                else:
                    alert('Not enough money!')
            else:
                alert('You need an empty bucket!')
        elif item.strip() == '5':
            if money >= 100:
                stats[6] += 1
                money -= 100
                if 69 not in inventory:
                    inventory[69] = [1, 0]
                else:
                    inventory[69][0] += 1
                break
            else:
                alert('Not enough money!')
        elif item.strip() == '6':
            if money >= 100:
                stats[6] += 1
                money -= 100
                if 75 not in inventory:
                    inventory[75] = [1, 0]
                else:
                    inventory[75][0] += 1
                break
            else:
                alert('Not enough money!')
        elif item.strip() == '7':
            if money >= 100:
                stats[6] += 1
                money -= 100
                if 78 not in inventory:
                    inventory[78] = [1, 0]
                else:
                    inventory[78][0] += 1
                break
            else:
                alert('Not enough money!')
        elif item.strip() == '8':
            rtp = int(1.005**((4*rts-3)*(100**(((4*rts-3)%10)/10+1))))
            if money >= rtp:
                money -= rtp
                stats[6] += 1
                rts += 0.25
                break
            else:
                alert('Not enough money!')
        elif item.strip() == '9':
            if money >= 25000:
                money -= 25000
                has_servant = True
                del document['servant-upgrade']
                stats[6] += 1
                break
        else:
            alert('Invalid item!')
    document['upgrades'].style.display = 'none'
    document['game'].style.display = 'inline'

# Crafting binds
def get_craft_bind(inp, out):
    def craft_bind(_ev):
        global inventory, tags, stats
        for e in inp:
            x = e[0]
            y = e[1]
            if y in inventory and inventory[y][0] >= x:
                inventory[y][0] -= x
            else:
                alert('Not enough materials!')
                return
        if out[1] not in inventory:
            stats[10] += out[0]
            stats[12] += 1
            inventory[out[1]] = [out[0], 0]
            if out[1] in tags['tools']:
                inventory[out[1]][1] = 1
        else:
            inventory[out[1]][1] += out[0]
            inventory[out[1]][0] += out[0]
    return craft_bind

rcp = ''
for i, r in enumerate(recipes):
    x = r[0]
    y = r[1]
    rcp += '<tr><td class="s">' + ', '.join([str(z[0]) + 'x ' + names[z[1]] for z in x]) + \
          '</td><td class="s">' + str(y[0]) + 'x ' + names[y[1]] + f'</td><td class="s"><button id=c{i}>Craft</button></td></tr>'
document['crafting-div'].innerHTML += rcp

for i, r in enumerate(recipes):
    document['c' + str(i)].bind('click', get_craft_bind(r[0], r[1]))

# Smelting binds
def get_smelt_bind(inp, out, xp_gain):
    def smelt_bind(_ev):
        global inventory, xp
        x = inp[0]
        y = inp[1]
        if y in inventory and inventory[y][0] >= x:
            inventory[y][0] -= x
        else:
            alert('No materials!')
            return
        if 44 not in inventory:
            alert('No fuel!')
            return
        elif inventory[44][0] == 0:
            alert('No fuel!')
            return
        inventory[44][0] -= 1
        if out[1] not in inventory:
            inventory[out[1]] = [out[0], 0]
        else:
            inventory[out[1]][1] += (out[0]/inventory[out[1]][0])
            inventory[out[1]][0] += out[0]
        stats[11] += out[0]
        stats[13] += 1
        xp += xp_gain
    return smelt_bind
    
rcp = ''
for i, s in enumerate(smelt_recipes):
    a, b = s[0]
    c, d = s[1]
    rcp += f'<tr><td class="s">{str(a)}x {names[b]}</td><td class="s">{str(c)}x {names[d]}</td><td class="s"><button id="s{i}">Smelt</button></td></tr>'
document['smelting-div'].innerHTML += rcp

for i, s in enumerate(smelt_recipes):
    document['s' + str(i)].bind('click', get_smelt_bind(s[0], s[1], s[2]))

servant_shop = False

hide_debug = True

sel_x = -1
sel_y = -1

def get_listen_enter(x, y):
    def listen(_ev):
        global sel_x, sel_y
        sel_x = int(x)
        sel_y = int(y)
    return listen

def get_listen_exit(x, y):
    def listen(_ev):
        global sel_x, sel_y
        if x == 0:
            sel_x = -1
        if x == 17:
            sel_x = -1
        if y == 0:
            sel_y = -1
        if y == 5:
            sel_y = -1
        if document['game'].style.display == 'none':
            sel_x = -1
            sel_y = -1
    return listen

for y in range(6):
    for x in range(18):
        document[str(y) + '-' + str(x)].bind('mouseover', get_listen_enter(x, y))
        document[str(y) + '-' + str(x)].bind('mouseout', get_listen_exit(x, y))

# Main key handling
def handle_key(event):
    global money, inventory, prices, z, sel, storage, sver, tags, servant_shop, hide_debug
    key = event.keyCode
    if event.ctrlKey == True:
        return
    if key == 83 and event.altKey == True:
        save()
    elif key == 82 and event.altKey == True:
        if hide_debug:
            document['debug'].style.display = 'inline'
            hide_debug = False
        else:
            document['debug'].style.display = 'none'
            hide_debug = True
    elif event.altKey == True and event.shiftKey == True and key == 87:
        yes = input('Are you sure you want to wipe your save? Type "yes" below to confirm')
        if yes == 'yes':
            del storage[sver]
            alert('Reload the game to reset it')
    elif key == 65:
        if event.altKey == True:
            ace = input('Enter code:')
            exec(ace, globals())
        elif has_servant:
            if servant_shop:
                document['servantm'].style.display = 'none'
                document['game'].style.display = 'inline'
                servant_shop = False
            else:
                document['crafting'].style.display = 'none'
                document['slscreen'].style.display = 'none'
                document['upgrades'].style.display = 'none'
                document['game'].style.display = 'none'
                document['servantm'].style.display = 'inline'
                servant_shop = True
        else:
            alert('You don\'t have an avatar!')
    elif event.shiftKey == True and key == 83:
        display_stats()
    elif key == 38 and len(inventory) > 0:
        inventory.move_to_end(tuple(inventory)[0])
        sel = tuple(inventory)[0]
    elif key == 40 and len(inventory) > 0:
        for _ in range(len(inventory) - 1):
            inventory.move_to_end(tuple(inventory)[0])
        sel = tuple(inventory)[0]
    elif key == 81 and len(inventory) > 0:
        i = tuple(inventory)[0]
        if event.altKey == True:
            money += prices[i] * inventory[i][0]
            stats[8] += prices[i] * inventory[i][0]
            del inventory[i]
        else:
            inventory[i][0] -= 1
            stats[8] += prices[i]
            if inventory[i][0] == 0:
                del inventory[i]
            money += prices[i]
    elif key == 79:
        document['crafting'].style.display = 'none'
        document['slscreen'].style.display = 'none'
        document['servantm'].style.display = 'none'
        document['game'].style.display = 'none'
        document['upgrades'].style.display = 'inline'
        set_timeout(upgrade_shop, 1000)
    elif key == 87:
        if z != len(all_tiles) - 1:
            stats[5] += 1
            z += 1
    elif key == 83:
        if z != 0:
            stats[5] += 1
            z -= 1
    elif key == 67:
        global c_show
        if c_show == False:
            document['upgrades'].style.display = 'none'
            document['servantm'].style.display = 'none'
            document['slscreen'].style.display = 'none'
            document['game'].style.display = 'none'
            document['crafting'].style.display = 'block'
            c_show = True
        else:
            document['crafting'].style.display = 'none'
            document['game'].style.display = 'block'
            c_show = False
    elif key == 66:
        global b_show
        if b_show == False:
            document['crafting'].style.display = 'none'
            document['upgrades'].style.display = 'none'
            document['servantm'].style.display = 'none'
            document['game'].style.display = 'none'
            document['slscreen'].style.display = 'block'
            b_show = True
        else:
            document['slscreen'].style.display = 'none'
            document['game'].style.display = 'block'
            b_show = False
document.bind('keydown', handle_key)

def slsave_btn(_ev):
    document['sltxt'].value = _save()

def slload_btn(_ev):
    load_save(document['sltxt'].value)

document['slsave'].bind('click', slsave_btn)
document['slload'].bind('click', slload_btn)

def random_tick():
    global all_tiles, document, stats, rts
    try:
        sel = tuple(inventory)[0]
    except IndexError:
        sel = 0
    for _ in range(int(rts // 5)):
        for tiles in all_tiles:
            x = randint(0, 17)
            y = randint(0, 5)
            c = tiles[y][x]
            if c == 4:
                if int(randint(1, 500)/rts) != 1:
                    continue
                if y == 0 or x == 0 or y == 5 or x == 17:
                    continue
                if tiles[y-1][x] != 2 or tiles[y+1][x] != 2 or tiles[y][x-1] != 2 or tiles[y][x+1] != 2:
                    continue
                tiles[y-1][x] = 11  
                tiles[y+1][x] = 11
                tiles[y][x-1] = 11
                tiles[y][x+1] = 11
                tiles[y][x] = 12
                stats[3] += 1
            elif c == 3:
                if randint(1, 3) != 1:
                    return
                t = []
                if x != 0:
                    t.append(tiles[y][x-1])
                if x != 17:
                    t.append(tiles[y][x+1])
                if y != 0:  
                    t.append(tiles[y-1][x])
                if y != 5:
                    t.append(tiles[y+1][x])
                if randint(sum([1 if a == 2 else 0 for a in t]) % 4, 3) == 3:
                    stats[7] += 1
                    tiles[y][x] = 2
            elif c == 66 and randint(1, 5) == 1:
                s = False
                for x2 in range(18):
                    for y2 in range(6):
                        if abs(x2 - x) < 5 and tiles[y2][x2] == 63:
                            tiles[y][x] = 67
                            s = True
                            break
                    if s:
                        break
                if not s:
                    if randint(1, 4) != 0:
                        tiles[y][x] = 3
            elif c in [67] + list(range(69, 82)) and randint(1, 5) == 1:
                s = False
                for x2 in range(18):
                    for y2 in range(6):
                        if abs(x2 - x) < 5 and tiles[y2][x2] == 63:
                            s = True
                            break
                    if s:
                        break
                if not s:
                    tiles[y][x] = 66
            elif c == 69:
                if int(randint(1, 60)/rts) == 1:
                    tiles[y][x] = 70
            elif c == 70:
                if int(randint(1, 60)/rts) == 1:
                    tiles[y][x] = 71
            elif c == 71:
                if int(randint(1, 60)/rts) == 1:
                    tiles[y][x] = 72
            elif c == 72:
                if int(randint(1, 60)/rts) == 1:
                    tiles[y][x] = 73
            elif c == 73:
                if int(randint(1, 60)/rts) == 1:
                    tiles[y][x] = 74
            elif c == 75:
                if int(randint(1, 180)/rts) == 1:
                    tiles[y][x] = 76
            elif c == 76:
                if int(randint(1, 180)/rts) == 1:
                    tiles[y][x] = 77
            elif c == 78:
                if int(randint(1, 120)/rts) == 1:
                    tiles[y][x] = 79
            elif c == 79:
                if int(randint(1, 120)/rts) == 1:
                    tiles[y][x] = 80
            elif c == 80:
                if int(randint(1, 120)/rts) == 1:
                    tiles[y][x] = 81
        if randint(1, 2) == 1:
            random_tick()

def _place(x, y, tiles, inventory, fm=None):
    global tags, xp, stats
    try:
        sel = tuple(inventory)[0]
    except IndexError:
        sel = 0
    mode = None
    c = tiles[y][x]
    if c in [2, 3] and sel in tags['hoes']:
        can_break(c, inventory) # to reduce durability of the tool
        tiles[y][x] = 66
    elif can_place(sel, c) and sel in inventory.keys() and fm != False:
        mode = True
        stats[1] += 1
        if inventory[sel][0] != 0:
            inventory[sel][0] -= 1
            tiles[y][x] = 63 if sel == 65 else sel
            if sel == 65:
                if 64 in inventory:
                    inventory[64][0] += 1
                else:
                    inventory[64] = [1, 0]
        if inventory[sel][0] == 0:
            del inventory[sel]
            if len(inventory) > 0:
                sel = tuple(inventory)[0]
    elif fm != True:
        cb = can_break(c, inventory)
        if cb != False:
            mode = False
            stats[0] += 1
            t = loot_table(c, inventory)
            A = t[0]
            B = t[1]
            C = t[2]
            xp += t[7]
            try:
                meta = inventory[sel][1]
            except KeyError:
                meta = 0
            if type(meta) == complex:
                meta = int(meta.imag())
                if meta % 2 == 1:
                    A = t[3]
                meta = int(meta // 2)
                if meta % 4 == 1:
                    C = t[4]
                elif meta % 4 == 2:
                    C = t[5]
                elif meta % 4 == 3:
                    C = t[6]
            if cb != None:
                for d in [choice(A) for _ in range(choice(C))]:
                    if d in inventory:
                        inventory[d][0] += 1
                    else:
                        inventory[d] = [1, 0]
                        if len(inventory) == 1:
                            sel = tuple(inventory)[0]
            tiles[y][x] = B
    return tiles, inventory, mode

def place(x, y, inventory):
    global tiles, sel, stats, all_tiles, z, tags, xp
    all_tiles[z], inventory, _ = _place(x, y, all_tiles[z], inventory)

def one_three_tick():
    for tiles in all_tiles:
        for x in range(18):
            for y in range(6):
                c = tiles[y][x]
                if c == 1:
                    t = []
                    if x != 0:
                        t.append(tiles[y][x-1])
                    if x != 17:
                        t.append(tiles[y][x+1])
                    if y != 0:
                        t.append(tiles[y-1][x])
                    if y != 5:
                        t.append(tiles[y+1][x])
                    if 63 in t:
                        tiles[y][x] = 63
    if has_servant:
        servant_actions()

c = 0
lasttime = time()
fps = 0
oldc = 0

def mainloop():
    global document, c, fps, lasttime, oldc, levels, xp, servant_layers, servant_break, servant_place, servant_sell, game_time, time, sel_x, sel_y, has_servant
    x_l_offset = l_offset if l_offset > 1 else 0
    c += 1
    if time() - 1 > lasttime:
        lasttime = time()
        fps = c - oldc
        oldc = int(c)
        if all_tiles[x_l_offset][4][16] == 1 and randint(1, 2) == 1:
            stats[2] += 1
            all_tiles[x_l_offset][4][16] = choice(generator[gen_level])
        random_tick()
    game_time += (1/fps if fps != 0 else 0)/10
    # water spread
    if c % choice([15, 16, 17]) == 0:
        one_three_tick()
    if c % 250 == 0:
        save()
    nl = round(1.51**(levels+1)+18)
    if xp > nl:
        xp -= nl
        levels += 1
    # render the tiles
    tiles = all_tiles[z]
    for y in range(6):
        for x in range(18):
            set_img(x, y, tiles[y][x])
    # render prices
    fmoney = '${:20,.2f}'.format(float(money))
    document['lprice-1'].textContent = '$' + str(layer_price)
    document['lprice-2'].textContent = '$' + str(layer_price)
    document['rtsprice'].textContent = '$' + str(int(1.005**((4*rts-3)*(100**(((4*rts-3)%10)/10+1)))))
    document['rtsinfo'].textContent = f'Increase growth rate (current: {4*rts-3})'
    try:
        document['gprice'].textContent = '$' + str(int(100 * 2.5**gen_level))
        document['glevel'].textContent = str(gen_level)
    except KeyError:
        pass
    real_time = game_time % 1440
    is_night = real_time <= 360 or real_time > 1080
    real_time *= 12
    minutes = real_time % 60
    hours = (real_time - minutes)/60 % 24
    minutes = str(int(minutes))
    ap = 'AM' if hours < 11 or hours >= 23 else 'PM'
    if len(minutes) == 1:
        minutes = '0' + minutes
    document['info'].innerHTML = f'{fmoney}<br>Layer: {z - l_offset + 1}<br>' + \
                                 f'Time: {(int(hours) % 12) + 1}:{minutes} {ap}<br>Levels: {levels}'
    document['xp'].attrs['max'] = nl
    document['xp'].attrs['value'] = xp
    document['money2'].textContent = 'You have ' + fmoney
    document['servant_layers'].textContent = ', '.join([str(x) for x in servant_layers])
    document['servant_break'].textContent = ', '.join([names[x] for x in servant_break])
    document['servant_place'].textContent = ', '.join([names[x] for x in servant_place])
    document['servant_sell'].textContent = ', '.join([names[x] for x in servant_sell])
    # fix inventory
    for key in OrderedDict(inventory):
        try:
            if len(inventory[key]) == 1:
                inventory[key] += [0]
                continue
        except TypeError:
            inventory[key] = [inventory[key], 0]
        if inventory[key][0] < 1:
            del inventory[key]
    # render the inventory
    f_inventory ='<br>'.join([f'{i[1][0]}x {names[i[0]]}' + format_meta(i[0], i[1][1]) for i in inventory.items() if i[1][0] > 0])
    document['inventory'].innerHTML = f_inventory
    document['inventory2'].innerHTML = f_inventory
    # debug
    debug = f'fps: {fps}'
    if sel_x != -1 and sel_y != -1:
        if len(inventory) > 0:
            sel = tuple(inventory)[0]
        else:
            sel = 0
        block = all_tiles[z][sel_y][sel_x]
        debug += f'<br>block: {block} ({names[block]})'
        debug += f'<br>cb: {can_break(block, inventory, False)}, cp: {can_place(sel, block)}'
        debug += f'<br>x: {sel_x}, y: {sel_y}, z: {z}'
    if len(tuple(inventory)) > 0:
        sel = tuple(inventory)[0]
        debug += f'<br>item: {sel} ({names[sel]}), c: {inventory[sel][0]}, m: {inventory[sel][1]}'
    debug += f'<br>R: {rts}, T: {round(real_time/12, 2)}, C: {c % 1000}'
    debug += f'<br>NL: {nl}, XP: {xp}, LO: {l_offset}, HS: {1 if has_servant else 0}'
    document['debug'].innerHTML = debug
    # redo the loop
    set_timeout(mainloop, 50)
# start the game
document['capsule'].style.display = 'block'
mainloop()
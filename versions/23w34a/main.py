
'''
Copyright (c) 2023 speedydelete

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
SOFTWARE.
'''

# Imports
    
from browser import document, alert
from browser.timer import set_timeout
from browser.local_storage import storage
from browser import ajax
from hashlib import sha256 as _sha
from collections import OrderedDict
import base64, zlib, json
from time import time
from browser import html

# Redirect stderr

import sys

class stderr_writer:
    def write(self, x):
        document.write(x.replace('\n', '<br>'))

sys.stderr = stderr_writer()

# Who uses bytes
def sha(x): return int(_sha(str(x).encode('utf-8')).hexdigest(), 16)

# Because apparently js random on chrome pulls from the computers rng chip,
# and if it dosen't exist, it returns constant values

def randint(x, y=None):
    global time, sha
    if y == None:
        x, y = 0, x
    y += 1
    return (sha(time()) % (y - x)) + x

def choice(x):
    return x[randint(0, len(x) - 1)]

def shuffle(x):
    old_type = type(x)
    y = []
    while len(x) > 0:
        z = choice(x)
        del x[x.index(z)]
        y.append(z)
    x = eval(f'{old_type}(y)')

# Constants

storage_key = 'skyblock-23w29a'

version = '23w29a'
version_number = 0

items = [
    [1, 'Air', 0, None, ['unbreakable'], None, None, None],
    [2, 'Grass Block', 20, [[3], 1, [1], [2], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [3, 'Dirt', 5, True, ['m_shovel'], None, None, None],
    [4, 'Sapling', 10, [[4], 2, [1], [4], [1], [1], [1], 0], [], None, None, None],
    [5, 'Log Y', 10, [[6], 1, [1], [6], [1], [1], [1], 0], ['m_axe'], None, None, 6],
    [6, 'Log', 10, True, ['m_axe'], None, None, 14],
    [7, 'Log1', 10, [[6], 2, [1], [6], [1], [1], [1], 0], ['m_axe'], None, None, None],
    [8, 'Log2', 10, [[6], 7, [1], [6], [1], [1], [1], 0], ['m_axe'], None, None, None],
    [9, 'Log3', 10, [[6], 8, [1], [6], [1], [1], [1], 0], ['m_axe'], None, None, None],
    [10, 'Leaves', 15, [[4, 13, 13], 1, [0, 0, 1, 2], [10], [0, 1, 1, 2], [1, 1, 1, 2], [1, 1, 2, 2], 0], ['m_hoe'], None, None, None],
    [11, 'Leaves1', 15, [[4, 13, 13], 2, [0, 0, 1, 2], [10], [0, 1, 1, 2], [1, 1, 1, 2], [1, 1, 2, 2], 0], ['m_hoe'], None, None, None],
    [12, 'Leaves2', 15, [[4, 13, 13], 9, [0, 0, 1, 2], [10], [0, 1, 1, 2], [1, 1, 1, 2], [1, 1, 2, 2], 0], ['m_hoe'], None, None, None],
    [13, 'Stick', 1.25, True, ['m_axe'], None, None, None],
    [14, 'Log X', 10, [[6], 1, [1], [6], [1], [1], [1], 0], ['m_axe'], None, None, 5],
    [15, 'Wooden Pickaxe', 10, None, ['can_break_pick_1', 'picks', 'noplace', 'wooden_tools', 'tools'], None, None, None],
    [16, 'Wooden Sword', 7.5, None, ['swords', 'noplace', 'wooden_tools', 'tools'], None, None, None],
    [17, 'Wooden Axe', 10, None, ['axes', 'noplace', 'wooden_tools', 'tools'], None, None, None],
    [18, 'Wooden Shovel', 5, None, ['shovels', 'noplace', 'wooden_tools', 'tools'], None, None, None],
    [19, 'Wooden Hoe', 7.5, None, ['hoes', 'wooden_tools', 'noplace', 'tools'], None, None, None],
    [20, 'Wooden Planks', 2.5, True, ['m_axe'], None, None, None],
    [21, 'Generator1', 0, None, ['unbreakable'], None, None, None],
    [22, 'Generator2', 0, None, ['unbreakable'], None, None, None],
    [23, 'Generator3', 0, None, ['unbreakable'], None, None, None],
    [24, 'Generator4', 0, None, ['unbreakable'], None, None, None],
    [25, 'Stone', 10, True, ['requires_pick_1', 'm_pick'], None, None, None],
    [26, 'Coal Ore', 20, [[30], 1, [1, 2, 3], [26], [1, 2, 3, 3], [1, 2, 3, 3, 4], [2, 3, 4, 4, 5], 2], ['requires_pick_1', 'm_pick'], None, None, None],
    [27, 'Iron Ore', 40, [[31], 1, [1], [27], [1, 1, 2], [1, 2, 2], [2, 3, 3], 0], ['requires_pick_2', 'm_pick'], None, None, None],
    [28, 'Gold Ore', 60, [[32], 1, [1], [28], [1, 1, 2], [1, 2, 2], [2, 3, 3], 0], ['requires_pick_3', 'm_pick'], None, None, None],
    [29, 'Diamond Ore', 140, [[35], 1, [1], [29], [1, 1, 2], [1, 2, 2], [2, 3, 3], 10], ['requires_pick_3', 'm_pick'], None, None, None],
    [30, 'Coal', 10, None, ['noplace'], None, None, None],
    [31, 'Raw Iron', 40, None, ['noplace'], None, None, None],
    [32, 'Raw Gold', 60, None, ['noplace'], None, None, None],
    [33, 'Iron Ingot', 45, None, ['noplace'], None, None, None],
    [34, 'Gold Ingot', 67.5, None, ['noplace'], None, None, None],
    [35, 'Diamond', 140, None, ['noplace'], None, None, None],
    [36, 'Copper Ore', 30, [[37], 1, [1, 2, 3], [36], [1, 2, 3, 3], [1, 2, 3, 3, 4], [2, 3, 4, 4, 5], 0], ['requires_pick_1', 'm_pick'], None, None, None],
    [37, 'Raw Copper', 15, None, ['noplace'], None, None, None],
    [38, 'Copper Ingot', 17.5, None, ['noplace'], None, None, None],
    [39, 'Block of Coal', 90, True, ['requires_pick_1', 'm_pick'], None, None, None],
    [40, 'Block of Iron', 405, True, ['requires_pick_2', 'm_pick'], None, None, None],
    [41, 'Block of Gold', 607.5, True, ['requires_pick_3', 'm_pick'], None, None, None],
    [42, 'Block of Diamond', 1260, True, ['requires_pick_3', 'm_pick'], None, None, None],
    [43, 'Block of Copper', 157.5, True, ['requires_pick_1', 'm_pick'], None, None, None],
    [44, 'Fuel', 1, None, ['noplace'], None, None, None],
    [45, 'Copper Pickaxe', 55, None, ['noplace', 'copper_tools', 'picks', 'tools', 'can_break_pick_1', 'can_break_pick_2'], None, None, None],
    [46, 'Copper Sword', 53.75, None, ['noplace', 'copper_tools', 'swords', 'tools'], None, None, None],
    [47, 'Copper Axe', 55, None, ['noplace', 'copper_tools', 'axes', 'tools'], None, None, None],
    [48, 'Copper Shovel', 20, None, ['noplace', 'copper_tools', 'shovels', 'tools'], None, None, None],
    [49, 'Copper Hoe', 37.5, None, ['noplace', 'copper_tools', 'hoes', 'tools'], None, None, None],
    [50, 'Iron Pickaxe', 137.5, None, ['noplace', 'iron_tools', 'picks', 'tools', 'can_break_pick_1', 'can_break_pick_2', 'can_break_pick_3'], None, None, None],
    [51, 'Iron Sword', 91.25, None, ['noplace', 'iron_tools', 'swords', 'tools'], None, None, None],
    [52, 'Iron Axe', 137.5, None, ['noplace', 'iron_tools', 'axes', 'tools'], None, None, None],
    [53, 'Iron Shovel', 47.5, None, ['noplace', 'iron_tools', 'shovels', 'tools'], None, None, None],
    [54, 'Iron Hoe', 92.5, None, ['noplace', 'iron_tools', 'hoes', 'tools'], None, None, None],
    [55, 'Diamond Pickaxe', 302.5, None, ['noplace', 'diamond_tools', 'picks', 'tools', 'can_break_pick_1', 'can_break_pick_2', 'can_break_pick_3', 'can_break_pick_4'], None, None, None],
    [56, 'Diamond Sword', 201.5, None, ['noplace', 'diamond_tools', 'swords', 'tools'], None, None, None],
    [57, 'Diamond Axe', 302.5, None, ['noplace', 'diamond_tools', 'axes', 'tools'], None, None, None],
    [58, 'Diamond Shovel', 102.75, None, ['noplace', 'diamond_tools', 'shovels', 'tools'], None, None, None],
    [59, 'Diamond Hoe', 202.75, None, ['noplace', 'diamond_tools', 'hoes', 'tools'], None, None, None],
    [60, 'Lapis Lazuli Ore', 50, [[61], 1, [1, 2, 2, 3, 3], [60], [2, 2, 3, 3], [2, 3, 3], [3], 3], ['requires_pick_2', 'm_pick'], None, None, None],
    [61, 'Lapis Lazuli', 20, None, ['noplace'], None, None, None],
    [62, 'Block of Lapis Lazuli', 180, True, ['requires_pick_2', 'm_pick'], None, None, None],
    [63, 'Water', 0, None, [], None, None, None],
    [64, 'Bucket', 135, None, [], None, None, None],
    [65, 'Bucket of Water', 150, None, [], None, None, None],
    [66, 'Farmland', 0, [[3], 1, [1], [3], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [67, 'Wet Farmland', 0, [[3], 1, [1], [3], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [68, 'Wheat', 10, None, ['noplace'], None, None, None],
    [69, 'Seeds', 2, [[69], 67, [1], [69], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [70, 'Wheat1', 0, [[69], 67, [1], [69], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [71, 'Wheat2', 0, [[69], 67, [1], [69], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [72, 'Wheat3', 0, [[69], 67, [1], [69], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [73, 'Wheat4', 0, [[69], 67, [1], [69], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [74, 'Wheats', 0, [[69, 69, 68], 67, [2, 3], [69, 68], [2, 3, 3], [2, 3, 3, 4], [3, 4, 4, 5], 1], ['m_shovel'], None, None, None],
    [75, 'Potato', 10, [[75], 67, [1], [75], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [76, 'Potato1', 0, [[75], 67, [1], [75], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [77, 'Potatoes', 0, [[75], 67, [2, 3], [75], [2, 3, 4], [3, 4, 5], [4, 5, 6], 1], ['m_shovel'], None, None, None],
    [78, 'Carrot', 10, [[78], 67, [1], [78], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [79, 'Carrot1', 0, [[78], 67, [1], [78], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [80, 'Carrot2', 0, [[78], 67, [1], [78], [1], [1], [1], 0], ['m_shovel'], None, None, None],
    [81, 'Carrots', 0, [[78], 67, [2, 3], [78], [2, 3, 4], [3, 4, 5], [4, 5, 6], 1], ['m_shovel'], None, None, None],
    [82, 'Bread', 30, None, ['noplace'], None, None, None],
    [83, 'Emerald Ore', 120, [[84], 1, [1], [83], [1, 1, 2], [1, 2, 2], [2, 3, 3], 10], ['requires_pick_3', 'm_pick'], None, None, None],
    [84, 'Emerald', 120, None, ['noplace'], None, None, None],
    [85, 'Redstone Ore', 100, [[86], 1, [1, 2, 2, 3, 3], [85], [2, 2, 3, 3], [2, 3, 3], [3], 3], ['requires_pick_3', 'm_pick'], None, None, None],
    [86, 'Redstone Dust', 40, None, ['noplace'], None, None, None],
    [87, 'Deepslate', 20, True, ['requires_pick_1', 'm_pick'], None, None, None],
    [88, 'Deepslate Coal Ore', 40, [[30], 1, [1, 2, 3], [88], [1, 2, 3, 3], [1, 2, 3, 3, 4], [2, 3, 4, 4, 5], 2], ['requires_pick_1', 'm_pick'], None, None, None],
    [89, 'Deepslate Iron Ore', 80, [[31], 1, [1], [89], [1, 1, 2], [1, 2, 2], [2, 3, 3], 0], ['requires_pick_2', 'm_pick'], None, None, None],
    [90, 'Deepslate Copper Ore', 60, [[37], 1, [1, 2, 3], [90], [1, 2, 3, 3], [1, 2, 3, 3, 4], [2, 3, 4, 4, 5], 0], ['requires_pick_1', 'm_pick'], None, None, None],
    [91, 'Deepslate Gold Ore', 120, [[32], 1, [1], [91], [1, 1, 2], [1, 2, 2], [2, 3, 3], 0], ['requires_pick_3', 'm_pick'], None, None, None],
    [92, 'Deepslate Emerald Ore', 240, [[84], 1, [1], [92], [1, 1, 2], [1, 2, 2], [2, 3, 3], 10], ['requires_pick_3', 'm_pick'], None, None, None],
    [93, 'Deepslate Redstone Ore', 200, [[86], 1, [1, 2, 2, 3, 3], [93], [2, 2, 3, 3], [2, 3, 3], [3], 3], ['requires_pick_3', 'm_pick'], None, None, None],
    [94, 'Deepslate Diamond Ore', 280, [[35], 1, [1], [94], [1, 1, 2], [1, 2, 2], [2, 3, 3], 10], ['requires_pick_3', 'm_pick'], None, None, None],
    [95, 'Deepslate Lapis Lazuli Ore', 100, [[61], 1, [1, 2, 2, 3, 3], [95], [2, 2, 3, 3], [2, 3, 3], [3], 3], ['requires_pick_2', 'm_pick'], None, None, None],
    [96, 'Block of Redstone', 360, True, ['requires_pick_3', 'm_pick'], None, None, None],
    [97, 'Block of Emerald', 1080, True, ['requires_pick_3', 'm_pick'], None, None, None],
    [98, 'Mycelium', 5, True, ['m_shovel'], None, None, None],
    [99, 'Mushroom Stem', 5, True, ['m_shovel'], None, None, None],
    [100, 'Red Mushroom Block', 5, True, ['m_shovel'], None, None, None],
    [101, 'Brown Mushroom Block', 5, True, ['m_shovel'], None, None, None],
    [102, 'Red Mushroom', 5, [[102], 98, [1], [102], [1], [1], [1], 0], [], None, None, None],
    [103, 'Brown Mushroom', 5, [[103], 99, [1], [102], [1], [1], [1], 0], [], None, None, None],
    [104, 'Netherrack', 5, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [105, 'Glowstone', 5, [[106], 1, [1, 2, 3, 3, 4, 4], [105], [1], [1], [1], 0], ['m_pick', 'requires_pick_1'], None, None, None],
    [106, 'Glowstone Dust', 2.8, None, ['noplace'], None, None, None],
    [107, 'Soul Sand', 5, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [108, 'Soul Soil', 5, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [109, 'Gravel', 5, [[109] * 15 + [110], 1, [1], [109], [1], [1], [1]], [], None, None, None],
    [110, 'Flint', 45, True, ['noplace'], None, None, None],
    [111, 'Flint and Steel', 90, True, ['tools'], None, None, None],
    [112, 'Clay', 5, True, ['m_shovel'], None, None, None],
    [113, 'Sand', 5, True, ['m_shovel'], None, None, None],
    [114, 'Mud', 5, True, ['m_shovel'], None, None, None],
    [115, 'Snow Block', 5, True, ['m_shovel'], None, None, None],
    [116, 'Snowball', 1.25, None, ['noplace'], None, None, None],
    [117, 'Ice', 1, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [118, 'Packed Ice', 9, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [119, 'Blue Ice', 81, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [120, 'Smooth Stone', 10, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [121, 'Stone Bricks', 10, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [122, 'Cracked Stone Bricks', 10, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [123, 'Mossy Stone Bricks', 10, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [124, 'Chiseled Stone Bricks', 10, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [125, 'Granite', 10, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [126, 'Polished Granite', 10, True, ['m_pick', 'requires_pick_1'], None, None, None],
    [127, 'Diorite', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [128, 'Polished Diorite', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [129, 'Andesite', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [130, 'Polished Andesite', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [131, 'Basalt', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [132, 'Polished Basalt', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [133, 'Smooth Basalt', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [134, 'Blackstone', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [135, 'Polished Blackstone', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [136, 'Chiseled Polished Blackstone', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [137, 'Polished Blackstone Bricks', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [138, 'Cracked Polished Blackstone Bricks', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [139, 'Gilded Blackstone', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [140, 'Red Sand', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [141, 'Nether Quartz Ore', 10, [[142], 1, [1], [141], [2], [3], [4]], ['m_pick', 'requires_pick_1'], None, None],
    [142, 'Nether Quartz', 10, None, ['noplace'], None, None],
    [143, 'Nether Gold Ore', 10, [[144], 1, [2, 3, 4, 5], [144], [3, 4, 5], [4, 5, 6], [5, 6, 7]], ['m_pick', 'requires_pick_1'], None, None],
    [144, 'Gold Nugget', 10, None, ['noplace'], None, None],
    [145, 'Iron Nugget', 10, None, ['noplace'], None, None],
    [146, 'Deepslate Bricks', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [147, 'Cracked Deepslate Bricks', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [148, 'Deepslate Tiles', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [149, 'Cracked Deepslate Tiles', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [150, 'Polished Deepslate', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [151, 'Chiseled Deepslate', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [152, 'Calcite', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [153, 'Tuff', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [154, 'Obsidian', 10, True, ['m_pick', 'requires_pick_4'], None, None],
    [155, 'Crying Obsidian', 10, True, ['m_pick', 'requires_pick_4'], None, None],
    [156, 'Ancient Debris', 500, True, ['m_pick', 'requires_pick_4'], None, None],
    [157, 'Netherite Scrap', 600, None, ['noplace'], None, None],
    [158, 'Netherite Ingot', 2500, None, ['noplace'], None, None],
    [159, 'Block of Netherite', 22500, True, ['m_pick', 'requires_pick_4'], None, None],
    [160, 'Netherite Pickaxe', 7500, None, ['noplace', 'tools', 'netherite_tools', 'picks', 'can_break_pick_1', 'can_break_pick_2', 'can_break_pick_3', 'can_break_pick_4'], None, None],
    [161, 'Netherite Sword', 5000, None, ['noplace', 'tools', 'netherite_tools', 'swords'], None, None],
    [162, 'Netherite Axe', 7500, None, ['noplace', 'tools', 'netherite_tools', 'axes'], None, None],
    [163, 'Netherite Shovel', 2500, None, ['noplace', 'tools', 'netherite_tools', 'shovels'], None, None],
    [164, 'Netherite Hoe', 5000, None, ['noplace', 'tools', 'netherite_tools', 'hoes'], None, None],
    [165, 'Block of Amethyst', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [166, 'Block of Quartz', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [167, 'Smooth Quartz', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [168, 'Quartz Pillar', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [169, 'Chiseled Quartz', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [170, 'Quartz Bricks', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [171, 'Sandstone', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [172, 'Cut Sandstone', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [173, 'Chiseled Sandstone', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [174, 'Red Sandstone', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [175, 'Cut Red Sandstone', 10, True, ['m_pick', 'requires_pick_1'], None, None],
    [176, 'Chiseled Red Sandstone', 10, True, ['m_pick', 'requires_pick_1'], None, None],
]

generator = [
    [0, [2], 'gb-plains', 'Plains'],
    [1, [25] * 50 + [125, 127, 129] * 4 + [36] * 5 + [26] * 4 + [27] * 3 + [28] * 2 + [85, 85, 83, 29], 'gb-caves1', 'Upper Caves'],
    [2, [87] * 50 + [89, 90] * 5 + [91, 93, 95, 153] * 3 + [94, 94, 88, 92], 'gb-caves2', 'Lower Caves'],
    [5, [98, 98, 98, 99, 100, 101, 102, 103], 'gb-mfields', 'Mushroom Fields'],
    [3, [104, 104, 104, 104, 104, 104, 105, 107, 107, 108, 109, 109] * 200 + [156], 'gb-netherw', 'Nether Wastes'],
    [2, [115] * 20 + [117] * 5 + [118] * 3 + [119], 'gb-snowb', 'Snowy Beach'],
    [1, [109, 112, 113, 114] * 10 + [139], 'gb-oceanf', 'Ocean Floor'],
    [3, [132, 133, 133] * 400 + [156], 'gb-bdelta', 'Basalt Deltas'],
    [2, [152, 133, 165], 'gb-geode', 'Amethyst Geode'],
    [3, [107, 108, 156] * 400 + [156], 'gb-ssvall', 'Soul Sand Valley'],
    [6, [134, 135, 136, 137, 138] * 9 + [139] * 3 + [41], 'gb-bastion', 'Bastion'],
]

nature_recipes = [
    [[[1, 6]], [4, 20]],
    [[[2, 20]], [4, 13]],
    [[[9, 117]], [1, 118]],
    [[[9, 118]], [1, 119]],
]

stone_recipes = [
    [[[1, 25]], [1, 120]],
    [[[1, 25]], [1, 121]],
    [[[1, 25]], [1, 122]],
    [[[1, 25]], [1, 123]],
    [[[1, 25]], [1, 124]],
    [[[1, 120]], [1, 25]],
    [[[1, 121]], [1, 25]],
    [[[1, 122]], [1, 25]],
    [[[1, 123]], [1, 25]],
    [[[1, 124]], [1, 25]],
    [[[1, 125]], [1, 126]],
    [[[1, 127]], [1, 128]],
    [[[1, 129]], [1, 130]],
    [[[1, 126]], [1, 125]],
    [[[1, 128]], [1, 127]],
    [[[1, 130]], [1, 129]],
    [[[1, 131]], [1, 132]],
    [[[1, 131]], [1, 133]],
    [[[1, 132]], [1, 131]],
    [[[1, 133]], [1, 131]],
    [[[4, 142]], [1, 166]],
    [[[1, 166]], [1, 167]],
    [[[1, 166]], [1, 168]],
    [[[1, 166]], [1, 169]],
    [[[1, 169]], [1, 170]],
    [[[1, 167]], [1, 166]],
    [[[1, 168]], [1, 166]],
    [[[1, 169]], [1, 166]],
    [[[1, 170]], [1, 166]],
    [[[1, 113]], [1, 171]],
    [[[1, 171]], [1, 172]],
    [[[1, 171]], [1, 173]],
    [[[1, 172]], [1, 171]],
    [[[1, 173]], [1, 171]],
    [[[1, 140]], [1, 174]],
    [[[1, 174]], [1, 175]],
    [[[1, 174]], [1, 176]],
    [[[1, 175]], [1, 174]],
    [[[1, 176]], [1, 174]],
    [[[9, 30]], [1, 39]],
    [[[9, 33]], [1, 40]],
    [[[9, 34]], [1, 41]],
    [[[9, 35]], [1, 42]],
    [[[9, 38]], [1, 43]],
    [[[9, 86]], [1, 96]],
    [[[9, 84]], [1, 95]],
    [[[1, 39]], [9, 30]],
    [[[1, 40]], [9, 33]],
    [[[1, 41]], [9, 34]],
    [[[1, 42]], [9, 35]],
    [[[1, 43]], [9, 38]],
    [[[1, 96]], [9, 86]],
    [[[1, 95]], [9, 84]],
    [[[9, 158]], [1, 159]],
    [[[1, 159]], [9, 158]],
    [[[1, 33]], [9, 145]],
    [[[1, 34]], [9, 144]],
    [[[4, 157], [4, 34]], [1, 158]],
    [[[9, 145]], [1, 33]],
    [[[9, 144]], [1, 34]],
    [[[1, 134]], [1, 135]],
    [[[1, 135]], [1, 134]],
    [[[1, 135]], [1, 136]],
    [[[1, 136]], [1, 135]],
    [[[1, 135]], [1, 137]],
    [[[1, 137]], [1, 135]],
    [[[1, 137]], [1, 138]],
    [[[1, 138]], [1, 137]],
    [[[1, 87]], [1, 146]],
    [[[1, 146]], [1, 87]],
    [[[1, 146]], [1, 147]],
    [[[1, 147]], [1, 146]],
    [[[1, 87]], [1, 148]],
    [[[1, 148]], [1, 87]],
    [[[1, 148]], [1, 149]],
    [[[1, 149]], [1, 148]],
    [[[1, 87]], [1, 150]],
    [[[1, 150]], [1, 87]],
    [[[1, 87]], [1, 151]],
    [[[1, 151]], [1, 87]],
]

nether_recipes = [
    [[[4, 106]], [1, 105]],
]

tools_recipes = [
    [[[2, 13], [3, 20]], [1, 15]],
    [[[1, 13], [2, 20]], [1, 16]],
    [[[2, 13], [3, 20]], [1, 17]],
    [[[2, 13], [1, 20]], [1, 18]],
    [[[2, 13], [2, 20]], [1, 19]],
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
    [[[3, 33]], [1, 64]],
    [[[2, 13], [3, 158]], [1, 160]],
    [[[1, 13], [2, 158]], [1, 161]],
    [[[2, 13], [3, 158]], [1, 162]],
    [[[2, 13], [1, 158]], [1, 163]],
    [[[2, 13], [2, 158]], [1, 164]],
]

other_recipes = []

food_recipes = [
    [[[3, 68]], [1, 82]],
]

fuel_recipes = [
    [[[1, 30]], [8, 44]], 
]

smelt_recipes = [
    [[1, 37], [1, 38], 5],
    [[1, 31], [1, 33], 5],
    [[1, 32], [1, 34], 5],
    [[1, 156], [1, 157], 100],
]

recipe_data_vars = [[nature_recipes, '-nature'], [stone_recipes, '-stone'], \
                   [nether_recipes, '-nether'], [tools_recipes, '-tools'], \
                   [other_recipes, '-other'], [food_recipes, '-food'], \
                   [fuel_recipes, '-fuel']]

base_tiles = [[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]]

moons = ['New Moon', 'Waxing Crescent', 'Waxing Half', 'Waxing Gibbous', \
         'Full Moon', 'Waning Gibbous', 'Waning Half', 'Waning Crescent']
rare_moons = ['Harvest Moon', 'Blue Moon', 'Supermoon', 'Super Blood Moon', 'Pork Moon', 'Dire Moon', \
              'Bloodstained Moon', 'Lunar Eclipse', 'Minmus Mun']
very_rare_moons = ['Total Solar Eclipse', 'Nightmare Moon']

shop = [
    ['Layer above', '<span id="lprice-1"></span>', 'buy_layer_above'],
    ['Layer below', '<span id="lprice-2"></span>', 'buy_layer_below'],
    ['Bucket -&GT; Water Bucket', '$45', 'buy_wb'],
    ['Seeds', '$100', 'buy_seeds'],
    ['Potato', '$100', 'buy_potato'],
    ['Carrot', '$100', 'buy_carrot'],
    ['Grass Block', '100', 'buy_grass_block'],
    ['<span id="rtsinfo"></span>', '<span id="rtsprice"></span>', 'buy_rts'],
    ['Unlock avatar', '$25,000', 'buy_servant'],
    ['1ǥ', '$1,000', 'buy_gen_money']
]

saved_vars = ['all_tiles', 'inventory', 'money', 'layer_price', 'z', \
              'l_offset', 'stats', 'xp', 'levels', 'rts', \
              'servant_inv', 'servant_break', 'servant_place', 'servant_sell', \
              'has_servant', 'servant_layers', 'game_time', 'gen_money', \
              'gen_mode', 'has_gens', 'game_seed', 'mods', 'nl']

# Makes item properties more accessible to the code
names = {x[0]: x[1] for x in items}
rnames = {v: k for k, v in names.items()}
prices = {x[0]: x[2] for x in items}
loot_table = {x[0]: x[3] for x in items if x[3] != None}
for x in dict(loot_table):
    if loot_table[x] == True:
        loot_table[x] = [[int(x)], 1, [1], [int(x)], [1], [1], [1], 0]
tags = {}
for k, v in {x[0]: x[4] for x in items}.items():
    for x in v:
        tags.setdefault(x,[]).append(k)

# Utility functions

# Checks if something is breakable and reduces durability
def break_block(c, inventory, d=False):
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
    elif c in tags['requires_pick_1'] and \
         item not in tags['can_break_pick_1']:
        return None
    elif c in tags['requires_pick_2'] and \
         item not in tags['can_break_pick_2']:
        return None
    elif c in tags['requires_pick_3'] and \
         item not in tags['can_break_pick_3']:
        return None
    elif c in tags['requires_pick_4'] and \
         item not in tags['can_break_pick_4']:
        return None
    elif c == 63 and item != 64:
        return False
    else:
        try:
            meta = inventory[item][1]
        except KeyError:
            return True
        m = 1
        if d == False:
            d = 0
            if item in tags['wooden_tools']:
                d += 1/64
            elif item in tags['copper_tools']:
                d += 1/128
            elif item in tags['iron_tools']:
                d += 1/384
            elif item in tags['diamond_tools']:
                d += 1/1024
            elif item in tags['netherite_tools']:
                d += 1/2048
            elif item == 111:
                d += 1/64
            if (item in tags['picks'] and c not in tags['m_pick']) or \
               (item in tags['axes'] and c not in tags['m_axe']) or \
               (item in tags['shovels'] and c not in tags['m_shovel']) or \
               (item in tags['swords'] and c not in tags['m_sword']) or \
               (item in tags['hoes'] and c not in tags['m_hoe']):
                d *= 2
            inventory[item][1] -= d
            if item in tags['tools']:
                if inventory[item][1] <= 0:
                    del inventory[item]
                    return None
        return True

# Checks if you can place a block
def can_place(x, y):
    global tags
    if x == 4: 
        return y == 2
    elif x in [102, 103]:
        return y == 98
    elif x in tags['noplace']:
        return False
    elif x in [69, 75, 78]:
        return y == 67
    elif y == 63:
        return can_place(x, 1)
    else:
        return y == 1

# Format an item for display
def format_item(i):
    global tags
    item = i[0]
    durability = i[1][1]
    if item in tags['tools']:
        a = ' (' + str(round(durability*100, 1)) + '%)'
    else:
        a = ''
    return f'{i[1][0]}x {names[i[0]]}' + a

# Display an image
def set_img(x, y, new):
    if items[new][5] != None:
        path = items[new][5]
    else:
        path = f'https://2dskyblock.github.io/assets/{new}.png'
    document[str(y) + '-' + str(x)].attrs['src'] = path

# Copied from Lib/tkinter/__init__.py
def flatten(x):
    res = []
    for item in x:
        if isinstance(item, [tuple, list]):
            res += flatten(item)
        else:
            res.append(item)
    return res

# Display statistics
def display_stats():
    global stats, alert, flatten, prices, all_tiles
    at2 = flatten(all_tiles)
    isv = '{:,.2f}'.format(float(str(sum([prices.get(x, 0) for x in at2]))))
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

# Load a save
def load_save_old(x):
    global all_tiles, inventory, sel, money, layer_price, z, l_offset, \
           gen_level, stats, xp, levels, rts, servant_inv, servant_break, \
           servant_place, servant_sell, has_servant, servant_layers, \
           game_time, gen_money, gen_mode, has_gens, game_seed
    try:
        x = x.encode('latin-1')
        x = base64.b64decode(x + b'=' * (-len(x) % 4)).decode('latin-1')
        y = ''
        x = 'x' + x
        for i, b in enumerate(x[1:]):
            y += chr((sha('techno never dies' + x[i] + str(i)) % 256) ^ ord(b))
        load = eval(y.encode('latin-1').decode('utf-8'))
        if load == None:
            return
        ver = load[0]
        if ver > 5:
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
            has_gens = load[20]
            gen_mode = load[21]
            gen_money = load[22]
            game_seed = load[23]
    except KeyError:
        pass
    except Exception as e:
        alert(f'Invalid save! ({str(e)})')
def load_save(save):
    if not save.startswith('$'):
        load_save_old(save)
        return None
    try:
        save = save[1:].encode('latin-1')
        save = base64.b64decode(save + b'=' * (-len(save) % 4))
        save = zlib.decompress(save)
        save = save.decode('utf-8')
        save = eval(save, globals())
        for x in save:
            globals()[x] = eval(save[x], globals())
        # Post-load
        global tiles, all_tiles, has_servant, has_gens, z
        tiles = all_tiles[z]
        if has_servant:
            del document['servant-upgrade']
        for x in has_gens:
            document[generator[x][2]].unbind('click')
            document[generator[x][2]].bind('click', get_gen_shop_sel(x))
            document[generator[x][2]].innerHTML = 'Select'
    except ZeroDivisionError:
        pass
    except Exception as e:
        alert(f'Invalid save! ({str(e)})')

# Get a save
def _save():
    o = {}
    for x in saved_vars:
        o[x] = repr(eval(x, globals()))
    o = repr(o)
    o = o.encode('utf-8')
    o = zlib.compress(o)
    o = base64.b64encode(o).decode('latin-1')
    return '$' + o

# Add a layer
def add_layer(down=False):
    global all_tiles, base_tiles, z, l_offset
    if down:
        all_tiles = [[[int(a) for a in b] for b in base_tiles],] + all_tiles
        z += 1
        l_offset += 1
    else:
        all_tiles.append([[int(a) for a in b] for b in base_tiles])

# Hide all the sub-screens
def hide_all():
    document['crafting'].style.display = 'none'
    document['upgrades'].style.display = 'none'
    document['gen'].style.display = 'none'
    document['slscreen'].style.display = 'none'
    document['servantm'].style.display = 'none'
    document['game'].style.display = 'none'

def _load_mod(req, url, say_name=True):
    global mods
    if req.status not in (200, 0):
        alert(f'Mod cannot be retrieved (Error code {req.status})')
        return
    text = req.text
    text = text.split('\n')
    header = json.loads(text[0])
    code = text[1]
    if 'min-version' not in header or 'max-version' not in header:
        alert('Invalid mod! (Error code 1)')
        return
    min_version = header['min-version']
    max_version = header['max-version']
    if type(min_version) != int or type(max_version) != int:
        if not input('This mod may not work. Are you sure you want to load it?'):
            return
    elif min_version > max_version:
        alert('Invalid mod! (Error code 1)')
        return
    elif min_version > version_number or max_version < version_number:
        alert('Invalid mod! (Error code 3)')
        return
    if 'name' not in header:
        alert('Invalid mod! (Error code 4)')
        return
    name = header['name']
    try:
        exec(code, globals(), {})
        if name not in mods:
            mods[name] = url
        if say_name:
            alert(f'The mod\'s name is "{name}"') 
    except Exception as e:
        alert('Invalid mod! (Error code 5)')
def load_mod(url, say_name=True):
    req = ajax.ajax()
    req.bind('complete', lambda x: _load_mod(x, url, say_name))
    req.open('GET', url+f'?nonce={randint(2**64)}', True)
    req.send()
def unload_mod(name):
    global mods
    try:
        del mods[name]
    except KeyError:
        alert('Invalid mod name')
def user_add_mod():
    load_mod(input('Enter mod url to add:'))
def user_list_mods():
    if len(mods) != 0:
        alert('Loaded mods: ' + ', '.join(list(mods.keys())))
    else:
        alert('There are no loaded mods')
def user_del_mod():
    unload_mod(input('Enter mod name to remove:'))

# Button functions

# Get click handlers for images
def get_handle_click(x, y):
    def handle_click(_event):
        global inventory
        click_bind(x, y, inventory)
    return handle_click

# Generator selection button
def get_gen_shop_sel(n):
    def gen_shop_sel(_ev):
        global gen_mode
        gen_mode = int(n)
    return gen_shop_sel

# Generator buying button
def get_gen_shop_buy(n, gb):
    def gen_shop_buy(_ev):
        global has_gens, gen_mode, generator, gen_money
        if generator[n][0] > gen_money:
            alert('You don\'t have enough ǥ!')
        else:
            gen_money -= generator[n][0]
            has_gens.append(n)
            document[gb].unbind('click')
            document[gb].bind('click', get_gen_shop_sel(n))
            document[gb].innerHTML = 'Select'
    return gen_shop_buy

# Shop buy buttons
def buy_layer_above(_ev):
    global money, layer_price, stats
    if money >= layer_price:
        stats[6] += 1
        stats[4] += 1
        stats[9] += layer_price
        money -= layer_price
        add_layer()
        layer_price *= 3
    else:
        alert('Not enough money!')
def buy_layer_below(_ev):
    global money, layer_price, stats
    if money >= layer_price:
        stats[6] += 1
        stats[4] += 1
        stats[9] += layer_price
        money -= layer_price
        add_layer(True)
        layer_price *= 3
    else:
        alert('Not enough money!')
def buy_wb(_ev):
    global inventory, money, stats
    if 64 in inventory and inventory[64][0] > 0:
        if money >= 45:
            stats[6] += 1
            money -= 45
            inventory[64][0] -= 1
            if 65 not in inventory:
                inventory[65] = [1, 0]
            else:
                inventory[65][0] += 1
        else:
            alert('Not enough money!')
    else:
        alert('You need an empty bucket!')
def buy_seeds(_ev):
    global money, stats, inventory
    if money >= 100:
        stats[6] += 1
        money -= 100
        if 69 not in inventory:
            inventory[69] = [1, 0]
        else:
            inventory[69][0] += 1
    else:
        alert('Not enough money!')
def buy_potato(_ev):
    global money, stats, inventory
    if money >= 100:
        stats[6] += 1
        money -= 100
        if 75 not in inventory:
            inventory[75] = [1, 0]
        else:
            inventory[75][0] += 1
    else:
        alert('Not enough money!')
def buy_carrot(_ev):
    global money, stats, inventory
    if money >= 100:
        stats[6] += 1
        money -= 100
        if 78 not in inventory:
            inventory[78] = [1, 0]
        else:
            inventory[78][0] += 1
    else:
        alert('Not enough money!')
def buy_grass_block(_ev):
    global money, stats, inventory
    if money >= 100:
        stats[6] += 1
        money -= 100
        if 2 not in inventory:
            inventory[2] = [1, 0]
        else:
            inventory[2][0] += 1
    else:
        alert('Not enough money!')
def buy_rts(_ev):
    global rts, money, stats
    rtp = int(1.005**((4*rts-3)*(100**(((4*rts-3)%10)/10+1))))
    if money >= rtp:
        money -= rtp
        stats[6] += 1
        rts += 0.25
    else:
        alert('Not enough money!')
def buy_servant(_ev):
    global has_servant, stats, money
    if money >= 25000:
        money -= 25000
        has_servant = True
        del document['servant-upgrade']
        stats[6] += 1
    else:
        alert('Not enough money!')
def buy_gen_money(_ev):
    global money, stats, gen_money
    if money >= 1000:
        money -= 1000
        stats[6] += 1
        gen_money += 1
    else:
        alert('Not enough money!')

# Avatar add layer button
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

# Avatar remove layer button
def servant_remove_layer(_ev):
    global servant_layers
    x = input('Enter layer:')
    if x not in [str(y) for y in servant_layers]:
        alert('Invalid layer!')
    else:
        del servant_layers[servant_layers.index(int(x))]

# Avatar add break button
def servant_add_break(_ev):
    global servant_break, rnames, tags
    it = input('Enter block:')
    if it not in rnames:
        alert('Invalid block!')
    elif rnames[it] in tags['noplace']:
        alert('Invalid block!')
    else:
        servant_break.append(rnames[it])

# Avatar remove break button
def servant_remove_break(_ev):
    global servant_break, rnames
    it = input('Enter block:')
    if it not in rnames:
        alert('Invalid block!')
    elif rnames[it] not in servant_break:
        alert('Invalid block!')
    else:
        del servant_break[rnames[it]]

# Avatar add place button
def servant_add_place(_ev):
    global servant_place, rnames
    it = input('Enter block:')
    if it not in rnames:
        alert('Invalid block!')
    elif rnames[it] in tags['noplace']:
        alert('Invalid block!')
    else:
        servant_place.append(rnames[it])

# Avatar remove place button
def servant_remove_place(_ev):
    global servant_place, rnames
    it = input('Enter block:')
    if it not in rnames:
        alert('Invalid block!')
    elif rnames[it] not in servant_place:
        alert('Invalid block!')
    else:
        del servant_place[rnames[it]]

# Avatar add sell button
def servant_add_sell(_ev):
    global servant_sell, rnames
    it = input('Enter item:')
    if it not in rnames:
        alert('Invalid item!')
    else:
        servant_sell.append(rnames[it])

# Avatar remove sell button
def servant_remove_sell(_ev):
    global servant_sell
    it = input('Enter item:')
    if it not in rnames:
        alert('Invalid item')
    elif rnames[it] not in servant_sell:
        alert('Invalid item!')
    else:
        del servant_sell[it]

# Crafting button bind
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

# Crafting tab bind
def get_craft_switch(to, nto):
    def craft_switch(_ev):
        global document
        document[to].style.display = 'inline'
        for x in nto:
            document[x].style.display = 'none'
    return craft_switch

# Smelting button bind
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

# Back button
def back_btn(_ev):
    hide_all()
    document['game'].style.display = 'inline'
    b_show = False
    c_show = False
    servant_shop = False
    gen_shop = False
    show_upgrade = False

# Up button
def button_up_layer(_ev):
    global z, all_tiles
    if z != len(all_tiles) - 1:
        z += 1

# Down button
def button_down_layer(_ev):
    global z
    if z != 0:
        z -= 1

# Inventory scroll buttons
def button_up_inv(_ev):
    global inventory, sel
    inventory.move_to_end(tuple(inventory)[0])
    sel = tuple(inventory)[0]
def button_down_inv(_ev):
    global inventory, sel
    for _ in range(len(inventory) - 1):
        inventory.move_to_end(tuple(inventory)[0])
    sel = tuple(inventory)[0]

# Save button
def button_save(_ev):
    storage[storage_key] = _save()

# Statistics button
def button_stats(_ev):
    display_stats()

# Crafting button
def button_craft(_ev):
    global document, c_show
    hide_all()
    document['crafting'].style.display = 'inline'
    c_show = True

def button_shop(_ev):
    global document, show_upgrade
    hide_all()
    document['upgrades'].style.display = 'inline'
    show_upgrade = True

def button_servant(_ev):
    global document, servant_shop, has_servant
    if has_servant:
        hide_all()
        document['servantm'].style.display = 'inline'
        servant_shop = True
    else:
        alert('You don\'t have an avatar!')

def button_gen(_ev):
    global document, gen_shop
    hide_all()
    document['gen'].style.display = 'inline'
    gen_shop = True

def button_backup(_ev):
    global document, b_show
    hide_all()
    document['slscreen'].style.display = 'inline'
    b_show = True

def button_sell(_ev):
    global money, inventory
    if len(inventory) != 0:
        return None
    i = tuple(inventory)[0]
    inventory[i][0] -= 1
    stats[8] += prices[i]
    if inventory[i][0] == 0:
        del inventory[i]
    money += prices[i]

def button_sell_all(_ev):
    global money, stats, inventory
    if len(inventory) != 0:
        return None
    i = tuple(inventory)[0]
    money += prices[i] * inventory[i][0]
    stats[8] += prices[i] * inventory[i][0]
    del inventory[i]

def button_slsave(_ev):
    document['sltxt'].value = _save()

def button_slload(_ev):
    load_save(document['sltxt'].value)
    
def button_rotate(_ev):
    global rotate_mode
    if rotate_mode == False:
        document['b-rotate'].innerHTML = 'Place/break mode'
        rotate_mode = True
    else:
        document['b-rotate'].innerHTML = 'Rotate mode'
        rotate_mode = False

# Main functions

# Avatar code
def servant_actions():
    global prices, servant_inv, money, servant_layers, servant_break, \
           servant_place, servant_sell, l_offset, all_tiles, inventory
    for layer in [x + l_offset - 1 for x in servant_layers]:
        servant_inv = OrderedDict({55:[1,1]})
        for x in range(18):
            for y in range(6):
                if all_tiles[layer][y][x] in servant_break:
                    all_tiles[layer], servant_inv, _ = click(\
                        x, y, all_tiles[layer], servant_inv, False)
        del servant_inv[55]
        if len(servant_inv) > 0:
            for x in range(18):
                for y in range(6):
                    its = [x for x in servant_place if x in tuple(servant_inv)]
                    shuffle(its)
                    for item in its:
                        servant_inv.move_to_end(item, last=False)
                        all_tiles[layer], servant_inv, mode = click(\
                            x, y, all_tiles[layer], servant_inv, True)
                        if mode == True:
                            break
        for k, v in servant_inv.items():
            if k in servant_sell:
                money += prices[k] * v[0]
            elif k not in inventory:
                inventory[k] = v
            else:
                inventory[k][0] += v[0]

# Main key handling
def handle_key(event):
    global money, inventory, prices, z, sel, storage, storage_key, tags, \
           servant_shop, gen_shop, show_upgrade
    key = event.keyCode
    if event.ctrlKey == True:
        return
    if key == 83 and event.altKey == True:
        storage[storage_key] = _save()
    elif key == 27:
        document['gen'].style.display = 'none'
        document['crafting'].style.display = 'none'
        document['slscreen'].style.display = 'none'
        document['upgrades'].style.display = 'none'
        document['servantm'].style.display = 'none'
        document['game'].style.display = 'inline'
    elif key == 71:
        if gen_shop:
            document['gen'].style.display = 'none'
            document['game'].style.display = 'inline'
            gen_shop = False
        else:
            document['crafting'].style.display = 'none'
            document['slscreen'].style.display = 'none'
            document['upgrades'].style.display = 'none'
            document['game'].style.display = 'none'
            document['servantm'].style.display = 'none'
            document['gen'].style.display = 'inline'
            gen_shop = True
    elif event.altKey == True and event.shiftKey == True and key == 87:
        yes = input('Are you sure you want to wipe your save? ' + \
                    'Type "yes" below to confirm')
        if yes == 'yes':
            del storage[storage_key]
            alert('Reload the game to reset it')
    elif key == 65:
        if event.altKey == True:
            exec(input('Enter code:'), globals())
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
                document['gen'].style.display = 'none'
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
        if show_upgrade:
            document['upgrades'].style.display = 'none'
            document['game'].style.display = 'inline'
            show_upgrade = False
        else:
            document['crafting'].style.display = 'none'
            document['slscreen'].style.display = 'none'
            document['servantm'].style.display = 'none'
            document['game'].style.display = 'none'
            document['gen'].style.display = 'none'
            document['upgrades'].style.display = 'inline'
            show_upgrade = True
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
            document['gen'].style.display = 'none'
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
            document['gen'].style.display = 'none'
            document['slscreen'].style.display = 'inline'
            b_show = True 
        else:
            document['slscreen'].style.display = 'none'
            document['game'].style.display = 'inline'
            b_show = False
    elif key == 82:
        if event.altKey == True:
            user_del_mod()
        else:
            button_rotate(None)
    elif key == 77 and event.altKey == True:
        user_add_mod()
    elif key == 76 and event.altKey == True:
        user_list_mods()

# Random ticks
def random_tick():
    global all_tiles, document, stats, rts
    try:
        sel = tuple(inventory)[0]
    except IndexError:
        sel = 0
    for _ in range(int(rts // 5) + 1):
        for tiles in all_tiles:
            x = randint(0, 17)
            y = randint(0, 5)
            c = tiles[y][x]
            if c == 4:
                if int(randint(1, 500)/rts) != 1:
                    continue
                if y == 0 or x == 0 or y == 5 or x == 17:
                    continue
                if tiles[y-1][x] != 2 or tiles[y+1][x] != 2 or \
                   tiles[y][x-1] != 2 or tiles[y][x+1] != 2:
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

# Click handling
def click(x, y, tiles, inventory, fm=None, rm=False):
    if rm:
        if items[tiles[y][x] - 1][7] != None:
            tiles[y][x] = items[tiles[y][x] - 1][7]
        return None
    global tags, xp, stats
    try:
        sel = tuple(inventory)[0]
    except IndexError:
        sel = 0
    mode = None
    c = tiles[y][x]
    if c in [2, 3] and sel in tags['hoes']:
        break_block(c, inventory) # to reduce durability of the tool
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
        cb = break_block(c, inventory)
        if cb != False:
            mode = False
            stats[0] += 1
            t = loot_table.get(c, None)
            if t == None: 

                raise ValueError(f'Item {c} not in loot table')
            A = t[0]
            B = t[1]
            C = t[2]
            xp += t[7]
            try:
                meta = inventory[sel][1]
            except KeyError:
                meta = 0
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

# Click handler
def click_bind(x, y, inventory):
    global tiles, sel, stats, all_tiles, z, tags, xp, rotate_mode
    tiles = all_tiles[z]
    if rotate_mode == True:
        click(x, y, tiles, inventory, None, True)
    else:
        all_tiles[z], inventory, _ = click(x, y, tiles, inventory)

# This will be executed every 1/3 of a second
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

# Main loop
def mainloop():
    global document, c, fps, lasttime, oldc, levels, xp, servant_layers, \
           servant_break, servant_place, servant_sell, game_time, time, \
           has_servant, gen_money, has_gens, z, all_tiles, tiles
    x_l_offset = l_offset if l_offset > 1 else 0
    c += 1
    if time() - 1 > lasttime:
        lasttime = time()
        fps = c - oldc
        oldc = int(c)
        if all_tiles[x_l_offset][4][16] == 1 and randint(1, 2) == 1:
            stats[2] += 1
            all_tiles[x_l_offset][4][16] = choice(generator[gen_mode][1])
            if randint(1, int(10**len(has_gens))) == 1:
                gen_money += len(has_gens)
                alert(f'You found {len(has_gens)}ǥ!')
        random_tick()
    game_time += (1/fps if fps != 0 else 0)
    if c % choice([15, 16, 17]) == 0:
        one_three_tick()
    if c % 1800 == 0:
        storage[storage_key] = _save()
    nl = round((levels+2)**2*10)
    if xp > nl:
        xp -= nl
        levels += 1
        if levels % 5 == 0 and levels != 0:
            gen_money += 1
    tiles = all_tiles[z]
    for y in range(6):
        for x in range(18):
            set_img(x, y, tiles[y][x])
    fmoney = '${:20,.2f}'.format(float(money))
    document['lprice-1'].textContent = '$' + str(layer_price)
    document['lprice-2'].textContent = '$' + str(layer_price)
    document['rtsprice'].textContent = '$' + str(int(1.005**((4*rts-3)*(100**(((4*rts-3)%10)/10+1)))))
    document['rtsinfo'].textContent = 'Increase growth rate ' + \
                                      f'(current: {4*rts-3})'
    document['gcsel'].textContent = generator[gen_mode][3]
    real_time = ((game_time % 1440) * 72) % 86400
    minutes = (real_time) % 3600
    hours = (real_time - minutes)//3600 % 24
    minutes = str(int(minutes // 60))
    ap = 'AM' if hours < 11 or hours == 23 else 'PM'
    is_night = hours < 6 or hours > 18
    if len(minutes) == 1:
        minutes = '0' + minutes
    if is_night:
        days = int((game_time - (game_time % 1440)) // 1440)
        if days == -1:
            days = 0
        moon = moons[int(days % len(moons))]
        if int(sha(days + game_seed) % 7) == 0:
            moon = rare_moons[int(days % len(rare_moons))]
        elif int(sha(days + game_seed) % 69) == 0:
            moon = super_rare_moons[int(days % len(super_rare_moons))]
    document['info'].innerHTML = f'{fmoney}<br>Layer: {z - l_offset + 1}' + \
                                 f'<br>Time: {(int(hours) % 12) + 1}:' + \
                                 f'{minutes} {ap}' + ('' if not \
                                                      is_night else \
                                                      ' (' + moon + ')') + \
                                 f'<br>{gen_money}ǥ<br>Levels: {levels}'
    document['xp'].attrs['max'] = nl
    document['xp'].attrs['value'] = xp
    document['money2'].textContent = 'You have ' + fmoney
    document['servant_layers'].textContent = ', '.join([str(x) for x in \
                                                        servant_layers])
    document['servant_break'].textContent = ', '.join([names[x] for x in \
                                                       servant_break])
    document['servant_place'].textContent = ', '.join([names[x] for x in \
                                                       servant_place])
    document['servant_sell'].textContent = ', '.join([names[x] for x in \
                                                      servant_sell])
    document['gmoney'].textContent = str(gen_money)
    for key in OrderedDict(inventory):
        if type(inventory[key]) in [list, tuple]:
            if len(inventory[key]) == 1:
                inventory[key] += [0]
                continue
        else:
            inventory[key] = [inventory[key], 0]
        if inventory[key][0] < 1:
                del inventory[key]
    f_inventory ='<br>'.join([format_item(i) for i in \
                              inventory.items() if i[1][0] > 0])
    document['inventory'].innerHTML = f_inventory
    document['inventory2'].innerHTML = f_inventory
    set_timeout(mainloop, 20)

# Start the game

# Variable definitions
gen_shop = False
show_upgrade = False
c_show = False
b_show = False
servant_shop = False
c = 0
lasttime = time()
fps = 0
oldc = 0
rotate_mode = False
last13 = time()
lastsave = time()

# Game state variables (these are values for new saves, the game will overwrite
# them if there is a save)
all_tiles = [[[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,11,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,11,12,11,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,11,2,2,2,2,2,2,2,2,2,2,2,2,2,24,2],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,21,2,23],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,22,2]]]
inventory = OrderedDict({4:[2,0]})
layer_price = 100
l_offset = 1
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
game_time = 360
has_gens = [0]
gen_mode = 0
gen_money = 0
game_seed = randint(0, 2**64 - 1)
mods = {}
z = 0
nl = 40
money = 0

# Button binds
document['servant_add_layer'].bind('click', servant_add_layer)
document['servant_remove_layer'].bind('click', servant_remove_layer)
document['servant_add_break'].bind('click', servant_add_break)
document['servant_remove_break'].bind('click', servant_remove_break)
document['servant_add_place'].bind('click', servant_add_place)
document['servant_remove_place'].bind('click', servant_remove_place)
document['servant_add_sell'].bind('click', servant_add_sell)
document['servant_remove_sell'].bind('click', servant_remove_sell)
document['back1'].bind('click', back_btn)
document['back2'].bind('click', back_btn)
document['back3'].bind('click', back_btn)
document['back4'].bind('click', back_btn)
document['back5'].bind('click', back_btn)
document['b-up'].bind('click', button_up_layer)
document['b-down'].bind('click', button_down_layer)
document['inv-u'].bind('click', button_up_inv)
document['inv-d'].bind('click', button_down_inv)
document['b-save'].bind('click', button_save)
document['b-stats'].bind('click', button_stats)
document['b-craft'].bind('click', button_craft)
document['b-shop'].bind('click', button_shop)
document['b-avatar'].bind('click', button_servant)
document['b-gen'].bind('click', button_gen)
document['b-backup'].bind('click', button_backup)
document['slsave'].bind('click', button_slsave)
document['slload'].bind('click', button_slload)
document['b-sell'].bind('click', button_sell)
document['b-sell-all'].bind('click', button_sell_all)
document['b-rotate'].bind('click', button_rotate)

# Image binds
for x in range(18):
    for y in range(6):
        document[str(y) + '-' + str(x)].bind('mousedown', \
                                             get_handle_click(x, y))

# Crafting button binds
acraft = set(['cd' + x[1] for x in recipe_data_vars if x[1] != '-fuel'] + \
             ['cd-smelting'])
for j, R in enumerate(recipe_data_vars):
    rcp = ''
    for i, r in enumerate(R[0]):
        x = r[0]
        y = r[1]
        rcp += '<tr><td class="s">' + ', '.join([str(z[0]) + 'x ' + \
                                                 names[z[1]] for z in x]) + \
               '</td><td class="s">' + str(y[0]) + 'x ' + names[y[1]] + \
               f'</td><td class="s"><button id={j}c{i}>Craft</button></td></tr>'
    document['crafting' + R[1]].innerHTML += rcp
    for i, r in enumerate(R[0]):
        document[f'{j}c' + str(i)].bind('click', get_craft_bind(r[0], r[1]))
    if R[1] != '-fuel':
        document['cb' + R[1]].bind('click', \
                                   get_craft_switch('cd' + R[1], \
                                                    list(acraft - \
                                                         set(['cd' + R[1]]))))

# Smelting button binds
rcp = ''
for i, s in enumerate(smelt_recipes):
    a, b = s[0]
    c, d = s[1]
    rcp += f'<tr><td class="s">{str(a)}x {names[b]}</td><td class="s">' + \
           f'{str(c)}x {names[d]}</td><td class="s"><button id="s{i}">' + \
           f'Smelt (1 Fuel)</button></td></tr>'
document['smelting-div'].innerHTML += rcp
for i, s in enumerate(smelt_recipes):
    document['s' + str(i)].bind('click', get_smelt_bind(s[0], s[1], s[2]))
document['cb-smelting'].bind('click', \
                             get_craft_switch('cd-smelting', \
                                              list(acraft - \
                                                   set(['cd-smelting']))))

# Generator html
o = ''
for x in generator:
    o += f'<tr><td class="s">{x[3]}</td><td class="s"><button id="{x[2]}">Buy ({x[0]}ǥ)</button></td></tr>'
document['gendiv'].innerHTML += o
document['gb-plains'].bind('click', get_gen_shop_sel(0))
document['gb-plains'].innerHTML = 'Select'
for i, x in enumerate(generator[1:]):
    document[x[2]].bind('click', get_gen_shop_buy(i + 1, x[2]))

# Shop html
o = ''
for i, x in enumerate(shop):
    o += f'<tr><td class="s">{x[0]}</td><td class="s">{x[1]}</td><td class="s"><button id="sb-{i}">Buy</button></td></tr>'
document['shop-div'].innerHTML += o
for i, x in enumerate(shop):
    document[f'sb-{i}'].bind('click', eval(x[2]))

# Key handler bind
document.bind('keydown', handle_key)

# Hide stuff
document['upgrades'].style.display = 'none'
document['crafting'].style.display = 'none'
document['servantm'].style.display = 'none'
document['slscreen'].style.display = 'none'
document['gen'].style.display = 'none'

# Load your save, if you have it
if storage_key in storage:
    load_save(storage[storage_key])
for mod in mods.values():
    load_mod(mod, False)

# Display the game
document['capsule'].style.display = 'block'

# Start the loop
set_timeout(mainloop, 20)                                                                                                                                                                                                                                                                          

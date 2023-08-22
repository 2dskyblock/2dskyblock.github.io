
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

try:
    # Imports
    
    from browser import document, alert
    from browser.timer import set_timeout
    from browser.local_storage import storage
    from hashlib import sha256 as _sha
    from collections import OrderedDict
    import base64
    from random import choice, randint
    
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
             55:'Diamond Pickaxe', 56:'Diamond Sword', 57:'Diamond Axe', 58:'Diamond Shovel', 59:'Diamond Hoe'}
    
    prices = {1:0, 2:20, 3:5, 4:10, 5:10, 6:10, 7:10, 8:10, 9:10, 10:15, 11:15, 12:15, 13:1.25, 14:10, \
              15:10, 16:7.5, 17:10, 18:5, 19:7.5, 20:2.5, 25:10, 26:20, 27:40, 28:60, 29:100, \
              30:10, 31:40, 32:60, 33:45, 34:67.5, 35:100, 36:30, 37:15, 38:17.5, 39:90, \
              40:405, 41:607.5, 42:900, 43:157.5, 44:1, 45:55, 46:53.75, 47:55, 48:20, 49:37.5, \
              50:137.5, 51:91.25, 52:137.5, 53:47.5, 54:92.5, 55:302.5, 56:201.5, 57:302.5, \
              58:102.75, 59:202.75}
    
    tags = {
        'picks':[15, 45, 50, 55],
        'swords':[16, 46, 51, 56],
        'axes':[17, 47, 52, 57],
        'shovels':[18, 48, 53, 58],
        'hoes':[19, 49, 54, 59],
        'unbreakable':[1, 21, 22, 23, 24],
        'can_break_pick_1':[15, 45, 50, 55],
        'can_break_pick_2':[45, 50, 55],
        'can_break_pick_3':[50, 55],
        'can_be_broken_pick_1':[25, 26, 36],
        'can_be_broken_pick_2':[27, 28],
        'can_be_broken_pick_3':[29],
        'wooden_tools':[15, 16, 17, 18, 19],
        'copper_tools':[45, 46, 47, 48, 49],
        'iron_tools':[50, 51, 52, 53, 54],
        'diamond_tools':[55, 56, 57, 58, 59],
        'tools':[15, 16, 17, 18, 19] + list(range(45, 60))
    }
    
    def can_break(c, inventory):
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
        else:
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
        [25, 25, 25, 25, 25, 25, 25, 26, 36, 27, 28],
        [25, 25, 25, 25, 25, 25, 25, 26, 36, 27, 28, 29]
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
        [[[1, 30]], [1, 44]],
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
        [[[2, 13], [2, 35]], [1, 59]]
    ]
    
    smelt_recipes = [
        [[1, 37], [1, 38]],
        [[1, 31], [1, 33]],
        [[1, 32], [1, 34]]
    ]

    def loot_table(c):
        try:
            if c == 1:
                return [[1], 1, [1], [1], [1], [1], [1]]
            elif c == 2:
                return [[3], 1, [1], [3], [1], [1], [1]]
            elif c == 3:
                return [[3], 1, [1], [3], [1], [1], [1]]
            elif c == 4:
                return [[4], 2, [1], [4], [1], [1], [1]]
            elif c == 5:
                return [[5], 1, [1], [5], [1], [1], [1]]
            elif c == 6:
                return [[6], 1, [1], [6], [1], [1], [1]]
            elif c == 7:
                return [[6], 2, [1], [5, 6], [1], [1], [1]]
            elif c == 8:
                return [[6], 7, [1], [5, 6], [1], [1], [1]]
            elif c == 9:
                return [[6], 8, [1], [5, 6], [1], [1], [1]]
            elif c == 10:
                return [[4, 13, 13], 1, [0, 0, 1, 2], [10], [0, 1, 1, 2], [1, 1, 1, 2], [1, 1, 2, 2]]
            elif c == 11:
                return [[4, 13, 13], 2, [0, 0, 1, 2], [10], [0, 1, 1, 2], [1, 1, 1, 2], [1, 1, 2, 2]]
            elif c == 12:
                return [[4, 13, 13], 9, [0, 0, 1, 2], [10], [0, 1, 1, 2], [1, 1, 1, 2], [1, 1, 2, 2]]
            elif c == 13:
                return [[13], 1, [1], [13], [1], [1], [1]]
            elif c == 14:
                return [[14], 1, [1], [14], [1], [1], [1]]
            elif c == 20:
                return [[20], 1, [1], [20], [1], [1], [1]]
            elif c == 25:
                return [[25], 1, [1], [25], [1], [1], [1]]
            elif c == 26:
                return [[30], 1, [1, 2, 3], [26], [1, 2, 3, 3], [1, 2, 3, 3, 4], [2, 3, 4, 4, 5]]
            elif c == 27:
                return [[31], 1, [1], [27], [1, 1, 2], [1, 2, 2], [2, 3, 3]]
            elif c == 28:
                return [[32], 1, [1], [28], [1, 1, 2], [1, 2, 2], [2, 3, 3]]
            elif c == 29:
                return [[35], 1, [1], [29], [1, 1, 2], [1, 2, 2], [2, 3, 3]]
            elif c == 36:
                return [[37], 1, [1, 2, 3], [37], [1, 2, 3, 3], [1, 2, 3, 3, 4], [2, 3, 4, 4, 5]]
            elif c == 39:
                return [[39], 1, [1], [39], [1], [1], [1]]
            elif c == 40:
                return [[40], 1, [1], [40], [1], [1], [1]]
            elif c == 41:
                return [[41], 1, [1], [41], [1], [1], [1]]
            elif c == 42:
                return [[42], 1, [1], [42], [1], [1], [1]]
            elif c == 43:
                return [[43], 1, [1], [43], [1], [1], [1]]
            else:
                raise ValueError(f'ID {c} not in loot table')
        except Exception as e:
            import traceback
            x = traceback.format_exc()
            x = x.replace('<','&LT;')
            x = x.replace('>','&GT;')
            x = x.replace('\n', '<br>')
            x = x.replace('\t', '&#9;')
            document.write('ERROR (please report):<br><br>' + x)
        
    def can_place(x, y):
        if x == 4: 
            return y == 2
        elif x in range(15, 20):
            return False
        elif x in range(30, 36):
            return False
        elif x in [38, 44]:
            return False
        elif x in range(45, 60):
            return False
        else:
            return y == 1
        
    def encode(x):
        x = repr(x).encode('utf-8').decode('latin-1')
        y = 'x'
        for i, b in enumerate(x):
            y += chr((sha('techno never dies' + y[-1] + str(i)) % 256) ^ ord(b))
        return base64.b64encode(y[1:].encode('latin-1')).decode('latin-1')
        
    def decode(x):
        x = base64.b64decode(x.encode('latin-1')).decode('latin-1')
        y = ''
        x = 'x' + x
        for i, b in enumerate(x[1:]):
            y += chr((sha('techno never dies' + x[i] + str(i)) % 256) ^ ord(b))
        return eval(y.encode('latin-1').decode('utf-8'))
    
    def format_meta(item, meta):
        try:
            global tags
            if item in tags['tools']:
                return ' (' + str(round(meta*100, 1)) + '%)'
            else:
                return ''
        except Exception as e:
            global document
            import traceback
            x = traceback.format_exc()
            x = x.replace('<','&LT;')
            x = x.replace('>','&GT;')
            x = x.replace('\n', '<br>')
            x = x.replace('\t', '&#9;')
            document.write('ERROR (please report):<br><br>' + x)

    # Display an image
    def set_img(x, y, new):
        document[str(y) + '-' + str(x)].attrs['src'] = 'skyblock-assets-0-0-1/' + str(new) + '.png'
    
    def show_controls(_ev):
        alert('Controls:\n\nClick to interact\nUp/down arrow -> scroll through inventory\n' + \
              'W -> move 1 layer up\nS -> move 1 layer down\nC -> crafting\nQ -> sell 1 item\n' + \
              'alt+Q -> sell all of selected item\nU -> upgrades shop\nalt+S -> save\nalt+shift+W -> wipe save')

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
    c_show = False
    # other stuff
    gen_level = 0
    document['controls'].bind('click', show_controls)
    document['copyright'].bind('click', show_copyright)
    
    def add_layer(down=False):
        global all_tiles, base_tiles, z, l_offset
        if down:
            all_tiles = [[[int(a) for a in b] for b in base_tiles],] + all_tiles
            z += 1
            l_offset -= 1
        else:
            all_tiles.append([[int(a) for a in b] for b in base_tiles])
    
    # Loading
    try:
        load = decode(storage[sver])
        ver = load[0]
        if ver != 1:
            alert('Downgrading a world is not supported. Closing game.')
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
    except KeyError:
        pass
    
    tiles = all_tiles[z]

    # get click handler for images
    def get_handle_click(x, y):
        def handle_click(_event):
            place(x, y)
        return handle_click
    
    # assign the click events to the images
    for x in range(18):
        for y in range(6):
            document[str(y) + '-' + str(x)].bind('mousedown', get_handle_click(x, y))
    
    # Saving
    def save():
        try:
            storage[sver] = encode({0:1,1:all_tiles,2:inventory,3:sel,4:money,5:layer_price,\
                                    6:z,7:l_offset,8:gen_level})
        except Exception as e:
            from browser import document
            import traceback
            x = traceback.format_exc()
            x = x.replace('<','&LT;')
            x = x.replace('>','&GT;')
            x = x.replace('\n', '<br>')
            x = x.replace('\t', '&#9;')
            document.write('ERROR (please report):<br><br>' + x)
    
    def upgrade_shop():
        global document, alert, inventory, money, layer_price, gen_level
        try:
            while True:
                item = input('Enter the item you want to buy (Enter nothing to exit)')
                if item.strip() == '' or item.lower().strip() == 'nothing':
                    break
                elif item.strip() == '1':
                    if money >= layer_price:
                        money -= layer_price
                        add_layer()
                        layer_price *= 3
                        break
                    else:
                        alert('Not enough money!')
                elif item.strip() == '2':
                    if money >= layer_price:
                        money -= layer_price
                        add_layer(True)
                        layer_price *= 3
                        break
                    else:
                        alert('Not enough money!')
                elif item.strip() == '3' and gen_level < 4:
                    if money >= int(100 * 2.5**gen_level):
                        money -= int(100 * 2.5**gen_level)
                        gen_level += 1
                        break
                    else:
                        alert('Not enough money!')
                else:
                    alert('Invalid item!')
            document['upgrades'].style.display = 'none'
            document['game'].style.display = 'inline'
        except Exception as e:
            import traceback
            x = traceback.format_exc()
            x = x.replace('<','&LT;')
            x = x.replace('>','&GT;')
            x = x.replace('\n', '<br>')
            x = x.replace('\t', '&#9;')
            document.write('ERROR (please report):<br><br>' + x)
    
    # Crafting binds
    def get_craft_bind(inp, out):
        def craft_bind(_ev):
            try:
                global inventory, tags
                for e in inp:
                    x = e[0]
                    y = e[1]
                    if y in inventory and inventory[y][0] >= x:
                        inventory[y][0] -= x
                    else:
                        alert('Not enough materials!')
                        return
                if out[1] not in inventory:
                    inventory[out[1]] = [out[0], 0]
                    if out[1] in tags['tools']:
                        inventory[out[1]][1] = 1
                else:
                    inventory[out[1]][1] += out[0]
                    inventory[out[1]][0] += out[0]
            except Exception as e:
                import traceback
                x = traceback.format_exc()
                x = x.replace('<','&LT;')
                x = x.replace('>','&GT;')
                x = x.replace('\n', '<br>')
                x = x.replace('\t', '&#9;')
                document.write('ERROR (please report):<br><br>' + x)
        return craft_bind
    
    for i, r in enumerate(recipes):
        document['c' + str(i)].bind('click', get_craft_bind(r[0], r[1]))
    
    # Smelting binds
    def get_smelt_bind(inp, out):
        def smelt_bind(_ev):
            try:
                global inventory
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
            except Exception as e:
                import traceback
                x = traceback.format_exc()
                x = x.replace('<','&LT;')
                x = x.replace('>','&GT;')
                x = x.replace('\n', '<br>')
                x = x.replace('\t', '&#9;')
                document.write('ERROR (please report):<br><br>' + x)
        return smelt_bind
    
    for i, s in enumerate(smelt_recipes):
        document['s' + str(i + 1)].bind('click', get_smelt_bind(s[0], s[1]))
    
    # Main key handling
    def handle_key(event):
        try:
            global money, inventory, prices, z, sel, storage, sver, tags
            key = event.keyCode
            if key == 83 and event.altKey == True:
                save()
            elif event.altKey == True and event.shiftKey == True and key == [87, 119]:
                yes = input('Are you sure you want to wipe your save? Type "yes" below to confirm')
                if yes == 'yes':
                    del storage[sver]
                    alert('Reload the game to reset it')
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
                    del inventory[i]
                else:
                    inventory[i][0] -= 1
                    if inventory[i][0] == 0:
                        del inventory[i]
                    money += prices[i]
            elif key == 85:
                    document['game'].style.display = 'none'
                    document['upgrades'].style.display = 'inline'
                    set_timeout(upgrade_shop, 1000)
            elif key == 87:
                if z != len(all_tiles) - 1:
                    z += 1
            elif key == 83:
                if z != 0:
                    z -= 1
            elif key == 67:
                global c_show
                if c_show == False:
                    document['game'].style.display = 'none'
                    document['crafting'].style.display = 'block'
                    c_show = True
                else:
                    document['crafting'].style.display = 'none'
                    document['game'].style.display = 'block'
                    c_show = False
        except Exception as e:
            import traceback
            x = traceback.format_exc()
            x = x.replace('<','&LT;')
            x = x.replace('>','&GT;')
            x = x.replace('\n', '<br>')
            x = x.replace('\t', '&#9;')
            document.write('ERROR (please report):<br><br>' + x)
    document.bind('keydown', handle_key)
    
    def random_tick():
        global all_tiles, document
        try:
            for tiles in all_tiles:
                x = randint(0, 17)
                y = randint(0, 5)
                c = tiles[y][x]
                if c == 4:
                    if randint(1, 500) != 1:
                        continue
                    if y == 0 or x == 0 or y == 5 or x == 17:
                        continue
                    if tiles[y-1][x] != 2 or tiles[y+1][x] != 2 or tiles[y][x-1] != 2 or tiles[y][x+1] != 2:
                        return
                    tiles[y-1][x] = 11
                    tiles[y+1][x] = 11
                    tiles[y][x-1] = 11
                    tiles[y][x+1] = 11
                    tiles[y][x] = 12
                elif c == 3:
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
                        tiles[y][x] = 2
                elif y == 4 and x == 16 and all_tiles[l_offset - 1][4][16] == 1:
                    all_tiles[l_offset - 1][4][16] = choice(generator[gen_level])
                    try:
                        if gen_level == 4:
                            del document['generator-upgrade']
                    except KeyError:
                        pass
            if randint(1, 2) == 1:
                set_timeout(random_tick, 1)
        except Exception as e:
            import traceback
            x = traceback.format_exc()
            x = x.replace('<','&LT;')
            x = x.replace('>','&GT;')
            x = x.replace('\n', '<br>')
            x = x.replace('\t', '&#9;')
            document.write('ERROR (please report):<br><br>' + x)
    
    def place(x, y):
        try:
            global inventory, tiles, sel
            try:
                sel = tuple(inventory)[0]
            except IndexError:
                sel = 0
            c = tiles[y][x]
            if can_place(sel, c) and sel in inventory.keys():
                if inventory[sel][0] != 0:
                    inventory[sel][0] -= 1
                    tiles[y][x] = sel
                if inventory[sel][0] == 0:
                    del inventory[sel][0]
                    if len(inventory) > 0:
                        sel = tuple(inventory)[0]
            else:
                cb = can_break(c, inventory)
                if cb != False:
                    t = loot_table(c)
                    A = t[0]
                    B = t[1]
                    C = t[2]
                    if cb != None:
                        for d in [choice(A) for _ in range(choice(C))]:
                            if d in inventory:
                                inventory[d][0] += 1
                            else:
                                inventory[d] = [1, 0]
                                if len(inventory) == 1:
                                    sel = tuple(inventory)[0]
                    tiles[y][x] = B
        except Exception as e:
            import traceback
            x = traceback.format_exc()
            x = x.replace('<','&LT;')
            x = x.replace('>','&GT;')
            x = x.replace('\n', '<br>')
            x = x.replace('\t', '&#9;')
            document.write('ERROR (please report):<br><br>' + x)  

    def mainloop():
        global document
        try:
            # render the tiles
            tiles = all_tiles[z]
            for y in range(6):
                for x in range(18):
                    set_img(x, y, tiles[y][x])
            # render prices
            fmoney = '${:20,.2f}'.format(float(money))
            document['lprice-1'].textContent = str(layer_price)
            document['lprice-2'].textContent = str(layer_price)
            try:
                document['gprice'].textContent = str(int(100 * 2.5**gen_level))
                document['glevel'].textContent = str(gen_level)
            except KeyError:
                pass
            document['info'].innerHTML = fmoney + '<br>Layer: ' + str(z + l_offset)
            document['money2'].textContent = 'You have ' + fmoney
            # fix inventory
            for key in OrderedDict(inventory):
                if inventory[key][0] == 0:
                    del inventory[key]
            # random tick
            random_tick()
            # render the inventory
            f_inventory ='<br>'.join([f'{i[1][0]}x {names[i[0]]}' + format_meta(i[0], i[1][1]) for i in inventory.items()])
            document['inventory'].innerHTML = f_inventory
            document['inventory2'].innerHTML = f_inventory
            # redo the loop
            set_timeout(mainloop, 20)
        except Exception as e:
            import traceback
            x = traceback.format_exc()
            x = x.replace('<','&LT;')
            x = x.replace('>','&GT;')
            x = x.replace('\n', '<br>')
            x = x.replace('\t', '&#9;')
            document.write('ERROR (please report):<br><br>' + x)
    # start the game
    set_timeout(mainloop, 20)
except Exception as e:
    from browser import document
    import traceback
    x = traceback.format_exc()
    x = x.replace('<','&LT;')
    x = x.replace('>','&GT;')
    x = x.replace('\n', '<br>')
    x = x.replace('\t', '&#9;')
    document.write('ERROR (please report):<br><br>' + x)
    

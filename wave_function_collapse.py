from PIL import Image
import random
import json
from tile import Tile
from cell import Cell

def generateEntropyTable(board):
    entropytable = []
    for y in board:
        entropyrow = []
        for cell in y:
            entropyrow.append(cell.getEntropy())
        entropytable.append(entropyrow)
    return entropytable

def minimumNonZero2DList(lst):
    minimum = 1000
    for y in lst:
        for x in y:
            if x < minimum and x != 0:
                minimum = x
    return minimum

def allZero2DList(lst):
    for y in lst:
        for x in y:
            if x != 0:
                return False
    return True

def getTileByEntropy(board, entropy):
    matchingentropy = []
    for y in board:
        for cell in y:
            if cell.getEntropy() == entropy:
                matchingentropy.append(cell)
    if len(matchingentropy) == 1:
        return matchingentropy[0]
    else:
        return random.choice(matchingentropy)

def index2DList(lst, item):
    for yi, y in enumerate(lst):
        if item in y:
            return (yi, y.index(item))

def main(settingssource):
    f = open(f"{settingssource}.json")
    settings = json.load(f)
    f.close()

    WEIGHTBLANK = settings["background"]["wave_function_collapse"]["weights"]["blank"]
    WEIGHTWIRESTRAIGHT = settings["background"]["wave_function_collapse"]["weights"]["wire_straight"]
    WEIGHTWIREBEND = settings["background"]["wave_function_collapse"]["weights"]["wire_bend"]
    WEIGHTWIREJUNCTION = settings["background"]["wave_function_collapse"]["weights"]["wire_junction"]
    WEIGHTCOMPONENTBASIC = settings["background"]["wave_function_collapse"]["weights"]["component_basic"]
    WEIGHTCOMPONENTCOMPLEX = settings["background"]["wave_function_collapse"]["weights"]["component_complex"]
    TARGETWIDTH = settings["wallpaper_size"]["width"]
    TARGETHEIGHT = settings["wallpaper_size"]["height"]
    TILESIZE = settings["background"]["wave_function_collapse"]["tile_size"]
    WIDTH = TARGETWIDTH // TILESIZE
    HEIGHT = TARGETHEIGHT // TILESIZE
    
    possibilities = [
        Tile("tiles/blank.png", [0, 0, 0, 0], WEIGHTBLANK),
        Tile("tiles/wire_straight_1.png", [1, 0, 1, 0], WEIGHTWIRESTRAIGHT),
        Tile("tiles/wire_straight_2.png", [0, 1, 0, 1], WEIGHTWIRESTRAIGHT),
        Tile("tiles/wire_corner_1.png", [1, 1, 0, 0], WEIGHTWIREBEND),
        Tile("tiles/wire_corner_2.png", [0, 1, 1, 0], WEIGHTWIREBEND),
        Tile("tiles/wire_corner_3.png", [0, 0, 1, 1], WEIGHTWIREBEND),
        Tile("tiles/wire_corner_4.png", [1, 0, 0, 1], WEIGHTWIREBEND),
        Tile("tiles/wire_tee_1.png", [1, 1, 1, 0], WEIGHTWIREJUNCTION),
        Tile("tiles/wire_tee_2.png", [0, 1, 1, 1], WEIGHTWIREJUNCTION),
        Tile("tiles/wire_tee_3.png", [1, 0, 1, 1], WEIGHTWIREJUNCTION),
        Tile("tiles/wire_tee_4.png", [1, 1, 0, 1], WEIGHTWIREJUNCTION),
        Tile("tiles/wire_cross_1.png", [1, 1, 1, 1], WEIGHTWIREJUNCTION),
        Tile("tiles/wire_cross_2.png", [1, 1, 1, 1], WEIGHTWIREJUNCTION),
        Tile("tiles/resistor_1.png", [1, 0, 1, 0], WEIGHTCOMPONENTBASIC),
        Tile("tiles/resistor_2.png", [0, 1, 0, 1], WEIGHTCOMPONENTBASIC),
        Tile("tiles/resistor_3.png", [1, 0, 1, 0], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/resistor_4.png", [0, 1, 0, 1], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/resistor_5.png", [1, 0, 1, 0], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/resistor_6.png", [0, 1, 0, 1], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/resistor_7.png", [1, 0, 1, 0], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/resistor_8.png", [0, 1, 0, 1], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/resistor_9.png", [1, 0, 1, 1], WEIGHTCOMPONENTBASIC),
        Tile("tiles/resistor_10.png", [1, 1, 0, 1], WEIGHTCOMPONENTBASIC),
        Tile("tiles/fuse_1.png", [1, 0, 1, 0], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/fuse_2.png", [0, 1, 0, 1], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/capacitor_1.png", [1, 0, 1, 0], WEIGHTCOMPONENTBASIC),
        Tile("tiles/capacitor_2.png", [0, 1, 0, 1], WEIGHTCOMPONENTBASIC),
        Tile("tiles/capacitor_3.png", [1, 0, 1, 0], WEIGHTCOMPONENTBASIC),
        Tile("tiles/capacitor_4.png", [0, 1, 0, 1], WEIGHTCOMPONENTBASIC),
        Tile("tiles/diode_1.png", [1, 0, 1, 0], WEIGHTCOMPONENTBASIC),
        Tile("tiles/diode_2.png", [0, 1, 0, 1], WEIGHTCOMPONENTBASIC),
        Tile("tiles/diode_3.png", [1, 0, 1, 0], WEIGHTCOMPONENTBASIC),
        Tile("tiles/diode_4.png", [0, 1, 0, 1], WEIGHTCOMPONENTBASIC),
        Tile("tiles/diode_5.png", [1, 0, 1, 0], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/diode_6.png", [0, 1, 0, 1], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/mosfet_1.png", [1, 0, 1, 1], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/mosfet_2.png", [1, 1, 0, 1], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/inductor_1.png", [1, 0, 1, 0], WEIGHTCOMPONENTBASIC),
        Tile("tiles/inductor_2.png", [0, 1, 0, 1], WEIGHTCOMPONENTBASIC),
        Tile("tiles/inductor_3.png", [1, 0, 1, 0], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/inductor_4.png", [0, 1, 0, 1], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/inductor_5.png", [1, 0, 1, 0], WEIGHTCOMPONENTCOMPLEX),
        Tile("tiles/inductor_6.png", [0, 1, 0, 1], WEIGHTCOMPONENTCOMPLEX)
    ]

    done = False
    while not done:
        try:
            board = []
            for _ in range(HEIGHT):
                temp = []
                for _ in range(WIDTH):
                    temp.append(Cell(possibilities))
                board.append(temp)
            
            while not done:
                entropytable = generateEntropyTable(board)

                if allZero2DList(entropytable):
                    done = True
                    continue
                
                entropy = minimumNonZero2DList(entropytable)
                minimumentropycell = getTileByEntropy(board, entropy)
                minimumentropycellposition = index2DList(board, minimumentropycell)

                if minimumentropycell.getEntropy() == 0:
                    minimumentropycell.setState()
                else:
                    minimumentropycell.setRandomState()
                
                minimumentropycell.propagateChange(board, minimumentropycellposition)
        except Exception:
            pass

    image = Image.new('RGB', (WIDTH * TILESIZE, HEIGHT * TILESIZE), 0)
    for yi, y in enumerate(board):
        for xi, cell in enumerate(y):
            image.paste(Image.open(cell.getState().getImagePath()), (xi * TILESIZE, yi * TILESIZE))

    return image

if __name__ == "__main__":
    main().save(f"wave_function_collapse.png", "PNG")

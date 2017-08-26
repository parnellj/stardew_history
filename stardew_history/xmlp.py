import colorsys
import csv
import os

import pygame
from lxml import etree

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)

# Change the in directory as needed
char_name = 'Diana'
indir = r"C:\Users\Justin\AppData\Roaming\StardewValley\Saves\Diana_116831079"

outdir = os.path.join('.', 'backups', char_name)
files = [a for a in os.listdir(outdir) if 'SaveGameInfo' not in a]

# These are the 3 largest categories of objects.  There are many more, though.
subdirs = {'objs': {'x': './/objects/item/key/Vector2/X',
                    'y': './/objects/item/key/Vector2/Y',
                    'n': './/objects/item/value/Object/Name'},
           'ltfs': {'x': './/LargeTerrainFeature/tilePosition/X',
                    'y': './/LargeTerrainFeature/tilePosition/Y',
                    'n': './/LargeTerrainFeature'},
           'tefs': {'x': './/terrainFeatures/item/key/Vector2/X',
                    'y': './/terrainFeatures/item/key/Vector2/Y',
                    'n': './/terrainFeatures/item/value/TerrainFeature'}
           }

itemNames = []

# Initialize the PyGame window to the parameters indicated below
mult = 15
xmx = (80 * mult)
ymx = 60 * mult
pygame.init()
screen = pygame.display.set_mode((xmx + 200, ymx))
pygame.display.set_caption('Farm View')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen.fill(WHITE)
font = pygame.font.Font(None, 12)


def draw(objs, types):
    screen.fill(WHITE)
    # draw rectangles
    for x, y, n in [t for sub in objs.itervalues() for t in sub]:
        pygame.draw.rect(screen, types[n],
                         (x * mult, y * mult, mult, mult), 0)

    # draw key
    for i, n in enumerate(sorted(types.iterkeys())):
        pygame.draw.rect(screen, types[n],
                         (xmx + 50, i * mult * 1.5, mult, mult), 0)
        text = font.render(n, 1, BLACK)
        screen.blit(text, (xmx + 75, i * mult * 1.5))

    pygame.display.flip()


def to_csv(objs, xmx, ymx, outdir="/", outfile="a.file"):
    matrix = [["" for x in range(xmx + 1)] for y in range(ymx + 1)]
    for x, y, n in [t for sub in objs.itervalues() for t in sub]:
        matrix[y][x] = n[0:2]
    with open('test.csv', 'wb') as f:
        w = csv.writer(f)
        w.writerows(matrix)
    return


def getNames():
    allNames = []

    for f in files:
        eTree = etree.parse(os.path.join(outdir, f))
        curFarm = eTree.xpath(".//GameLocation[@xsi:type='Farm']")[0]
        curName = []

        for k, v in subdirs.iteritems():
            if k is not 'objs':
                n = [c.attrib.values()[0] for c in curFarm.findall(v['n'])]
            else:
                n = [c.text for c in curFarm.findall(v['n'])]

            curName += n

        allNames += curName

    allNames = set(allNames)

    N = len(allNames)
    HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    colors = [(a[0] * 255, a[1] * 255, a[2] * 255) for a in RGB_tuples]

    return {name: color for name, color in zip(sorted(allNames), colors)}


ns = etree.FunctionNamespace("http://www.w3.org/2001/XMLSchema-instance")
ns.prefix = "xsi"

i = 0

itemNames = getNames()
print itemNames

auto = False
change = False
end = False

while True:
    change = False
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                auto = not auto
            elif event.key == pygame.K_RIGHT:
                i = min(len(files) - 1, i + 1)
                change = True
            elif event.key == pygame.K_LEFT:
                i = max(0, i - 1)
                change = True
            elif event.key == pygame.K_ESCAPE:
                end = True
    if end:
        break
    if not(auto or change):
        continue

    i = min(len(files) - 1, i + auto)

    e = etree.parse(os.path.join(outdir, files[i]))
    print e.find(".//dateStringForSaveGame").text
    farm = e.xpath(".//GameLocation[@xsi:type='Farm']")[0]

    all = {}

    for k, v in subdirs.iteritems():
        x = [int(a.text) for a in farm.findall(v['x'])]
        y = [int(b.text) for b in farm.findall(v['y'])]

        if k is not 'objs':
            n = [c.attrib.values()[0] for c in farm.findall(v['n'])]
        else:
            n = [c.text for c in farm.findall(v['n'])]

        all[k] = zip(x, y, n)

    draw(all, itemNames)

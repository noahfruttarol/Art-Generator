#!/usr/bin/env python3
'''HTML art generator by Noah Fruttarol'''
print(__doc__)

from email.policy import default
from logging.config import valid_ident
from pickle import FALSE, TRUE
import random
import sys
from typing import IO

defaultShapes: int = 10000
defaultHight: int = 600
defaultWidth: int = 400
defaultRGB: tuple= [(0, 255), (0, 255), (0, 255)]


class Circle:
    '''Circle class'''
    def __init__(self, cir: tuple, col: tuple):
        self.cx: int = cir[0] 
        self.cy: int = cir[1]
        self.rad: int = cir[2]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]
    
    def draw(self, f: IO[str], t: int):
        '''drawCircle method'''
        ts: str = "   " * t
        line: str = f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.rad}" fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></circle>'
        f.write(f"{ts}{line}\n")

class Rectangle:
    '''Rectangle class'''
    def __init__(self, rec: tuple, col: tuple):
        self.x: int = rec[0]
        self.y: int = rec[1]
        self.width: int = rec[2]
        self.hight: int = rec[3]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]

    def draw(self, f: IO[str], t: int):
        '''drawRectangle method'''
        ts: str = "   " * t
        line: str = f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.hight}" style="fill:rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></rect>'
        f.write(f"{ts}{line}\n")

class Ellipse:
    '''Ellipse class'''
    def __init__(self, ell: tuple, col: tuple):
        self.cx: int = ell[0]
        self.cy: int = ell[1]
        self.rx: int = ell[2]
        self.ry: int = ell[3]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]
    
    def draw(self, f: IO[str], t: int):
        '''drawEllipse method'''
        ts: str = "   " * t
        line: str = f'<ellipse cx="{self.cx}" cy="{self.cy}" rx="{self.rx}" ry="{self.ry}" fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></ellipse>'
        f.write(f"{ts}{line}\n")

class GenRandom:
    '''random number class to gen numbers for art config table'''
    def __init__(self, x, y, rgb):
        self.maxX: int = x
        self.maxY: int = y
        self.maxRad: int = 100
        self.minRx: int = 10
        self.maxRx: int = 30
        self.minRy: int = 10
        self.maxRy: int = 30
        self.minWidth: int = 10
        self.maxWidth: int = 100
        self.minHight: int = 10
        self.maxHight: int = 100
        self.red: tuple = rgb[0]
        self.green: tuple = rgb[1]
        self.blue: tuple = rgb[2]

    def genRow(self):
        '''gives returns a dict with random values to the specifacation set up in class __init__'''
        rand: random.Random = random
        sha: int = rand.randint(0, 2)
        x: int = rand.randint(0, self.maxX)
        y: int = rand.randint(0, self.maxY)
        rad: int = rand.randint(0, self.maxRad)
        rx: int = rand.randint(self.minRx, self.maxRx)
        ry: int = rand.randint(self.minRy, self.maxRy)
        w: int = rand.randint(self.minWidth, self.maxWidth)
        h: int = rand.randint(self.minHight, self.maxHight)
        r: int = rand.randint(self.red[0], self.red[1])
        g: int = rand.randint(self.green[0], self.green[1])
        b: int = rand.randint(self.blue[0], self.blue[1])
        op: float = (float(rand.randint(1,100)))/100
        mydist: dict = {
            "sha": sha,
            "x": x, "y":y,
            "rad": rad,
            "rx": rx, "ry": ry,
            "w": w, "h": h,
            "r": r, "g": g, "b": b,
            "op": op 
        }
        return mydist


class ArtConfig:
    '''Art Config class'''
    def __init__(self, items: int, viewRangeX: int, viewRangeY:int, rgbRange: tuple):
        self.items: int = items ##number of shapes that will be in the class
        self.random: GenRandom = GenRandom(viewRangeX, viewRangeY, rgbRange)
        self.table: dict = [] ##array to hold the shapes
        self.genNewTable() ##gererates new table

    def getSize(self):
        '''retuens total shapes in class'''
        return self.items

    def genNewTable(self):
        '''gererates fresh shapes into table'''
        for x in range(self.items):
            self.table.append(self.random.genRow())
    
    def printTable(self):
        '''prints out the table of shapes with randon values'''
        print("CNT SHA   X   Y RAD  RX  RY   W   H   R   G   B  OP")
        for i in range(self.items):
            temp = self.table[i]
            s: str = f'{i:{" "}{3}}{temp["sha"]:{" "}{4}}{temp["x"]:{" "}{4}}{temp["y"]:{" "}{4}}{temp["rad"]:{" "}{4}}{temp["rx"]:{" "}{4}}{temp["ry"]:{" "}{4}}' ##formats the table and puts into temp string s
            s = s + f'{temp["w"]:{" "}{4}}{temp["h"]:{" "}{4}}{temp["r"]:{" "}{4}}{temp["g"]:{" "}{4}}{temp["b"]:{" "}{4}}{temp["op"]:{" "}{4}}' ##split to not make the line too long
            print(s)##prints formated string

    def getShape(self, i:int):
        '''gets a shape at a cirtain index i'''
        if(i >= self.items or i < 0):
            return self.table[0] ##returns shape at index 0 if i is not in range
        return self.table[i]

class ProEpiloge:
    '''ProEpiloge class'''
    def __init__(self, f: IO[str]):
        self.f: IO[str] = f #file

    def start(self):
        '''opends SVG Canvas and makes the ArtConfig for making html file with the shapes'''
        argc: int = len(sys.argv) ##grabs amount of command line arguments to see if specifacations were given 
        rgb: tuple = defaultRGB##rgb set like this to stop other lines from being too long
        if argc == 2: ##2 command line arguments means amout of shapes was given
            self.openSVG(1, (defaultHight, defaultWidth))
            return ArtConfig(int(sys.argv[1]), defaultHight, defaultWidth, rgb)
        elif argc == 4: ##4 command line arguments means amout of shapes and size was given
            self.openSVG(1, (int(sys.argv[2]),int(sys.argv[3])))
            return ArtConfig(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), rgb)
        elif argc == 10: ##10 command line arguments means amout of shapes, size and rgb range was given
            self.openSVG(1, (sys.argv[2],sys.argv[3]))
            rgb = [(int(sys.argv[4]), int(sys.argv[5])), (int(sys.argv[6]), int(sys.argv[7])), (int(sys.argv[8]), int(sys.argv[9]))]
            return ArtConfig(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), rgb)
        else: ##no or wrong amount of command line arguments means defalt values as set at start of program
            self.openSVG(1, (defaultHight, defaultWidth))
            return ArtConfig(defaultShapes, defaultHight, defaultWidth, rgb)


    def genPage(self, winTitle: str):
        '''adds the title then runs all the functions generating the shapes'''
        self.writeHTMLHeader(winTitle)
        art: ArtConfig = self.start()
        self.genArt(art)
        self.closeSVG(1)

    def writeHTMLcomment(self, t: int, com: str):
        '''writeHTMLcomment method'''
        ts: str = "   " * t
        self.f.write(f'{ts}<!--{com}-->\n')

    def drawShape(self, shape: dict):
        '''draws the shape'''
        sha: int = shape["sha"] ##grabs shape type to then print the right shape
        if sha == 0:
            Circle((shape["x"],shape["y"],shape["rad"]), (shape["r"],shape["g"],shape["b"],shape["op"])).draw(self.f, 2)
            return
        elif sha == 1: 
            Rectangle((shape["x"],shape["y"],shape["w"],shape["h"]),  (shape["r"],shape["g"],shape["b"],shape["op"])).draw(self.f, 2)
            return
        elif sha == 2: 
            Ellipse((shape["x"],shape["y"],shape["rx"],shape["ry"]),  (shape["r"],shape["g"],shape["b"],shape["op"])).draw(self.f, 2)
            return
            
    def genArt(self, art: ArtConfig):
        '''genART method'''
        for i in range(art.getSize()):
            self.drawShape(art.getShape(i)) ##uses loop to draw all shapes 
            
    def openSVG(self, t: int, canvas: tuple):
        '''openSVGcanvas method'''
        ts: str = "   " * t
        self.writeHTMLcomment(t, "Define SVG drawing box")
        self.f.write(f'{ts}<svg width="{canvas[0]}" height="{canvas[1]}">\n')

    def closeSVG(self, t: int):
        '''closeSVGcanvas method'''
        ts: str = "   " * t
        self.f.write(f'{ts}</svg>\n')
        self.f.write(f'</body>\n')
        self.f.write(f'</html>\n')

    def writeHTMLline(self, t: int, line: str):
        '''writeLineHTML method'''
        ts = "   " * t
        self.f.write(f"{ts}{line}\n")

    def writeHTMLHeader(self, winTitle: str):
        '''writeHeadHTML method'''
        self.writeHTMLline(0, "<html>")
        self.writeHTMLline(0, "<head>")
        self.writeHTMLline(1, f"<title>{winTitle}</title>")
        self.writeHTMLline(0, "</head>")
        self.writeHTMLline(0, "<body>")

def writeHTMLfile(): 
    '''writeHTMLfile method'''
    fnam: str = "my_art.html"
    winTitle = "My Art"
    f: IO[str] = open(fnam, "w")
    Epiloge = ProEpiloge(f)
    Epiloge.genPage(winTitle)
    f.close()

def main():
    '''main method'''
    argc: int = len(sys.argv)
    validInput: bool = TRUE
    if (argc > 1):
        if(argc == 3 or (argc > 4 and argc != 10)):
            validInput = FALSE
        for i in range(1, len(sys.argv)):
            if(sys.argv[i].isnumeric() != 1):
                validInput = FALSE
    
    if(validInput):
        writeHTMLfile()
    else:
        print("Incorect useage:")
        print("Useage is")
        print("Python a43.py")
        print("Python a43.py <number-of-shapes>")
        print("Python a43.py <number-of-shapes> <width> <hight>")
        print("Python a43.py <number-of-shapes> <width> <hight> <red-min> <red-max> <green-min> <green-max> <blue-min> <blue-max>")
    
main()

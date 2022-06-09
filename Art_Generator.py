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
    def __init__(self, cir: tuple, col: tuple):
        self.x: int = cir[0] 
        self.y: int = cir[1]
        self.rad: int = cir[2]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]
    
    def draw(self, f: IO[str]):
        spacing: str = "   " * 2
        line: str = f'<circle cx="{self.x}" cy="{self.y}" r="{self.rad}" fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></circle>'
        f.write(f"{spacing}{line}\n")

class Rectangle:
    def __init__(self, rec: tuple, col: tuple):
        self.x: int = rec[0]
        self.y: int = rec[1]
        self.width: int = rec[2]
        self.hight: int = rec[3]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]

    def draw(self, f: IO[str]):
        spacing: str = "   " * 2
        line: str = f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.hight}" style="fill:rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></rect>'
        f.write(f"{spacing}{line}\n")

class Ellipse:
    def __init__(self, ell: tuple, col: tuple):
        self.x: int = ell[0]
        self.y: int = ell[1]
        self.rx: int = ell[2]
        self.ry: int = ell[3]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]
    
    def draw(self, f: IO[str]):
        spacing: str = "   " * 2
        line: str = f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.rx}" ry="{self.ry}" fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></ellipse>'
        f.write(f"{spacing}{line}\n")

class shapeRandom:
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

    def genShape(self):
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


class shapesConfig:
    def __init__(self, items: int, viewRangeX: int, viewRangeY:int, rgbRange: tuple):
        self.items: int = items ##number of shapes that will be in the class
        self.random: shapeRandom = shapeRandom(viewRangeX, viewRangeY, rgbRange)
        self.table: dict = [] ##array to hold the shapes
        self.genNewTable() ##gererates new table

    def getSize(self):
        return self.items

    def genNewTable(self):
        self.table.clear()
        for x in range(self.items):
            self.table.append(self.random.genShape())

    def getShape(self, i:int):
        if(i >= self.items or i < 0):
            return self.table[0] ##returns shape at index 0 if i is not in range
        return self.table[i]

class pageSetup:
    def __init__(self, f: IO[str]):
        self.f: IO[str] = f #file

    def start(self):
        argc: int = len(sys.argv) ##grabs amount of command line arguments to see if specifacations were given 
        rgb: tuple = defaultRGB##rgb set like this to stop other lines from being too long
        if argc == 2: ##2 command line arguments means amout of shapes was given
            self.startPage((defaultHight, defaultWidth))
            return shapesConfig(int(sys.argv[1]), defaultHight, defaultWidth, rgb)
        elif argc == 4: ##4 command line arguments means amout of shapes and size was given
            self.startPage((int(sys.argv[2]),int(sys.argv[3])))
            return shapesConfig(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), rgb)
        elif argc == 10: ##10 command line arguments means amout of shapes, size and rgb range was given
            self.startPage((sys.argv[2],sys.argv[3]))
            rgb = [(int(sys.argv[4]), int(sys.argv[5])), (int(sys.argv[6]), int(sys.argv[7])), (int(sys.argv[8]), int(sys.argv[9]))]
            return shapesConfig(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), rgb)
        else: ##no or wrong amount of command line arguments means defalt values as set at start of program
            self.startPage((defaultHight, defaultWidth))
            return shapesConfig(defaultShapes, defaultHight, defaultWidth, rgb)


    def genPage(self, winTitle: str):
        self.writeHTMLHeader(winTitle)
        art: shapesConfig = self.start()
        self.genAllShapes(art)
        self.endPage()

    def drawShape(self, shape: dict):
        sha: int = shape["sha"] ##grabs shape type to then print the right shape
        if sha == 0:
            Circle((shape["x"],shape["y"],shape["rad"]), (shape["r"],shape["g"],shape["b"],shape["op"])).draw(self.f)
            return
        elif sha == 1: 
            Rectangle((shape["x"],shape["y"],shape["w"],shape["h"]),  (shape["r"],shape["g"],shape["b"],shape["op"])).draw(self.f)
            return
        elif sha == 2: 
            Ellipse((shape["x"],shape["y"],shape["rx"],shape["ry"]),  (shape["r"],shape["g"],shape["b"],shape["op"])).draw(self.f)
            return
            
    def genAllShapes(self, art: ArtConfig):
        for i in range(art.getSize()):
            self.drawShape(art.getShape(i)) ##uses loop to draw all shapes 
            
    def startPage(self, canvas: tuple):
        spacing: str = "   "
        comment: str = "Define SVG drawing box"
        self.f.write(f'{spacing}<!--{comment}-->\n')
        self.f.write(f'{spacing}<svg width="{canvas[0]}" height="{canvas[1]}">\n')

    def endPage(self):
        spacing: str = "   "
        self.f.write(f'{spacing}</svg>\n')
        self.f.write(f'</body>\n')
        self.f.write(f'</html>\n')

    def writeLine(self, line: str):
        spacing: str = "   "
        self.f.write(f"{spacing}{line}\n")

    def writeHeader(self, winTitle: str):
        self.writeLine(0, "<html>")
        self.writeLine(0, "<head>")
        self.writeLine(1, f"<title>{winTitle}</title>")
        self.writeLine(0, "</head>")
        self.writeLine(0, "<body>")

def makeHTMLfile(): 
    fileName: str = "my_art.html"
    title: str = "My Art"
    f: IO[str] = open(fileName, "w")
    Epiloge: pageSetup = pageSetup(f)
    Epiloge.genPage(title)
    f.close()

def main():
    argc: int = len(sys.argv)
    validInput: bool = TRUE
    if (argc > 1):
        if(argc == 3 or (argc > 4 and argc != 10)):
            validInput = FALSE
        for i in range(1, len(sys.argv)):
            if(sys.argv[i].isnumeric() != 1):
                validInput = FALSE
    
    if(validInput):
        makeHTMLfile()
    else:
        print("Incorect useage:")
        print("Useage:")
        print("Python a43.py")
        print("Python a43.py <number-of-shapes>")
        print("Python a43.py <number-of-shapes> <width> <hight>")
        print("Python a43.py <number-of-shapes> <width> <hight> <red-min> <red-max> <green-min> <green-max> <blue-min> <blue-max>")
    
main()

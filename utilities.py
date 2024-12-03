from cmu_graphics import *
from level2 import Level
import random
from snowman import *
from PIL import Image as PilImage
import os
import pathlib

def openImage(fileName):
    return PilImage.open(os.path.join(pathlib.Path(__file__).parent, fileName))

def reset(app, stored=False):
    app.bgImage0 = openImage("bg0.png")
    app.bg0 = CMUImage(app.bgImage0)
    app.bgImage1 = openImage("bg1.png")
    app.bg1 = CMUImage(app.bgImage1)
    app.bgImage2 = openImage("bg2.png")
    app.bg2 = CMUImage(app.bgImage2)
    app.bgImage3 = openImage("bg3.png")
    app.bg3 = CMUImage(app.bgImage3)
    app.bgImage4 = openImage("bg4.png")
    app.bg4 = CMUImage(app.bgImage4)
    app.bgImages = [app.bg0, app.bg1, app.bg2, app.bg3, app.bg4]
    app.setMaxShapeCount(10000)
    app.surfing = False
    app.ballVel = [0, 0]
    app.gravity = 0.5
    app.isSwinging = False
    app.isDrawing = False
    app.ballPos = [50, 50]
    app.remainingLine = 1500
    app.cameraX = 0
    if stored == False:
        app.levels = [
            Level(pivots=[(200, 150), (400, 200), (600, 100)], finishLineX=800),
            Level(pivots=[(250, 300), (500, 250), (750, 150), (1000, 100)],
                  finishLineX=1200),
            Level(pivots=[(300, 200), (600, 300), (900, 250), (1200, 200)],
                  finishLineX=1400),
            Level(pivots=[(400, 350), (800, 300), (1200, 250), (1600, 150)],
                  finishLineX=1800),
            Level(pivots=[(500, 250), (1000, 300), (1500, 200), (2000, 100)],
                  finishLineX=2200),
        ]
    app.levels[app.currentLevel].resetLevel()
    app.carrImage = openImage("carrot.png")
    app.carrot = CMUImage(app.carrImage)
    app.snowman = openImage("snow.png")
    app.flyImage = openImage("para.png")
    app.birdImage0 = openImage("0.png")
    app.birdImage1 = openImage("1.png")
    app.birdImage2 = openImage("2.png")
    app.birdImage3 = openImage("3.png")
    app.surfImage = openImage("surfer.png")
    app.bloodImage0 = openImage("blood0.png")
    app.blood0 = CMUImage(app.bloodImage0)
    app.bloodImage1 = openImage("blood1.png")
    app.blood1 = CMUImage(app.bloodImage1)
    app.bloodImage2 = openImage("blood2.png")
    app.blood2 = CMUImage(app.bloodImage2)
    app.bloodImage3 = openImage("blood3.png")
    app.blood3 = CMUImage(app.bloodImage3)
    app.bloodImage4 = openImage("blood4.png")
    app.blood4 = CMUImage(app.bloodImage4)
    app.bloodImage5 = openImage("blood5.png")
    app.blood5 = CMUImage(app.bloodImage5)
    app.bloodImage6 = openImage("blood6.png")
    app.blood6 = CMUImage(app.bloodImage6)
    app.bloodImage7 = openImage("blood7.png")
    app.blood7 = CMUImage(app.bloodImage7)
    app.bloodImage8 = openImage("blood8.png")
    app.blood8 = CMUImage(app.bloodImage8)
    app.bloodImage9 = openImage("blood9.png")
    app.blood9 = CMUImage(app.bloodImage9)
    app.bloodImage10 = openImage("blood10.png")
    app.blood10 = CMUImage(app.bloodImage10)
    app.bloodImage11 = openImage("blood11.png")
    app.blood11 = CMUImage(app.bloodImage11)
    app.bloods = [app.blood0, app.blood1, app.blood2, app.blood3, app.blood4, app.blood5, app.blood6, app.blood7, app.blood8, app.blood9, app.blood10, app.blood11]
    
    app.Bird0 = CMUImage(app.birdImage0)
    app.Bird1 = CMUImage(app.birdImage1)
    app.Bird2 = CMUImage(app.birdImage2)
    app.Bird3 = CMUImage(app.birdImage3)
    app.Snow = CMUImage(app.snowman)
    app.surfer = CMUImage(app.surfImage)
    app.flier = CMUImage(app.flyImage)
    app.birdImages = [app.Bird0, app.Bird1, app.Bird2, app.Bird3]
    numBirds = 3 + app.currentLevel  # Increase the number of birds with the level
    birdSpeeds = [random.randint(2, 5) + app.currentLevel for _ in range(numBirds)]  # Faster birds on higher levels
    birdHeights = [random.randint(50, app.height - 50) for _ in range(numBirds)]  # Birds at random heights
    
    app.birds = [
        {'x': app.levels[app.currentLevel].finishLineX + random.randint(-200, 200),
         'y': birdHeights[i], 'speed': birdSpeeds[i]}
        for i in range(numBirds)
    ]
    
    #app.levels[app.currentLevel].finishLineX
    app.snowman = Snowman(x=app.levels[app.currentLevel].finishLineX ,
                          y=app.height / 2)
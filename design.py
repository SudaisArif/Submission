from cmu_graphics import *
import math

def showLevelCreator(app):
    drawRect(0, 0, app.width, app.height,  fill= "yellow")
    drawLabel("Create Your Custom Level", app.width / 2, app.height * 0.2, size=50,
                  font="monospace", bold=True, fill="black")
    drawLabel(f"Number of Pivots: {app.customPiv}", app.width / 2, app.height * 0.5, size=25,
                  font="monospace", bold=True, fill="black")
    drawLabel(f"Level Length: {app.customLen}", app.width / 2, app.height * 0.7, size=25,
                  font="monospace", bold=True, fill="black")
    drawLine(app.width / 4, app.height * 0.6, app.width  * 3 / 4, app.height * 0.6)
    drawLine(app.width / 4, app.height * 0.8, app.width  * 3 / 4, app.height * 0.8)
    drawCircle(app.customSlider1, app.height * 0.6, 10, fill = "red")
    drawCircle(app.customSlider2, app.height * 0.8, 10, fill = "red")
    drawRect(app.width / 2 - 100, app.height * 0.9, 200, 50, fill = "white")
    drawLabel("Create", app.width / 2, app.height * 0.935, size = 30, fill = "black", bold = True)
    drawCircle(app.width - 100, app.height - 100, 70, fill = "red")
    drawLabel("Press V to toggle between voice and AI", app.width / 2, app.height * 0.3, size = 20, fill = "black")
    if app.voice == True:
        drawLabel("Voice toggled", app.width - 100, app.height - 100, size = 20, fill = "black")
    else:
        drawLabel("AI toggled", app.width - 100, app.height - 100, size = 20, fill = "black")
def updatePivotNum(app, x):
    proportion = (x - app.width / 4) / (app.width / 2)
    app.customPiv =  5 + rounded(5 * proportion)

def updateLenNum(app, x):
    proportion = (x - app.width / 4) / (app.width / 2)
    app.customLen =  1000 + rounded(1000 * proportion)
    
def creationStage(app):
    drawRect(0, 0, app.customLen, app.height, fill = "lightblue")
    drawLabel("Click to place or remove a pivot", app.width/2 , app.height * 0.1, size = 20, fill = "black")
    left = app.customPiv - len(app.createPivots)
    drawLabel(f"Pivots left: {left}", app.width/2 , app.height * 0.15, size = 20, fill = "black")
    drawLabel(f"Level Left: {app.customLen - app.customcameraX}", app.width/2 , app.height * 0.2, size = 20, fill = "black")
    drawLabel("Press S to Start", app.width/2 , app.height * 0.25, size = 20, fill = "black")
    for pivot in app.createPivots:
        drawCircle(pivot[0] - app.customcameraX, pivot[1], 10, fill="yellow")
    
    
def gameOver(app):
    drawRect(0, 0, app.width, app.height, fill = "black")
    drawLabel("Game Over", app.width/2, app.height / 2, fill = "white", size = 30, bold = True)
    drawLabel("Press r to reset", app.width / 2, app.height * 0.7, size = 15, fill = "white")


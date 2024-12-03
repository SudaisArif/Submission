from cmu_graphics import *
from utilities import *

def drawLevelSelectionMenu(app):
    drawRect(0, 0, app.width, app.height, fill="lightblue")
    drawLabel("Select a Level", app.width / 2, 30, size=40, bold=True,
              fill="darkblue")
    if app.handPlay:
        drawLabel("Press H to deactivate Hand Cam", app.width / 2, 60 , size = 20, fill = "darkBlue")
    else:
        drawLabel("Press H to activate Hand Cam", app.width / 2, 60 , size = 20, fill = "darkBlue")
    if app.collision:
        drawLabel("Press C to activate collisions", app.width / 2, 80 , size = 20, fill = "darkBlue")
    else:
        drawLabel("Press C to deactivate collisions", app.width / 2, 80 , size = 20, fill = "darkBlue")
    drawCircle(app.width - 100, app.height - 100, 70, fill = "red")
    drawLabel(f"Hand: {app.handPlay}", app.width - 100, app.height - 100, size = 20, fill = "black")
    drawCircle(100, app.height - 100, 70, fill = "red")
    drawLabel(f"Collisions: {app.collision}", 100, app.height - 100, size = 20, fill = "black")
    buttonWidth = 150
    buttonHeight = 50
    gap = 20

    for i in range(len(app.levels)):
        x = app.width / 2 - buttonWidth / 2
        y = 100 + i * (buttonHeight + gap)
        # Check completion status for each level
        color = "green" if app.completedLevels[i] else "red"
        drawRect(x, y, buttonWidth, buttonHeight, fill=color, border="black",
                 borderWidth=2)
        drawLabel(f"Level {i + 1}", x + buttonWidth / 2, y + buttonHeight / 2,
                  size=20, fill="white")

def handleLevelSelection(app, mouseX, mouseY):
    buttonWidth = 150
    buttonHeight = 50
    gap = 20

    for i in range(len(app.levels)):
        x = app.width / 2 - buttonWidth / 2
        y = 100 + i * (buttonHeight + gap)

        if x <= mouseX <= x + buttonWidth and y <= mouseY <= y + buttonHeight:
            app.currentLevel = i
            app.startGame = True
            app.inLevelSelection = False
            reset(app, stored = True)
            return

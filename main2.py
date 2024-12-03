from cmu_graphics import *
from level2 import *
from levelselection import *
from utilities import *
import math
from random import *
from PIL import Image as PilImage
from design import *
#from speech2 import *
from speech import * 
from hand import *
from ai import *

def onAppStart(app):
    initialise(app)

def initialise(app):
    #app.speech_recognition = SpeechRecognition()
    #app.speech_recognition.start_listening()
    app.frame = 0
    app.birdStart = 0 
    app.ballR = 15
    app.startGame = False
    app.inMainMenu = True #Change to True
    app.inLevelSelection = False
    app.currentLevel = 0
    reset(app)  # Reset the game to initialise everything
    app.title = "Swing and Surf"
    app.buttonWidth = 200
    app.buttonHeight = 50
    app.buttonX = app.width / 2 - app.buttonWidth / 2
    app.buttonY = app.height * 0.7
    app.buttonColor = "white"
    app.buttonTextColor = "darkblue"
    # Initialize completedLevels to be a list of False for each level
    app.completedLevels = [False] * len(app.levels)
    app.inCustom = False
    app.customPiv = 5
    app.customLen = 1000
    app.customSlider1 = app.width / 4
    app.customSlider2 = app.width / 4
    app.inCreation = False
    app.customcameraX = 0
    app.createPivots = []
    app.over = False
    app.collision = True
    app.voice = False
    app.gunshots = 0
    app.kill = False
    app.killx = None
    app.killy = None
    #app.shootsound = Sound("shotgun2.mp3")
    app.mainsound = Sound("toreup.mp3")
    app.mainImage = openImage("fast3.png")
    app.mainbg = CMUImage(app.mainImage)
    app.collisionsound = Sound("fastsound.mp3")
    app.aiPlayer = AI()
    app.handPlay = False
    app.frozen = False
def onStep(app):
    if app.startGame:
        if app.currentLevel == 5 and app.voice == True:
            
            if not hasattr(app, 'speech_recognition'):
                app.speech_recognition = FastSpeechRecognition(r"C:\Users\sudai\Downloads\112HW\vosk-model-small-en-us-0.15")
            command = app.speech_recognition.get_last_command()
            print(f"Command captured: {command}")
            if command and "swing" in command and not app.isSwinging:
                currentLevel = app.levels[app.currentLevel]
                if currentLevel.isSwingable(app):
                    app.isSwinging = True
                    app.swingPivot = currentLevel.closestPivot(app)
                    app.swingAngle = math.atan2(
                       app.ballPos[1] - app.swingPivot[1],
                        app.ballPos[0] - app.swingPivot[0]
                    )
                    app.swingLen = math.dist(app.ballPos, app.swingPivot)
                    
            if command and "stop" in command and app.isSwinging:
                app.isSwinging = False
                releaseAngle = app.swingAngle
                tangentialSpeed = app.swingLen * 0.05
                app.ballVel[0] = tangentialSpeed * math.cos(releaseAngle)
                app.ballVel[1] = -tangentialSpeed * math.sin(releaseAngle)
        elif app.currentLevel == 5:
             if hasattr(app, "aiPlayer"):
                app.aiPlayer.decideAction(app)
                app.aiPlayer.executeAction(app)
                


        
        if app.handPlay:
        
            if not hasattr(app, 'gestureRecognition'):
            # Initialize hand gesture recognition for gestures
                    app.gestureRecognition = HandGestureRecognition(
                    lambda: handleSpidermanGesture(app),  # Callback for Spiderman gesture
                    lambda: handleGunGesture(app),       # Callback for Gun gesture
                    lambda: releaseSwing(app) if app.currentGesture == "spiderman" else decreaseLine(app)  # On release
                )
            

        app.birdStart += 1
        app.birdStart = app.birdStart % 4
        currentLevel = app.levels[app.currentLevel]
        currentLevel.updatePhysics(app)

        # Camera can moves forward or back
        app.cameraX = max(0, app.ballPos[0] - app.width / 2)

        # Check for level completion
        if app.ballPos[0] >= currentLevel.finishLineX:
            app.completedLevels[app.currentLevel] = True
            app.currentLevel += 1
        
            # Move to the next level
            if app.currentLevel > 5:
                app.over = True
                app.currentLevel = 0
                app.inLevelSelection = True
            # If there are no more levels, return to the main menu
            if app.currentLevel >= len(app.levels):
                if len(app.levels) <= 6:
                    app.inCustom = True
                    
                
                app.currentLevel = 0  # Reset to the first level
                app.startGame = False

                print("All levels completed! Returning to level selection.")
            else:
                app.levels[app.currentLevel].resetLevel()
                app.startGame = True
                reset(app)  # Reset the app for the next level
                print(f"Level {app.currentLevel + 1} starts!")

        # Check if the player falls off-screen
        if app.ballPos[1] > app.height:
            print("Player fell off! Restarting level.")
            app.startGame = False
            app.inLevelSelection = True
            reset(app, stored =True)  # Reset the current level
            app.levels[app.currentLevel].resetLevel()
        
        for bird in app.birds:
            bird["x"] -= bird["speed"]
            if bird["x"] < -50:
                bird['x'] = app.width + 50
                bird['y'] = randint(50, app.height - 50)
                
            # Check collision with the ball
            if app.collision:
                if checkCollisionBird(app.ballPos, app.ballR, bird['x'], bird['y'], 20):  # Bird radius = 20
                    app.collisionsound.play()
                    app.startGame = False  # Lose condition
                    app.inLevelSelection = True

        app.snowman.updateSnowman(app)
    elif app.inMainMenu:
        pass
        #app.mainsound.play(loop=True)
def decreaseLine(app):
    app.remainingLine -= 50
                
def checkCollisionBird(ballPos, ballR, birdX, birdY, birdR):
    dist = math.dist(ballPos, (birdX, birdY))
    return dist < ballR + birdR

def handleSpidermanGesture(app):
    app.currentGesture = "spiderman"
    app.frozen = False
    if not app.isSwinging:
        currentLevel = app.levels[app.currentLevel]
        if currentLevel.isSwingable(app):
            app.isSwinging = True
            app.swingPivot = currentLevel.closestPivot(app)
            app.swingAngle = math.atan2(
                app.ballPos[1] - app.swingPivot[1],
                app.ballPos[0] - app.swingPivot[0]
            )
            app.swingLen = math.dist(app.ballPos, app.swingPivot)
            print("Swinging triggered by Spiderman symbol!")

def handleGunGesture(app):
    app.currentGesture = "gun"
    if app.gunshots < 10:
        if len(app.birds) >= 1:
            closestBird = 0
            closestBirdDist = math.dist((app.birds[0]["x"], app.birds[0]["y"]), app.ballPos)
            for i in range(1, len(app.birds)):
                if math.dist((app.birds[i]["x"], app.birds[i]["y"]), app.ballPos) < closestBirdDist:
                    closestBirdDist = math.dist((app.birds[i]["x"], app.birds[i]["y"]), app.ballPos)
                    closestBird = i
            app.gunshots += 1
            app.killx = app.birds[closestBird]["x"]
            app.killy = app.birds[closestBird]["y"]

            app.birds.pop(closestBird)
        
        for carrot in app.snowman.carrots:
            carrot['vx'] = 0
            carrot['vy'] = 0
            app.frozen = True
            print("CX", carrot['vx'])
            print("CY", carrot['vy'])
def releaseSwing(app):
    if app.isSwinging:
        app.isSwinging = False
        releaseAngle = app.swingAngle
        tangentialSpeed = app.swingLen * 0.05
        app.ballVel[0] = tangentialSpeed * math.cos(releaseAngle)
        app.ballVel[1] = -tangentialSpeed * math.sin(releaseAngle)
        print("Swing released!")
            
def redrawAll(app):
    if app.over:
        gameOver(app)
    elif app.inLevelSelection:
        drawLevelSelectionMenu(app)
    elif app.inMainMenu:
        # Main menu
        drawRect(0, 0, app.width, app.height, fill="black")
        drawImage(app.mainbg, 0, 0, width= app.width, height = app.height)
        #drawRect(0, 0, app.width, app.height, fill=gradient("lightblue",
                                                            #"blue", "darkblue",
                                                            #start="left-top"))
        #drawLabel(app.title, app.width / 2, app.height * 0.3, size=50,
                  #font="monospace", bold=True, fill="white")
        drawRect(app.buttonX, app.buttonY, app.buttonWidth,
                 app.buttonHeight, fill=app.buttonColor, border="black")
        drawLabel("Start Game", app.buttonX + app.buttonWidth / 2,
                  app.buttonY + app.buttonHeight / 2,
                  size=20, fill=app.buttonTextColor)
    elif app.inCustom:
        showLevelCreator(app)
    elif app.inCreation:
        creationStage(app)
    else:
        currentLevel = app.levels[app.currentLevel]
        currentLevel.drawLevel(app)
        
        # Draw the swinging line if the player is swinging
        if app.isSwinging:
        
            drawLine(
                app.ballPos[0] - app.cameraX, app.ballPos[1],
                # Ball's position relative to the camera
                app.swingPivot[0] - app.cameraX, app.swingPivot[1],
                # Pivot's position relative to the camera
                fill="green", lineWidth=3
            )
            drawCircle(app.ballPos[0] - app.cameraX, app.ballPos[1], app.ballR,
                       fill="red")
        elif app.surfing:
            drawCircle(app.ballPos[0] - app.cameraX, app.ballPos[1], app.ballR,
                       fill="red")
            #drawImage(app.surfer, app.ballPos[0] - app.cameraX, app.ballPos[1],
            #width = 70, height = 70)
            
        # Ball position relative to the camera
        else:
    
            drawImage(app.flier, app.ballPos[0] - app.cameraX, app.ballPos[1],
                      width = 100, height = 100)
            
        if app.currentLevel < 5:
            app.snowman.drawSnowman(app)
            for bird in app.birds:
                drawImage(app.birdImages[app.birdStart], bird['x'] - app.cameraX,
                          bird['y'], width = 40, height = 40)
        
        if app.killx != None and app.killy != None:
            #app.shootsound.play()
            for blood in app.bloods:
                drawImage(blood, app.killx - app.cameraX, app.killy, width=60, height=60)
                
        # Remaining line length
        drawLabel(f"Line: {int(app.remainingLine)}", app.width - 100, 20,
                  size=16, fill="white")
        if app.collision:
            drawLabel(f"Collision: ON", 100, 20,
                  size=16, fill="white")
        else:
            drawLabel(f"Collision: Off", 100, 20,
                  size=16, fill="white")
        
        drawLabel(f"Gun shots left: {10 - app.gunshots}", app.width - 100, app.height - 20, size = 16, fill = "black")
        
def onMousePress(app, mouseX, mouseY):
    if app.inMainMenu:
        # Check if Start Game button is clicked
        if (app.buttonX <= mouseX <= app.buttonX + app.buttonWidth and
                app.buttonY <= mouseY <= app.buttonY + app.buttonHeight):
            app.inMainMenu = False
            app.inLevelSelection = True
    elif app.inLevelSelection:
        handleLevelSelection(app, mouseX, mouseY)
    elif app.inCustom:
        if  app.width / 4 <= mouseX <= app.width * 3 / 4 and app.height * 0.57 <= mouseY <= app.height * 0.63:
            app.customSlider1 = mouseX
            updatePivotNum(app, mouseX)
        elif app.width / 4 <= mouseX <= app.width * 3 / 4 and app.height * 0.77 <= mouseY <= app.height * 0.83:
            app.customSlider2 = mouseX
            updateLenNum(app, mouseX)
        elif app.width / 2 - 100 <= mouseX <= app.width / 2 + 100 and app.height * 0.9 <= mouseY <= app.height * 0.9 + 200:
            app.inCreation = True
            app.inCustom = False
    if app.inCreation:
        removed = False
        for pivot in app.createPivots[:]:
            if abs(mouseX - (pivot[0] - app.customcameraX)) < 10 and abs(mouseY - pivot[1]) < 10:
                app.createPivots.remove(pivot)
                removed = True
                break
        if removed ==  False:
            if len(app.createPivots) < app.customPiv:
                app.createPivots.append((mouseX + app.customcameraX, mouseY))
            
    elif app.startGame:
        app.isDrawing = True
        app.levels[app.currentLevel].lines = [(mouseX + app.customcameraX, mouseY)]
    

def onMouseDrag(app, mouseX, mouseY):
    if app.currentLevel < 5:
        if app.isDrawing and app.remainingLine > 0:
            currentLevel = app.levels[app.currentLevel]
            if len(currentLevel.lines) == 0:
                currentLevel.lines = [(mouseX + app.customcameraX, mouseY)]
            lastX, lastY = currentLevel.lines[-1]
            partLen = math.dist((lastX, lastY), (mouseX + app.cameraX, mouseY))
            print(len(currentLevel.lines))
            if len(currentLevel.lines) <= 25:
                if app.remainingLine >= partLen:
                    currentLevel.lines.append((mouseX + app.cameraX, mouseY))
                    app.remainingLine -= partLen
                else:
                    ratio = app.remainingLine / partLen
                    projX = lastX + ratio * (mouseX + app.cameraX - lastX)
                    projY = lastY + ratio * (mouseY - lastY)
                    currentLevel.lines.append((projX, projY))
                    app.remainingLine = 0
            
            
            for bird in app.birds[:]:  # Use a copy of the list to safely remove items
                if checkLineIntersectsCircle(lastX, lastY, mouseX + app.cameraX, mouseY, bird['x'], bird['y'], 20):
            
                    app.killx = bird['x']
                    app.killy = bird['y']
                    app.birds.remove(bird)  # Remove the bird
                    app.remainingLine -= 50  # Deduct line length for slashing

                
def onMouseRelease(app, mouseX, mouseY):
    app.isDrawing = False
    #currentLevel = app.levels[app.currentLevel]
    #currentLevel.lines = [(mouseX + app.customcameraX, mouseY)]
    
        
def onKeyPress(app, key):
    if app.inLevelSelection:
        if key == "c":
            app.collision = not app.collision
            print(app.collision)
        if key == "h":
            app.handPlay = not app.handPlay
    if app.inCreation:
        if key == "s":
            app.completedLevels.append(False)
            app.levels.append(Level(app.createPivots, finishLineX = app.customLen))
            app.inLevelSelection = True
            app.inCreation = False
    if app.inCustom:
        if key == "v":
            app.voice = not app.voice
            print(app.voice)
    if app.over:
        if key == "r":
            app.gameOver = True
            initialise(app)
            
            
def onKeyHold(app, keys):
    if "space" in keys and not app.isSwinging:
        currentLevel = app.levels[app.currentLevel]
        if currentLevel.isSwingable(app):
            app.isSwinging = True
            app.swingPivot = currentLevel.closestPivot(app)
            app.swingAngle = math.atan2(app.ballPos[1] - app.swingPivot[1],
                                        app.ballPos[0] - app.swingPivot[0])
            app.swingLen = math.dist(app.ballPos, app.swingPivot)
    if app.inCreation:
        if "right" in keys:
            app.customcameraX = min(app.customcameraX + 10, app.customLen - 400)
        if "left" in keys:
            app.customcameraX = max(app.customcameraX - 10, 0)
            
def onKeyRelease(app, key):
    if key == "space" and app.isSwinging:
        app.isSwinging = False
        releaseAngle = app.swingAngle
        tangentialSpeed = app.swingLen * 0.05
        app.ballVel[0] = tangentialSpeed * math.cos(releaseAngle)
        app.ballVel[1] = -tangentialSpeed * math.sin(releaseAngle)

def checkLineIntersectsCircle(x1, y1, x2, y2, cx, cy, radius):
    #Calculate the distance from the line to the circle center
    dx, dy = x2 - x1, y2 - y1
    fx, fy = x1 - cx, y1 - cy

    a = dx**2 + dy**2
    b = 2 * (fx * dx + fy * dy)
    c = fx**2 + fy**2 - radius**2
    
    if a == 0:
        # Check if the point (x1, y1) is within the circle
        dist = math.sqrt((x1 - cx)**2 + (y1 - cy)**2)
        return dist <= radius
    
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return False  # No intersection

    discriminant = math.sqrt(discriminant)
    t1 = (-b - discriminant) / (2 * a)
    t2 = (-b + discriminant) / (2 * a)

    # Check if the circle intersects the line segment
    return (0 <= t1 <= 1) or (0 <= t2 <= 1)

runApp(width=800, height=600)
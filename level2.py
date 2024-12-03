from cmu_graphics import *
import math

class Level:
    def __init__(self, pivots, finishLineX):
        self.pivots = pivots
        self.finishLineX = finishLineX
        self.lines = []

    def resetLevel(self):
        self.lines = []

    def updatePhysics(self, app):
        if not app.isSwinging:
            app.ballVel[1] += app.gravity
            app.ballPos[0] += app.ballVel[0]
            app.ballPos[1] += app.ballVel[1]
        else:
            app.swingAngle -= 0.05
            app.ballPos[0] = app.swingPivot[0] + app.swingLen * math.cos(app.swingAngle)
            app.ballPos[1] = app.swingPivot[1] + app.swingLen * math.sin(app.swingAngle)

        self.checkCollision(app)

    def drawLevel(self, app):

        # Draw background
        if app.currentLevel <= 4:
            drawImage(app.bgImages[app.currentLevel], 0, 0, width=app.width, height=app.height)
        else:
            drawRect(0, 0, app.width, app.height, fill="lightblue")

        for line in self.lines:
            if len(self.lines) > 1:
                for i in range(1, len(self.lines) - 1):
                    x1, y1 = self.lines[i]
                    x2, y2 = self.lines[i + 1]
                    drawLine(x1 - app.cameraX, y1, x2 - app.cameraX, y2, fill="black")
        for pivot in self.pivots:
            drawCircle(pivot[0] - app.cameraX, pivot[1], 10, fill="yellow")
        self.drawDottedLine(app)
        
    def drawDottedLine(self, app):
        segmentLength = 5
        gapLength = 2
        for x in range(self.finishLineX, self.finishLineX + 200, segmentLength + gapLength):
            drawLine(x - app.cameraX, 0, x - app.cameraX, app.height, fill="black")

    def closestPivot(self, app):
        return min(self.pivots, key=lambda p: math.dist(p, app.ballPos))

    def isSwingable(self, app):
        return any(math.dist(p, app.ballPos) <= 300 for p in self.pivots)

    def checkCollision(self, app):
        for i in range(1, len(self.lines) - 1):
            x1, y1 = self.lines[i]
            x2, y2 = self.lines[i + 1]

            # Handle x-range
            if min(x1, x2) - app.ballR <= app.ballPos[0] <= max(x1, x2) + app.ballR:
                dx = x2 - x1
                dy = y2 - y1

                # Handle vertical lines
                if dx == 0:
                    yAtBallX = min(y1, y2)
                else:
                    slope = dy / dx
                    yAtBallX = slope * (app.ballPos[0] - x1) + y1

                # Check collision in the y-range
                if yAtBallX - app.ballR <= app.ballPos[1] <= yAtBallX + app.ballR:
                    # Adjust ball position
                    app.ballPos[1] = yAtBallX - app.ballR

                    # Calculate bounce angle
                    angle = math.atan2(dy, dx) if dx != 0 else math.pi / 2
                    app.ballVel[0] = 8 * math.cos(angle)
                    app.ballVel[1] = 8 * math.sin(angle)

                    
                    app.surfing = True
                    break
        else:
            #stop surfing
            
            app.surfing = False

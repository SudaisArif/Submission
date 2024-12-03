from cmu_graphics import *
import math
from utilities import *

class Snowman:
    def __init__(self, x, y, shoot_interval=50):
        self.x = x
        self.y = y
        self.shoot_interval = shoot_interval  # Time in seconds between carrot shots
        self.time_since_last_shot = 0
        self.carrots = []  # List of carrots

    def drawSnowman(self, app):
        # Draw the snowman
        #drawImage(app.Snow, self.x - app.cameraX, self.y, width = 400, height = 400)
        drawImage(app.Snow, self.x - app.cameraX, self.y - 100, width = 200, height = 200)
        # Draw all active carrots
        for carrot in self.carrots:
            drawImage(app.carrot, carrot["x"] - app.cameraX, carrot["y"], width = 35, height = 35)
            #drawCircle(carrot["x"] - app.cameraX, carrot["y"], 10, fill="orange")  # Carrot bullet

    def updateCarrots(self, app):
        if not app.frozen:
            for carrot in self.carrots[:]:  # Iterate over a copy to allow removal
                # Homing behavior: adjust velocity to move toward the player
                dx = app.ballPos[0] - carrot["x"]
                dy = app.ballPos[1] - carrot["y"]
                dist = math.sqrt(dx**2 + dy**2)

                if dist > 0:
                    carrot["vx"] = 2 * (dx / dist)  # Normalize and scale velocity
                    carrot["vy"] = 2 * (dy / dist)

                # Update carrot position
                carrot["x"] += carrot["vx"]
                carrot["y"] += carrot["vy"]

                # Check if the carrot collides with a line
                for i in range(len(app.levels[app.currentLevel].lines) - 1):
                    x1, y1 = app.levels[app.currentLevel].lines[i]
                    x2, y2 = app.levels[app.currentLevel].lines[i + 1]
                    if self.checkLineCollision(carrot, x1, y1, x2, y2):
                        self.carrots.remove(carrot)
                        break
                    
                
                if app.collision:
                    if math.dist((carrot["x"], carrot["y"]), app.ballPos) < app.ballR + 5:
                        app.collisionsound.play()
                        app.startGame = False  # Player loses
                        app.inLevelSelection = True

    def checkLineCollision(self, carrot, x1, y1, x2, y2):
        """Check if a carrot collides with a line segment."""
        # Vector math to find the closest point on the line
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:  # Line segment is a point
            return math.dist((carrot["x"], carrot["y"]), (x1, y1)) < 5

        # Project carrot position onto the line
        t = max(0, min(1, ((carrot["x"] - x1) * dx + (carrot["y"] - y1) * dy) / (dx**2 + dy**2)))
        closestX = x1 + t * dx
        closestY = y1 + t * dy

        # Check distance to the closest point
        return math.dist((carrot["x"], carrot["y"]), (closestX, closestY)) < 5

    def shootCarrot(self):
        # Shoot a new carrot
        self.carrots.append({"x": self.x, "y": self.y - 40, "vx": 0, "vy": 0})

    def updateSnowman(self, app):
        # Update the timer and shoot carrots at intervals
        self.time_since_last_shot += 1
        if self.time_since_last_shot >= self.shoot_interval:
            self.shootCarrot()
            self.time_since_last_shot = 0

        # Update all carrot positions and check collisions
        self.updateCarrots(app)

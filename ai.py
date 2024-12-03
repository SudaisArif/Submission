import math

class AI:
    def __init__(self):
        self.action = None  # Current action ('swing', 'release', or None)
        self.targetAngle = None  # Target release angle
        self.releaseCooldown = 0  

    def decideAction(self, app):
        if self.releaseCooldown > 0:
            self.releaseCooldown -= 1  # Decrement cooldown
            return

        currentLevel = app.levels[app.currentLevel]

        if app.isSwinging:
            # Check if the release angle is optimal
            releaseAngle = math.atan2(
                app.ballPos[1] - app.swingPivot[1],
                app.ballPos[0] - app.swingPivot[0]
            )

            # Ideal release 
            if releaseAngle >= -math.pi / 4 and releaseAngle <= math.pi / 4:
                self.action = 'release'
                self.releaseCooldown = 30  # Prevent immediate re-swing
                
            else:
                self.action = 'swing'  # Continue swinging
        else:
            # Check if swinging is possible
            if currentLevel.isSwingable(app):
                self.action = 'swing'
                app.swingPivot = currentLevel.closestPivot(app)
                app.swingAngle = math.atan2(
                    app.ballPos[1] - app.swingPivot[1],
                    app.ballPos[0] - app.swingPivot[0]
                )
                app.swingLen = math.dist(app.ballPos, app.swingPivot)
                

    def executeAction(self, app):
        if self.action == 'swing' and not app.isSwinging:
            app.isSwinging = True
        elif self.action == 'release' and app.isSwinging:
            app.isSwinging = False
            # Calculate the release velocity
            tangentialSpeed = app.swingLen * 0.05
            releaseAngle = app.swingAngle
            app.ballVel[0] = tangentialSpeed * math.cos(releaseAngle)
            app.ballVel[1] = -tangentialSpeed * math.sin(releaseAngle)
            


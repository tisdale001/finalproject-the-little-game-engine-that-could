import time
from datetime import datetime

from lib import engine



class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def getTimeMS():
    # return int(datetime.now().microsecond / 1000)
    # return int(time.time_ns() / 1000000) # TODO: might need more testing, so far SDL_getTicks is best for performance
    pass

class Player:
    def __init__(self, replayFrames):
        self.obj = engine.GameObject()
        self.transform = engine.Transform()
        self.obj.addTransformComponent(self.transform)
        self.transform.xPos = 0
        self.transform.yPos = 160
        self.rectangle = engine.RectangleComponent(self.transform)
        self.rectangle.setDimensions(25, 25)
        self.obj.addRectangleComponent(self.rectangle)
        self.physics = engine.PhysicsComponent()
        self.obj.addPhysicsComponent(self.physics)
        self.camera = engine.StaticCamera()
        self.obj.addCamera(self.camera)
        self.replayFrames = replayFrames
        self.currFrame = replayFrames[0]


class Game:
    def __init__(self, windowWidth, windowHeight):
        # Create game objects
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.player = engine.GameObject()
        self.level = engine.GameObject()

        self.transform = engine.Transform()
        self.player.addTransformComponent(self.transform)
        self.transform.xPos = 0
        self.transform.yPos = int(windowHeight/2)

        self.rectangle = engine.RectangleComponent(self.transform)
        self.rectangle.setDimensions(25, 25)
        self.player.addRectangleComponent(self.rectangle)

        self.tilemap = engine.TileMapComponent("Assets/Levels/MarioTiles/replay_test.lvl")
        self.tilemap.loadTileset("Assets/tilesets/mario-like-tileset-32x32.png", self.sdl.getSDLRenderer())
        self.level.addTileMapComponent(self.tilemap)
        self.tileSize = self.tilemap.getSize()

        self.physics = engine.PhysicsComponent()
        self.player.addPhysicsComponent(self.physics)

        self.camera = engine.StaticCamera()
        self.player.addCamera(self.camera)
        self.level.addCamera(self.camera)

        self.sdl.addGameObject(self.player)
        self.sdl.addGameObject(self.level)

        # Setup game state
        self.playerSpeed = 3
        targetFPS = 60
        self.maxTicksPerFrame = int(1000 / targetFPS); # 16.66ms per frame
        self.frameStartTime = 0
        self.frame_count = 0
        self.startTime = self.sdl.getTimeMS() # TODO: Is it better to use python time function?

    # Delay game loop to reach target fps
    def limitFPS(self):
        frameTicks = self.sdl.getTimeMS() - self.frameStartTime
        if frameTicks < self.maxTicksPerFrame:
            self.sdl.delay(self.maxTicksPerFrame - frameTicks)
        else:
            print(f"Exceeding frametime: {frameTicks} ms")
        self.frame_count += 1
        timeElapsed = self.sdl.getTimeMS() - self.startTime
        fps = self.frame_count / (timeElapsed / 1000)
        # self.sdl.setTitle("%.2f"%(fps))

    def replayComplete(self):
        replayStatus = []
        for entity in self.replayEntities:
            replayStatus.append(entity.currFrame == entity.replayFrames[1])
        return all(replayStatus)

    def runLoop(self):
        inputs = self.sdl.getInput()
        self.replayFrames = []
        self.replayMode = False
        self.replayStartFrame = 0
        while not inputs[engine.QUIT_EVENT]:
            self.frameStartTime = self.sdl.getTimeMS()
            self.update(self.player, inputs := self.sdl.getInput())
            self.render()
            self.limitFPS()

        # Replay
        if self.replayMode:
            self.replayEntities = []
            for replay in self.replayFrames:
                replayPlayer = Player(replay)
                self.replayEntities.append(replayPlayer)
                self.sdl.addGameObject(replayPlayer.obj)

            while not self.replayComplete():
                self.frameStartTime = self.sdl.getTimeMS()
                for entity in self.replayEntities:
                    if entity.currFrame < entity.replayFrames[1]:
                        self.update(entity.obj, self.sdl.getInputAtFrame(entity.currFrame))
                        entity.currFrame += 1
                self.render()
                self.limitFPS()


    def update(self, player, inputs):
        player.xVel = 0
        player.yVel = 0
        if inputs[engine.ESCAPE_PRESSED]:
            inputs[engine.QUIT_EVENT] = True
            self.replayMode = True
        if inputs[engine.W_PRESSED]:
            player.yVel = -self.playerSpeed
        if inputs[engine.S_PRESSED]:
            player.yVel = self.playerSpeed
        if inputs[engine.A_PRESSED]:
            player.xVel = -self.playerSpeed
        if inputs[engine.D_PRESSED]:
            player.xVel = self.playerSpeed

        # Record replay if player crosses end
        if not self.replayMode and (player.mTransform.xPos > self.windowWidth):
            # player.mTransform.xPos = 0
            # player.mTransform.yPos = int(self.windowHeight/2)
            player.mTransform.setPosition(0, int(self.windowHeight/2))
            self.replayFrames.append((self.replayStartFrame, self.frame_count + 1))
            self.replayStartFrame = self.frame_count + 1

        # Handle x and y collisions separately so we can slide along tiles and into corners
        # Handle x-axis collisions
        player.mPhysicsComponent.UpdateX(player)
        collision = self.tilemap.checkCollision(player)
        if collision.isColliding:
            if player.xVel < 0:
                player.mTransform.xPos = (collision.firstTileColumn + 1) * self.tilemap.getSize()
            elif player.xVel > 0:
                player.mTransform.xPos = collision.firstTileColumn * self.tilemap.getSize() - player.mRectangle.getWidth()

        # Handle y-axis collisions
        player.mPhysicsComponent.UpdateY(player)
        collision = self.tilemap.checkCollision(player)
        if collision.isColliding:
            if player.yVel < 0:
                player.mTransform.yPos = (collision.firstTileRow + 1) * self.tilemap.getSize()
            elif player.yVel > 0:
                player.mTransform.yPos = collision.firstTileRow * self.tilemap.getSize() - player.mRectangle.getHeight()

        #     # hit right wall: set xPos to correct x according to row, col
        #     self.transform.xPos = self.tileSize * collision.col - self.rectangle.getWidth()
        #     # change isClimbingRight only once
        #     if not self.isClimbingRight:
        #         self.isClimbingRight = True
        #         # check if on ground or ceiling
        #         if not (self.tilemap.isOnCeiling(self.player) or self.tilemap.isOnGround(self.player)):
        #             self.curYDirection *= -1
        #     self.isClimbingLeft = False
        # elif collision.isColliding and self.player.xVel < 0:
        #     # hit left wall
        #     self.transform.xPos = self.tileSize * (collision.col + 1)
        #     # change isClimbingLeft only once
        #     if not self.isClimbingLeft:
        #         self.isClimbingLeft = True
        #         # check if on ground or ceiling
        #         if not (self.tilemap.isOnCeiling(self.player) or self.tilemap.isOnGround(self.player)):
        #             self.curYDirection *= -1
        #     self.isClimbingRight = False
        # # check if falling off wall (pushing opposite direction than climbing wall)
        # if self.isClimbingRight and not self.tilemap.isTouchingRightWall(self.player):
        #     self.isClimbingRight = False
        #     if self.player.xVel < 0:
        #         # player jumped off wall
        #         # self.curYDirection *= -1
        #         self.player.yVel = self.playerJumpSpeed * self.curYDirection
        #     elif self.player.xVel > 0:
        #         # player reached top of wall
        #         # self.curYDirection *= -1
        #         self.player.yVel = self.playerJumpSpeed * self.curYDirection
        #     else:
        #         # player is not pushing left or right
        #         self.player.yVel = 0
        #         self.curYDirection *= -1
        # elif self.isClimbingLeft and not self.tilemap.isTouchingLeftWall(self.player):
        #     self.isClimbingLeft = False
        #     if self.player.xVel > 0:
        #         # player jumped off wall
        #         # self.curYDirection *= -1
        #         self.player.yVel = self.playerJumpSpeed * self.curYDirection
        #     elif self.player.xVel < 0:
        #         # player reached top of wall
        #         # self.curYDirection *= -1
        #         self.player.yVel = self.playerJumpSpeed * self.curYDirection
        #     else:
        #         # player is not pushing left or right
        #         self.player.yVel = 0
        #         self.curYDirection *= -1

        # update player yPos
        # self.physics.UpdateY(self.player)
        # check if off screen
        # if self.transform.yPos <= 0 or self.transform.yPos >= self.lvlHeight - self.rectangle.getHeight():
        #     # death: respawn
        #     self.transform.xPos = 100
        #     self.transform.yPos = 100
        # collision = self.tilemap.checkCollision(self.player)
        # if collision.isColliding and self.player.yVel < 0:
        #     # hit ceiling: set yPos to correct y according to row, col
        #     self.transform.yPos = self.tileSize * (collision.row + 1)
        # elif collision.isColliding and self.player.yVel > 0:
        #     # hit floor
        #     self.transform.yPos = self.tileSize * (collision.row) - self.rectangle.getHeight()

    def render(self):
        self.sdl.clear(32, 32, 32, 255) # Set background to gray
        self.sdl.Render()
        self.sdl.flip()

def main():
    game = Game(640, 320)
    game.runLoop()


if __name__ == "__main__":
    main()
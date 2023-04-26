import os
import random

from lib import engine

class Player:
    def __init__(self, replayFrames, camera):
        self.obj = engine.GameObject()
        self.transform = engine.Transform()
        self.obj.addTransformComponent(self.transform)
        self.transform.xPos = 35
        self.transform.yPos = 263
        self.rectangle = engine.RectangleComponent(self.transform)
        self.rectangle.setDimensions(25, 25)
        self.rectangle.setColor(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.obj.addRectangleComponent(self.rectangle)
        self.physics = engine.PhysicsComponent()
        self.obj.addPhysicsComponent(self.physics)
        # self.camera = engine.StaticCamera()
        self.obj.addCamera(camera)
        self.replayFrames = replayFrames
        self.currFrame = replayFrames[0]


class Enemy:
    def __init__(self, x, y, leftX, rightX, camera):
        self.obj = engine.GameObject()
        self.transform = engine.Transform()
        self.obj.addTransformComponent(self.transform)
        self.startX = x
        self.startY = y
        self.transform.xPos = x
        self.transform.yPos = y
        self.rectangle = engine.RectangleComponent(self.transform)
        self.rectangle.setDimensions(25, 25)
        self.rectangle.setColor(255, 0, 0, 255)
        self.obj.addRectangleComponent(self.rectangle)
        self.physics = engine.PhysicsComponent()
        self.obj.addPhysicsComponent(self.physics)
        self.obj.addCamera(camera)
        self.leftX = leftX
        self.rightX = rightX
        self.xVel = 3

    def resetPosition(self):
        self.transform.xPos = startX
        self.transform.yPos = startY

    def update(self):
        self.transform.xPos += self.xVel
        if self.transform.xPos >= self.rightX or self.transform.xPos <= self.leftX:
            self.xVel *= -1

class Command:
    def execute():
        pass

    def undo():
        pass

    def redo():
        pass

class MoveCommand(Command):
    def __init__(self, gameObject, xPos, yPos):
        self.gameObject = gameObject
        self.xPos = xPos
        self.yPos = yPos
        self.startX = 0
        self.startY = 0

    def execute(self):
        self.startX = self.gameObject.mTransform.xPos
        self.startY = self.gameObject.mTransform.yPos
        self.gameObject.mTransform.setPosition(self.xPos, self.yPos)

    def undo(self):
        self.gameObject.mTransform.setPosition(self.startX, self.startY)

    def redo(self):
        self.execute()


class Game:
    def __init__(self, windowWidth, windowHeight):
        print("WASD to move and jump, ESC to view replays and exit")
        # Create game objects
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.sdl.setTitle("Platformer Replay Demo")
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.player = engine.GameObject()
        self.level = engine.GameObject()

        self.transform = engine.Transform()
        self.player.addTransformComponent(self.transform)
        self.transform.xPos = 35
        self.transform.yPos = 263

        self.rectangle = engine.RectangleComponent(self.transform)
        self.rectangle.setColor(126, 200, 227, 255)
        self.rectangle.setDimensions(25, 25)
        self.player.addRectangleComponent(self.rectangle)

        self.tilemap = engine.TileMapComponent("Assets/Levels/MarioTiles/replay_test.lvl")
        self.tilemap.loadTileset("Assets/tilesets/mario-like-tileset-32x32.png", self.sdl.getSDLRenderer())
        self.level.addTileMapComponent(self.tilemap)
        self.tileSize = self.tilemap.getSize()

        self.physics = engine.PhysicsComponent()
        self.player.addPhysicsComponent(self.physics)

        self.lvlWidth = self.tilemap.getCols() * self.tilemap.getSize()
        self.lvlHeight = self.tilemap.getRows() * self.tilemap.getSize()
        # self.camera = engine.StaticCamera()
        self.camera = engine.SideScrollerCamera(self.windowWidth, self.windowHeight, self.lvlWidth,
                                                self.lvlHeight, self.rectangle)
        self.player.addCamera(self.camera)
        self.level.addCamera(self.camera)

        self.enemies = []
        enemy = Enemy(int(windowWidth/2), int(windowHeight/2), 0, self.windowWidth, self.camera)
        enemy2 = Enemy(windowWidth, int(windowHeight/2), 0, 2 * self.windowWidth, self.camera)
        self.enemies.append(enemy)
        self.enemies.append(enemy2)

        self.sdl.addGameObject(self.player)
        self.sdl.addGameObject(self.level)
        for enemy in self.enemies:
            self.sdl.addGameObject(enemy.obj)

        # Setup game state
        self.playerSpeed = 5
        targetFPS = 60
        self.maxTicksPerFrame = int(1000 / targetFPS); # 16.66ms per frame
        self.frameStartTime = 0
        self.frame_count = 0
        self.startTime = self.sdl.getTimeMS()
        self.maxYVel = 25
        self.commandQueue = []
        self.lastCommand = -1
        self.currCommand = -1
        self.rewindMode = False

    # Not used in this game, but can be used to reconstruct commandQueue for replay
    def saveReplay(self):
        replayPath = "Assets/Replays"
        if not os.path.exists(replayPath):
            os.makedirs(replayPath)
        replayFile = os.path.join(replayPath, "challenge_time.rpy")
        with open(replayFile, "w") as f:
            f.write(f"{len(self.commandQueue)}\n")
            for command in self.commandQueue:
                f.write(f"{command.startX}")
                f.write(f" {command.startY}")
                f.write(f" {command.xPos}")
                f.write(f" {command.yPos}\n")

    # Delay game loop to reach target fps
    def limitFPS(self):
        frameTicks = self.sdl.getTimeMS() - self.frameStartTime
        if frameTicks < self.maxTicksPerFrame:
            self.sdl.delay(self.maxTicksPerFrame - frameTicks)
        self.frame_count += 1
        timeElapsed = self.sdl.getTimeMS() - self.startTime
        fps = self.frame_count / (timeElapsed / 1000)

    def replayComplete(self):
        replayStatus = []
        for entity in self.replayEntities:
            replayStatus.append(entity.currFrame >= entity.replayFrames[1])
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

        # Replay loop
        if self.replayMode and len(self.replayFrames) > 0:
            print("Replaying all attempts")
            self.sdl.setBlendModeAlpha()
            self.transform.setPosition(self.windowWidth, self.windowHeight) # Hide main player
            self.replayEntities = []
            for replay in self.replayFrames:
                replayPlayer = Player(replay, self.camera)
                self.replayEntities.append(replayPlayer)
                self.sdl.addGameObject(replayPlayer.obj)

            self.camera.target = self.replayEntities[-1].rectangle # Change focus to last replay
            # while not self.replayComplete() or not inputs[engine.QUIT_EVENT]:
            while not self.replayComplete():
                inputs = self.sdl.getInput()
                self.frameStartTime = self.sdl.getTimeMS()
                for entity in self.replayEntities:
                    if entity.currFrame <= entity.replayFrames[1]:
                        self.update(entity.obj, self.sdl.getInputAtFrame(entity.currFrame))
                        entity.currFrame += 1
                    else:
                        entity.obj.mRectangle.setColor(0, 0, 0, 0) # Hide replay object
                self.render()
                self.limitFPS()

    # Record replay and reset player back to start
    def reset(self, playerObj):
        if not self.replayMode:
            # print(f"{self.replayStartFrame} - {self.frame_count + 1}")
            self.replayFrames.append((self.replayStartFrame, self.frame_count + 1))
            self.rewindMode = True
            self.currCommand = len(self.commandQueue) - 1
            playerObj.mRectangle.setColor(255, 255, 0, 255)

    def victory(self, playerObj):
        if not self.replayMode:
            print("Victory!")
            print(f"You took: {(self.sdl.getTimeMS() - self.startTime) / 1000} seconds")
            self.replayFrames.append((self.replayStartFrame, self.frame_count + 1))
            self.replayMode = True

    def update(self, player, inputs):
        if self.rewindMode:
            if self.currCommand >= 0:
                self.commandQueue[self.currCommand].undo()
                self.currCommand -= 1
                self.camera.Update()
                return
            else:
                self.commandQueue = []
                self.rewindMode = False
                self.replayStartFrame = self.frame_count + 1
                player.mRectangle.setColor(126, 200, 227, 255)


        player.xVel = 0
        # Only apply gravity midair
        onGround = self.tilemap.isOnGround(player)
        if onGround:
            player.yVel = 0
        else:
            player.yVel += 2
            player.yVel = min(player.yVel, self.maxYVel)

        if inputs[engine.ESCAPE_PRESSED]:
            inputs[engine.QUIT_EVENT] = True
            self.replayMode = True
            return
        if inputs[engine.W_PRESSED] and onGround:
            player.yVel = -20
        if inputs[engine.A_PRESSED]:
            player.xVel = -self.playerSpeed
        if inputs[engine.D_PRESSED]:
            player.xVel = self.playerSpeed

        # Record replay if player crosses end
        if player.mTransform.xPos > self.lvlWidth:
            self.reset(player)
            return

        # Handle x and y collisions separately so we can slide along tiles and into corners
        # Handle x-axis collisions
        player.mPhysicsComponent.UpdateX(player)
        collision = self.tilemap.checkCollision(player)
        if self.tilemap.isTouchingType(collision, 27): # Flag tile
            self.reset(player)
            return
        if collision.isColliding:
            if player.xVel < 0:
                player.mTransform.xPos = (collision.firstTileColumn + 1) * self.tilemap.getSize()
            elif player.xVel > 0:
                player.mTransform.xPos = collision.firstTileColumn * self.tilemap.getSize() - player.mRectangle.getWidth()

        # Handle y-axis collisions
        player.mPhysicsComponent.UpdateY(player)
        collision = self.tilemap.checkCollision(player)
        if self.tilemap.isTouchingType(collision, 27):
            self.reset(player) # TODO: check if we need to create command on each pos update instead of just at end
            return
        if player.mTransform.xPos >= 1673: # Victory condition at end of level
            inputs[engine.QUIT_EVENT] = True
            self.victory(player)
            return
        if collision.isColliding:
            if player.yVel < 0:
                player.mTransform.yPos = (collision.firstTileRow + 1) * self.tilemap.getSize()
            elif player.yVel > 0:
                player.mTransform.yPos = collision.firstTileRow * self.tilemap.getSize() - player.mRectangle.getHeight()

        # Update enemies and handle collisions
        for enemy in self.enemies:
            if player.mRectangle.checkCollision(enemy.rectangle):
                self.reset(player)
            enemy.update()

        self.camera.Update()
        if not self.replayMode:
            command = MoveCommand(player, player.mTransform.xPos, player.mTransform.yPos)
            command.execute()
            self.commandQueue.append(command)
            self.lastCommand = len(self.commandQueue)

    def render(self):
        self.sdl.clear(32, 32, 32, 255) # Set background to gray
        self.sdl.Render()
        self.sdl.flip()

def main():
    game = Game(640, 320)
    game.runLoop()


if __name__ == "__main__":
    main()
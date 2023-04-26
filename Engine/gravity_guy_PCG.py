from lib import engine
import random
import os


# Represents a Gravity Guy Game
class Game:
    # Initialize Game
    def __init__(self, windowWidth, windowHeight):
        # SDL Setup
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        # Random level pieces
        self.level = 1
        self.levelPieces = ["Assets/Levels/MarioTiles/PCG-1-1.lvl", "Assets/Levels/MarioTiles/PCG-1-2.lvl",
                            "Assets/Levels/MarioTiles/PCG-1-3.lvl", "Assets/Levels/MarioTiles/PCG-1-4.lvl",
                            "Assets/Levels/MarioTiles/PCG-1-5.lvl", "Assets/Levels/MarioTiles/PCG-1-6.lvl",
                            "Assets/Levels/MarioTiles/PCG-1-7.lvl", "Assets/Levels/MarioTiles/PCG-1-8.lvl",
                            "Assets/Levels/MarioTiles/PCG-1-9.lvl", "Assets/Levels/MarioTiles/PCG-1-10.lvl"]
        # Tilemap Setup
        self.tilemap = self.GenerateLevel()
        self.tileSize = self.tilemap.getSize()
        self.lvlWidth = self.tilemap.getCols() * self.tileSize
        self.lvlHeight = self.tilemap.getRows() * self.tileSize
        # Physics Setup
        self.physics = engine.PhysicsComponent()
        # Entities to render
        self.entities = [] 

        # Player Object Setup
        self.player = engine.GameObject()
        # Player Transform Component
        self.playerTransform = engine.Transform()
        self.player.addTransformComponent(self.playerTransform)

        self.frameUpdateDelay = 0
        self.maxFrameUpdateDelay = 2
        targetFPS = 60
        self.maxTicksPerFrame = int(1000 / targetFPS); # 16.66ms per frame
        self.frameStartTime = 0
        self.frame_count = 0
        self.startTime = self.sdl.getTimeMS()
        self.maxFrameDict = {}
        '''
        CREATE A SPRITE
        Spritesheets should be located in the Assets folder. Use the "loadImage"
        function to import one.
        "setRectangleDimensions" sets the size of the sprite on the screen.
        
        "setSpriteSheetDimensions" is for correctly iterating through the spritesheet.
        (width of sprite, height of sprite, max num sprites in a row, total num sprites, numPixelsToTrimFromWidth)
        numPixelsToTrimFromWidth : this parameter tells how many pixels are to be taken off each sprite image, in case
        there is extra space between images.
        '''
        self.run_right_sprite = engine.Sprite(self.playerTransform, True)
        self.run_right_sprite.setRectangleDimensions(32, 48)
        self.run_right_sprite.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_right_sprite.loadImage("Assets/spritesheets/Cyborg_run_right.bmp", self.sdl.getSDLRenderer())
        self.player.addSpriteComponent(self.run_right_sprite)
        self.maxFrameDict[str(self.run_right_sprite)] = 5

        self.run_left_sprite = engine.Sprite(self.playerTransform, False)
        self.run_left_sprite.setRectangleDimensions(32, 48)
        self.run_left_sprite.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_left_sprite.loadImage("Assets/spritesheets/Cyborg_run_left.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_left_sprite)] = 5

        self.run_right_on_ceiling = engine.Sprite(self.playerTransform, True)
        self.run_right_on_ceiling.setRectangleDimensions(32, 48)
        self.run_right_on_ceiling.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_right_on_ceiling.loadImage("Assets/spritesheets/Cyborg_run_ceiling_and_right.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_right_on_ceiling)] = 5

        self.run_left_on_ceiling = engine.Sprite(self.playerTransform, False)
        self.run_left_on_ceiling.setRectangleDimensions(32, 48)
        self.run_left_on_ceiling.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_left_on_ceiling.loadImage("Assets/spritesheets/Cyborg_run_ceiling_and_left.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_left_on_ceiling)] = 5

        self.idle_right = engine.Sprite(self.playerTransform, True)
        self.idle_right.setRectangleDimensions(26, 48)
        self.idle_right.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_right.loadImage("Assets/spritesheets/Cyborg_idle_right.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_right)] = 4

        self.idle_left = engine.Sprite(self.playerTransform, False)
        self.idle_left.setRectangleDimensions(26, 48)
        self.idle_left.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_left.loadImage("Assets/spritesheets/Cyborg_idle_left.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_left)] = 4

        self.idle_right_on_ceiling = engine.Sprite(self.playerTransform, True)
        self.idle_right_on_ceiling.setRectangleDimensions(26, 48)
        self.idle_right_on_ceiling.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_right_on_ceiling.loadImage("Assets/spritesheets/Cyborg_idle_right_on_ceiling.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_right_on_ceiling)] = 4

        self.idle_left_on_ceiling = engine.Sprite(self.playerTransform, False)
        self.idle_left_on_ceiling.setRectangleDimensions(26, 48)
        self.idle_left_on_ceiling.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_left_on_ceiling.loadImage("Assets/spritesheets/Cyborg_idle_left_on_ceiling.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_left_on_ceiling)] = 4

        self.climb_up = engine.Sprite(self.playerTransform, True)
        self.climb_up.setRectangleDimensions(26, 48)
        self.climb_up.setSpriteSheetDimensions(48, 48, 6, 6, 24)
        self.climb_up.loadImage("Assets/spritesheets/Cyborg_climb.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.climb_up)] = 5

        self.climb_down = engine.Sprite(self.playerTransform, True)
        self.climb_down.setRectangleDimensions(26, 48)
        self.climb_down.setSpriteSheetDimensions(48, 48, 6, 6, 24)
        self.climb_down.loadImage("Assets/spritesheets/Cyborg_climb_down.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.climb_down)] = 5

        # Player Tilemap Component
        self.player.addTileMapComponent(self.tilemap)
        # Player Physics Component
        self.player.addPhysicsComponent(self.physics)

        # Camera Setup
        self.camera = engine.SpriteSideScrollerCamera(self.windowWidth, self.windowHeight, self.lvlWidth, 
                                                self.lvlHeight, self.player.mSprite)
        self.cameraOffsetX = 0
        self.cameraOffsetY = 0

        # Track number of frames in the sprite sheet
        self.currentFrame = 0
        self.currentMaxFrame = self.maxFrameDict[str(self.run_right_sprite)]

        # Climbing variables
        self.isClimbingRight = False
        self.isClimbingLeft = False
        self.curYDirection = 1 # must be 1 or -1
        self.curXDirection = 1 # must be 1 or -1
        self.climbingSpeed = 6
        self.fallingSpeed = 1

        # Sounds
        self.music = engine.Music()
        self.music.SetMusic("Assets/Sounds/SteamtechMayhem.wav")
        self.gameOverSound = engine.Sound()
        self.gameOverSound.SetSound("Assets/Sounds/GameOver.wav")
        self.winSound = engine.Sound()
        self.winSound.SetSound("Assets/Sounds/Win.wav")
        self.jumpSound = engine.Sound()
        self.jumpSound.SetSound("Assets/Sounds/Jump.wav")
        self.speedUpSound = engine.Sound()
        self.speedUpSound.SetSound("Assets/Sounds/SpeedUp.wav")

        # Gravity Guy Settings
        self.playerRunSpeed = 5
        self.playerJumpSpeed = self.playerRunSpeed * 2
        self.autoRun = True
        self.spaceTapErrorLenience = 0.1
        # Game Variables
        self.player.xVel = self.playerRunSpeed
        self.player.yVel = self.playerJumpSpeed
        self.timeSinceSpaceTapped = 99
        self.alreadySpedUp = False

    # Generates a random level
    def GenerateLevel(self):
        # Level start
        if self.level == 1:
            tilemap = engine.TileMapComponent("Assets/Levels/MarioTiles/PCG-1-start.lvl")
        else:
            tilemap = engine.TileMapComponent("Assets/Levels/MarioTiles/PCG-2-start.lvl")

        # Level pieces (if new are needed)
        if self.level == 2:
            self.levelPieces = ["Assets/Levels/MarioTiles/PCG-2-1.lvl", "Assets/Levels/MarioTiles/PCG-2-2.lvl",
                            "Assets/Levels/MarioTiles/PCG-2-3.lvl", "Assets/Levels/MarioTiles/PCG-2-4.lvl",
                            "Assets/Levels/MarioTiles/PCG-2-5.lvl", "Assets/Levels/MarioTiles/PCG-2-6.lvl",
                            "Assets/Levels/MarioTiles/PCG-2-7.lvl", "Assets/Levels/MarioTiles/PCG-2-8.lvl",
                            "Assets/Levels/MarioTiles/PCG-2-9.lvl", "Assets/Levels/MarioTiles/PCG-2-10.lvl"]
        
        # Random pieces
        random.seed()
        pieceIndecesChosen = []
        for i in range(10):
            newPieceIndex = random.randint(0, len(self.levelPieces) - 1)
            while newPieceIndex in pieceIndecesChosen:
                newPieceIndex = random.randint(0, len(self.levelPieces) - 1)
            pieceIndecesChosen.append(newPieceIndex)
            randomPiece = self.levelPieces[newPieceIndex]
            tilemap.ExtendTilemap(randomPiece)
        # Level end
        if self.level == 1:
            tilemap.ExtendTilemap("Assets/Levels/MarioTiles/PCG-1-end.lvl")
        else:
            tilemap.ExtendTilemap("Assets/Levels/MarioTiles/PCG-2-end.lvl")
        # Load tileset
        tilemap.loadTileset("Assets/tilesets/mario-like-tileset-32x32.png", self.sdl.getSDLRenderer())
        return tilemap

    # Handles player left and right movement from input
    def handlePlayerMove(self, inputs):
        if self.autoRun:
            self.curXDirection = 1
            self.player.xVel = self.playerRunSpeed
            self.player.yVel = self.playerJumpSpeed * self.curYDirection
            if self.isClimbingRight:
                self.player.yVel = self.climbingSpeed * (- self.curYDirection)
                if self.curYDirection > 0:
                    # gravity is down, change to climb_up sprite
                    self.player.addSpriteComponent(self.climb_up)
                    self.currentMaxFrame = self.maxFrameDict[str(self.climb_up)]
                else:
                    # gravity is up, change to climb_down sprite
                    self.player.addSpriteComponent(self.climb_down)
                    self.currentMaxFrame = self.maxFrameDict[str(self.climb_down)]
            else:
                if self.curYDirection > 0:
                    # change to running right
                    self.player.addSpriteComponent(self.run_right_sprite)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_right_sprite)]
                else:
                    # change to running right on ceiling
                    self.player.addSpriteComponent(self.run_right_on_ceiling)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_right_on_ceiling)]
            return
        if inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]:
            self.curXDirection = -1
            self.player.xVel = - self.playerRunSpeed
            self.player.yVel = self.playerJumpSpeed * self.curYDirection
            if self.isClimbingLeft:
                self.player.yVel = self.climbingSpeed * (- self.curYDirection)
                if self.curYDirection > 0:
                    # gravity is down, change to climb_up sprite
                    self.player.addSpriteComponent(self.climb_up)
                    self.currentMaxFrame = self.maxFrameDict[str(self.climb_up)]
                else:
                    # gravity is up, change to climb_down sprite
                    self.player.addSpriteComponent(self.climb_down)
                    self.currentMaxFrame = self.maxFrameDict[str(self.climb_down)]
            else:
                if self.curYDirection > 0:
                    # change to running left
                    self.player.addSpriteComponent(self.run_left_sprite)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_left_sprite)]
                else:
                    # change to running left on ceiling
                    self.player.addSpriteComponent(self.run_left_on_ceiling)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_left_on_ceiling)]
        elif inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]:
            self.curXDirection = 1
            self.player.xVel = self.playerRunSpeed
            self.player.yVel = self.playerJumpSpeed * self.curYDirection
            if self.isClimbingRight:
                self.player.yVel = self.climbingSpeed * (- self.curYDirection)
                if self.curYDirection > 0:
                    # gravity is down, change to climb_up sprite
                    self.player.addSpriteComponent(self.climb_up)
                    self.currentMaxFrame = self.maxFrameDict[str(self.climb_up)]
                else:
                    # gravity is up, change to climb_down sprite
                    self.player.addSpriteComponent(self.climb_down)
                    self.currentMaxFrame = self.maxFrameDict[str(self.climb_down)]
            else:
                if self.curYDirection > 0:
                    # change to running right
                    self.player.addSpriteComponent(self.run_right_sprite)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_right_sprite)]
                else:
                    # change to running right on ceiling
                    self.player.addSpriteComponent(self.run_right_on_ceiling)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_right_on_ceiling)]
        else:
            # set x velocity to 0
            self.player.xVel = 0
            # change to idle sprite based on self.curXDirection and self.curYDirection
            if self.curYDirection > 0:
                if self.curXDirection > 0:
                    # switch to idle_right
                    self.player.addSpriteComponent(self.idle_right)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_right)]
                else:
                    # switch to idle_left
                    self.player.addSpriteComponent(self.idle_left)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_left)]
            else:
                if self.curXDirection > 0:
                    # switch to idle_right_on_ceiling
                    self.player.addSpriteComponent(self.idle_right_on_ceiling)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_right_on_ceiling)]
                else:
                    # switch to idle_left_on_ceiling
                    self.player.addSpriteComponent(self.idle_left_on_ceiling)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_left_on_ceiling)]

            if self.isClimbingLeft or self.isClimbingRight:
                self.player.yVel = self.curYDirection * self.fallingSpeed

    # Handles player jump logic
    def handlePlayerJump(self, inputs):
        # Increment time since space tapped
        self.timeSinceSpaceTapped += 1 / 60
        # Detect if space was tapped
        if inputs[engine.SPACE_TAPPED]:
            self.timeSinceSpaceTapped = 0
        # If space hasn't been tapped recently (wiggle room time), no jump
        if self.timeSinceSpaceTapped > self.spaceTapErrorLenience:
            return
        # If space has been tapped within the time, then perform jump if possible
        self.timeSinceSpaceTapped = 99
        if self.tilemap.isOnCeiling(self.player) or self.tilemap.isOnGround(self.player):
            self.jumpSound.PlaySound()
            self.curYDirection *= -1
            self.player.yVel = self.playerJumpSpeed * self.curYDirection
        elif self.isClimbingRight or self.isClimbingLeft:
            if self.player.yVel > 0:
                self.player.yVel = self.climbingSpeed
                self.curYDirection = 1
            elif self.player.yVel < 0:
                self.player.yVel = - self.climbingSpeed
                self.curYDirection = -1
            else:
                # yVel == 0, falling speed acording to curYDirection
                self.player.yVel = self.fallingSpeed * self.curYDirection

    # Handles player wall climbing
    def handlePlayerWallClimbing(self, inputs, collision):
        if collision.isColliding and self.player.xVel > 0:
            # hit right wall: set xPos to correct x according to row, col
            self.playerTransform.xPos = self.tileSize * collision.firstTileColumn - self.player.mSprite.getWidth()
            # change isClimbingRight only once
            if not self.isClimbingRight:
                self.isClimbingRight = True
                # check if on ground or ceiling
                if not (self.tilemap.isOnCeiling(self.player) or self.tilemap.isOnGround(self.player)):
                    self.curYDirection *= -1
            self.isClimbingLeft = False
        elif collision.isColliding and self.player.xVel < 0:
            # hit left wall
            self.playerTransform.xPos = self.tileSize * (collision.firstTileColumn + 1)
            # change isClimbingLeft only once
            if not self.isClimbingLeft:
                self.isClimbingLeft = True
                # check if on ground or ceiling
                if not (self.tilemap.isOnCeiling(self.player) or self.tilemap.isOnGround(self.player)):
                    self.curYDirection *= -1
            self.isClimbingRight = False
        # check if falling off wall (pushing opposite direction than climbing wall)
        if self.isClimbingRight and not self.tilemap.isTouchingRightWall(self.player):
            self.isClimbingRight = False
            if self.player.xVel < 0:
                # player jumped off wall
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            elif self.player.xVel > 0:
                # player reached top of wall
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            else:
                # player is not pushing left or right
                self.player.yVel = 0
                self.curYDirection *= -1
        elif self.isClimbingLeft and not self.tilemap.isTouchingLeftWall(self.player):
            self.isClimbingLeft = False
            if self.player.xVel > 0:
                # player jumped off wall
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            elif self.player.xVel < 0:
                # player reached top of wall
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            else:
                # player is not pushing left or right
                self.player.yVel = 0
                self.curYDirection *= -1

    # Handles game over
    def playerGameOver(self):
        self.gameOverSound.PlaySound()
        self.RestartGame()

    # Handles player win
    def playerWin(self):
        self.level += 1
        self.winSound.PlaySound()
        self.RestartGame()

    # Checks for collisions with a spike (any tile with ID 10)
    def touchingSpikeCheck(self, collision):
        if self.tilemap.isTouchingType(collision, 10):
            self.playerGameOver()

    # Checks for collisions with a speed up tile (any tile with ID 42)
    def touchingSpeedUpCheck(self, collision):
        if self.tilemap.isTouchingType(collision, 42) and not self.alreadySpedUp:
            self.speedUpSound.PlaySound()
            self.alreadySpedUp = True
            if self.playerRunSpeed < 20:
                self.playerRunSpeed += 1
                self.playerJumpSpeed = self.playerRunSpeed * 2
        elif not self.tilemap.isTouchingType(collision, 42):
            self.alreadySpedUp = False

    # Checks for collisions with a spike (any tile with ID 27)
    def touchingWinCheck(self, collision):
        if self.tilemap.isTouchingType(collision, 27):
            self.playerWin()

    # Handles all unique collision checks
    def handleCollisionTypes(self, collision):
        self.touchingSpikeCheck(collision)
        self.touchingWinCheck(collision)

    # Handles all player associated updates
    def playerUpdate(self, inputs):
        # Player left and right movement
        self.handlePlayerMove(inputs)
        # Player jump
        self.handlePlayerJump(inputs)
        # Physics update on player xPos
        self.physics.UpdateX(self.player)
        # Collision update
        collision = self.tilemap.checkCollision(self.player)
        # Wall climb
        self.handlePlayerWallClimbing(inputs, collision)
        # Collision Checks
        self.handleCollisionTypes(collision)
        # Physics update on player yPos
        self.physics.UpdateY(self.player)
        # Collision update
        collision = self.tilemap.checkCollision(self.player)
        # Collision Checks
        self.handleCollisionTypes(collision)
        # Check for speedup collision
        self.touchingSpeedUpCheck(collision)
        # Ceiling or floor collision check
        if collision.isColliding and self.player.yVel < 0:
            # hit ceiling: set yPos to correct y according to row, col
            self.playerTransform.yPos = self.tileSize * (collision.firstTileRow + 1)
        elif collision.isColliding and self.player.yVel > 0:
            # hit floor
            self.playerTransform.yPos = self.tileSize * (collision.firstTileRow) - self.player.mSprite.getHeight()
        # check if off screen
        if self.playerTransform.yPos <= 0 or self.playerTransform.yPos >= self.lvlHeight - self.player.mSprite.getHeight():
            self.playerGameOver()
        
        # update frame
        if self.frameUpdateDelay > self.maxFrameUpdateDelay:
            self.frameUpdateDelay = 0
            if self.currentFrame >= self.currentMaxFrame-1:
                self.currentFrame = 0
            else:
                self.currentFrame += 1
        else:
            self.frameUpdateDelay += 1
        self.player.mSprite.update(0, 0, self.currentFrame)
    

    # Delay game loop to reach target fps
    def limitFPS(self):
        frameTicks = self.sdl.getTimeMS() - self.frameStartTime
        if frameTicks < self.maxTicksPerFrame:
            self.sdl.delay(self.maxTicksPerFrame - frameTicks)
        self.frame_count += 1
        timeElapsed = self.sdl.getTimeMS() - self.startTime
        fps = self.frame_count / (timeElapsed / 1000)

    # Update
    def Update(self, inputs):
        # Quit check
        if inputs[engine.ESCAPE_PRESSED]:
            inputs[engine.QUIT_EVENT] = True
        # Player Update
        self.playerUpdate(inputs)
        # update camera
        self.camera.Update()

    # Render
    def Render(self):
        self.sdl.clear(32, 32, 32, 255) # Set background to gray
        self.player.mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.tilemap.Render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.sdl.flip()

    # Starts the game
    def StartGame(self):
        self.playerRunSpeed = 5
        self.playerJumpSpeed = self.playerRunSpeed * 2
        self.curYDirection = 1 # must be 1 or -1
        self.curXDirection = 1 # must be 1 or -1
        self.player.xVel = self.playerRunSpeed
        self.player.yVel = self.playerJumpSpeed
        self.timeSinceSpaceTapped = 99
        self.alreadySpedUp = False
        self.playerTransform.xPos = 100
        self.playerTransform.yPos = 100
        self.camera.Update()

    # Re-starts the game
    def RestartGame(self):
        self.tilemap = self.GenerateLevel()
        self.tileSize = self.tilemap.getSize()
        self.lvlWidth = self.tilemap.getCols() * self.tileSize
        self.lvlHeight = self.tilemap.getRows() * self.tileSize
        self.player.addTileMapComponent(self.tilemap)
        self.StartGame()

    # Main Loop
    def RunLoop(self):
        inputs = self.sdl.getInput()
        self.music.PlayMusic()
        while not inputs[engine.QUIT_EVENT]:
            self.frameStartTime = self.sdl.getTimeMS()
            self.Update(inputs := self.sdl.getInput())
            self.Render()
            self.limitFPS()
# Main
def main():
    game = Game(960, 540)
    print("GRAVITY GUY\nProcedural Generation mode.\nCONTROLS:\nSpace - invert gravity\nESC - exit\nBlue Tiles are dangerous, pink tiles speed you up.\n")
    game.StartGame()
    game.RunLoop()

# Run Main
if __name__ == "__main__":
    main()
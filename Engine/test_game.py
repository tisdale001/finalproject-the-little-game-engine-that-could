from lib import engine

class Game:
    def __init__(self, windowWidth, windowHeight):
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.entities = [] # Entities to render

        self.player = engine.GameObject()

        self.transform = engine.Transform()
        self.transform.xPos = 100
        self.transform.yPos = 200

        self.rectangle = engine.RectangleComponent(self.transform)
        self.rectangle.setDimensions(50, 50)
        self.player.addRectangleComponent(self.rectangle)

        self.tilemap = engine.TileMapComponent("Assets/Levels/MarioTiles/nish-test1.lvl")
        self.player.addTileMapComponent(self.tilemap)

        self.camera = engine.SideScrollerCamera(0, 0, 0, 0, self.rectangle) # Needs real values

    def runLoop(self):
        inputs = self.sdl.getInput()
        while not inputs[engine.QUIT_EVENT]:
            self.update(inputs := self.sdl.getInput())
            self.render()
            self.sdl.delay(25) # Needs frame rate limiting code from test_game.cpp

    def update(self, inputs):
        if inputs[engine.W_PRESSED]:
            pass
        if inputs[engine.S_PRESSED]:
            pass
        if inputs[engine.A_PRESSED]:
            pass
        if inputs[engine.D_PRESSED]:
            pass

    def render(self):
        self.sdl.clear(32, 32, 32, 255) # Set background to gray
        # for entity in self.entities:
        #     entity.draw(self.sdl)
        self.rectangle.Render(self.sdl.getSDLRenderer(), 0, 0)
        self.sdl.flip()

def main():
    game = Game(960, 540)
    game.runLoop()


if __name__ == "__main__":
    main()
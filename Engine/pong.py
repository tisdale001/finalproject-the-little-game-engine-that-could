# Run with:
#
# (Linux & Mac) python3 test.py -m ./mygameengine.so
# (Windows) python3.6 test.py -m ./mygameengine.pyd
#
# Note: Tested on Python3.10

from lib import mygameengine as engine
from enum import IntEnum
import random


class Direction(IntEnum):
    UP = -1
    DOWN = 1


class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, xPos, yPos, width, height):
        self.x = xPos # xPos of rectangle's top left corner
        self.y = yPos # yPos of rectangle's top left corner
        self.w = width
        self.h = height

    # Return true if there is an intersection with Rectangle r2
    def checkCollision(self, r2):
        return (self.x < r2.x + r2.w and
            self.x + self.w > r2.x and
            self.y < r2.y + r2.h and
            self.h + self.y > r2.y)

    def draw(self, sdl):
        sdl.setRenderColor(255, 255, 255, 255) # Draw filled in white
        sdl.DrawRectangle(int(self.x), int(self.y), int(self.w), int(self.h))


class Paddle(Rectangle):
    def __init__(self, xPos, yPos, width, height, speed, windowHeight):
        super().__init__(xPos, yPos, width, height)
        self.speed = speed
        self.windowHeight = windowHeight

    def update(self, direction):
        self.y += (direction * self.speed)
        if self.y < 0:
            self.y = 0
        elif self.y > (lowerBound := self.windowHeight - self.h):
            self.y = lowerBound

    def draw(self, sdl):
        sdl.setRenderColor(255, 0, 0, 255) # Draw filled in red
        sdl.DrawRectangle(int(self.x), int(self.y), int(self.w), int(self.h))


class Ball(Rectangle):
    def __init__(self, xPos, yPos, width, height, speed):
        super().__init__(xPos, yPos, width, height)
        self.startX = xPos
        self.startY = yPos
        self.speed = speed
        self.vel = Vec2D(speed, 0)

    # Reset to original speed, ball direction is random
    def reset(self):
        self.x = self.startX
        self.y = self.startY
        self.vel.x = random.choice([-1, 1]) * self.speed
        self.vel.y = 0

    def handleWallCollision(self, windowWidth, windowHeight):
        topY = self.y
        botY = self.y + self.h
        leftX = self.x # Paddle left edge
        rightX = self.x + self.w # Paddle right edge
        if rightX < 0 or leftX > windowWidth:
            self.reset()
        if topY < 0 or botY > windowHeight:
            self.vel.y *= -1

    def resolveCollision(self, paddle):
        if self.vel.x > 0:
            self.x = paddle.x - self.w # Set ball to left edge of right paddle
        else:
            self.x = paddle.x + paddle.w # Set ball to right edge of left paddle

    def handlePaddleCollision(self, paddle):
        if self.checkCollision(paddle):
            self.resolveCollision(paddle)
            topThirdPaddle = paddle.y + paddle.h/3
            bottomThirdPaddle = paddle.y + 2*paddle.h/3
            ballCenterY = self.y + self.h/2
            if ballCenterY < topThirdPaddle:
                self.vel.y = -0.75 * self.speed
            elif ballCenterY > bottomThirdPaddle:
                self.vel.y = 0.75 * self.speed
            else:
                self.vel.y *= -1
            self.vel.x *= -1

    def update(self):
        self.x += self.vel.x
        self.y += self.vel.y


class PongGame:
    def __init__(self, windowWidth, windowHeight):
        paddleWidth = 10
        paddleHeight = 40
        paddleSpeed = 10
        ballSize = 10
        ballSpeed = 8
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.p1 = Paddle(
            windowWidth*0.05 - paddleWidth/2,
            windowHeight/2 - paddleHeight/2,
            paddleWidth,
            paddleHeight,
            paddleSpeed,
            windowHeight
        )
        self.p2 = Paddle(
            windowWidth*0.95 - paddleWidth/2,
            windowHeight/2 - paddleHeight/2,
            paddleWidth,
            paddleHeight,
            paddleSpeed,
            windowHeight
        )
        self.ball = Ball(
            windowWidth/2 - ballSize/2,
            windowHeight/2 - ballSize/2,
            ballSize,
            ballSize,
            ballSpeed
        )
        self.divider = Rectangle(xPos=windowWidth/2, yPos=0, width=2, height=windowHeight)
        self.entities = [self.p1, self.p2, self.ball, self.divider] # Entities to render

    def runLoop(self):
        inputs = self.sdl.getInput()
        while not inputs[engine.QUIT_EVENT]:
            self.update(inputs := self.sdl.getInput())
            self.render()
            self.sdl.delay(25)

    def update(self, inputs):
        if inputs[engine.W_PRESSED]:
            self.p1.update(Direction.UP)
        if inputs[engine.S_PRESSED]:
            self.p1.update(Direction.DOWN)
        if inputs[engine.UP_PRESSED]:
            self.p2.update(Direction.UP)
        if inputs[engine.DOWN_PRESSED]:
            self.p2.update(Direction.DOWN)
        self.ball.update()
        self.ball.handleWallCollision(self.windowWidth, self.windowHeight)
        self.ball.handlePaddleCollision(self.p1)
        self.ball.handlePaddleCollision(self.p2)

    def render(self):
        self.sdl.clear(32, 32, 32, 255) # Set background to gray
        for entity in self.entities:
            entity.draw(self.sdl)
        self.sdl.flip()


def main():
    pong = PongGame(960, 540)
    pong.runLoop()


if __name__ == "__main__":
    main()
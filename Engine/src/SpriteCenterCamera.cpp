#include "SpriteCenterCamera.hpp"
#include <algorithm>

SpriteCenterCamera::SpriteCenterCamera(int camWidth, int camHeight, int lvlWidth, int lvlHeight, Sprite* sp):
    cameraWidth(camWidth),
    cameraHeight(camHeight),
    levelWidth(lvlWidth),
    levelHeight(lvlHeight),
    target(sp) {
        x = std::clamp(sp->getCenterX() - cameraWidth/2, 0, levelWidth - cameraWidth);
        y = std::clamp(sp->getCenterY() - cameraHeight/2, 0, levelHeight - cameraHeight);
    }

SpriteCenterCamera::~SpriteCenterCamera() {}

void SpriteCenterCamera::Update() {
    x = target->getCenterX() - cameraWidth/2;
    y = target->getCenterY() - cameraHeight/2;
    x = std::clamp(x, 0, levelWidth - cameraWidth);
    y = std::clamp(y, 0, levelHeight - cameraWidth);
}
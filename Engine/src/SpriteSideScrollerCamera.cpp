#include "SpriteSideScrollerCamera.hpp"
#include <algorithm>

// TODO: This should be abstracted into a base class/interface
// TODO: Setting y to bottom of level by default but we should have a setY in a function or the constructor
/** @brief Constructor
 * 
 * Constructor that takes in demensions and, for now, a RectangleComponent as the main character
 * 
*/
SpriteSideScrollerCamera::SpriteSideScrollerCamera(int camWidth, int camHeight, int lvlWidth, int lvlHeight, Sprite* sp):
    cameraWidth(camWidth),
    cameraHeight(camHeight),
    levelWidth(lvlWidth),
    levelHeight(lvlHeight),
    target(sp) {
        x = std::clamp(sp->getCenterX() - cameraWidth/2, 0, levelWidth - cameraWidth);
        y = lvlHeight - cameraHeight;
    }
/** @brief Deconstructor
 * 
*/
SpriteSideScrollerCamera::~SpriteSideScrollerCamera() {}

/** @brief Update function that offsets camera x position
 * 
 * Update function offsets camera x value according to target (main character). Uses std::clamp() to not pan off the level on either side.
 * This creates the side scroller functionality of the camera.
*/
void SpriteSideScrollerCamera::Update() {
    x = target->getCenterX() - cameraWidth/2;
    x = std::clamp(x, 0, levelWidth - cameraWidth);
}
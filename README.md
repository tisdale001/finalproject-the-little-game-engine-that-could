# finalproject-the-little-game-engine-that-could
Game Engine for creating 2D games such as side-scrolling or map-scrolling games, plus three different versions of a "Gravity Guy" inspired game of our own design. The Engine also contains a level editor for designing tile-based levels for your games.
## Group members:
B. Lucian Tisdale (myself)<br>
Nishanth Duraiarasu<br>
Evan Haines<br>
Mateus Aurelio<br>

## Background:
This was a final project for a Game Engine Design class at Northeastern University. The requirements for the project included implementing resource managers, game objects with components, and handling collisions. 
It was also required for us to create a level editor which could save/load levels that could be used in an actual game. 
We were also required to create a game with our engine. The Game Engine had to be completed in C++, while the actual game was to be implemented completely in Python, using Pybind.
## Features:
* Game Engine was implemented in C++
* "Gravity Guy" inspired game was completed completely in Python
* Pybind was used to "link" the two languages (Python scripting)
* Level Editor was completed in Python using Tkinter
* Three different versions of the "Gravity Guy" game were completed to achieve the "wow factor" requirement of the project. These versions featured Procedural Content Generation and the ability to record and play back, forward and reverse.
* Software Design Patterns include: Game Object pattern, Resource Manager pattern, Singleton Pattern
* Sprite sheets and tile sheets were used to create animated sprites and tile-based game environments

## How to run locally
This project was completely developed in a Linux environment. There is logic contained in the code to be able to run in Windows and Mac, but it has not been tested.<br>
To run in Linux you will have to download dependencies including SDL2 and Pybind11.
To compile the Engine(C++)
```
cd Engine/
python3 linuxbuild.py
```
To run "Gravity Guy"
```
python3 gravity_guy.py
```
***



#  Space Invader Game

A fun arcade-style Space Invader game developed in Python using Pygame.

## Features

- Player spaceship with custom drawn shape
- Animated enemy aliens
- Smooth moving starfield background
- Bullet shooting system
- Enemy shooting system
- Particle explosion effects
- Multiple levels with increasing difficulty
- Score, high score, and lives system
- Start menu
- Restart and quit options
- High score saved in a text file

## Technologies Used

- **Python**
- **Pygame**
- **OS module** for file handling
- **Random module** for enemy shooting and particle effects
- **Math module** for animation and movement effects

---

## Game Logic Overview

### Player
The player controls a spaceship at the bottom of the screen.

- Move left and right using arrow keys or A / D
- Shoot bullets using the Space key
- Avoid enemy bullets and enemy contact

### Enemies
Enemies move left and right together.

- When they touch the screen edge, they reverse direction
- After reversing, they move downward
- Enemies randomly shoot bullets at the player
- If all enemies are destroyed, the next level starts

### Levels
Each time the player clears all enemies:

- The level increases
- Enemy speed increases
- Enemy shooting becomes faster
- A new wave of enemies is created

### Score
- Destroying enemies gives score
- Different enemy types can give different points
- Extra score is awarded after clearing a level

### High Score
The high score is stored in a file called:

```bash
highscore.txt


##  Controls

- Left Arrow → Move Left
- Right Arrow → Move Right
- Spacebar → Shoot
- R → Play Again
- Q → Quit

##  How to Run

1. Install pygame

```bash
pip install pygame

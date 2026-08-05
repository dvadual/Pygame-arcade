# ?? snek arena

A Pygame snake simulation with AI-controlled snakes, physics-driven movement, and procedurally rendered food particles.

## ?? Project Overview

**snek arena** is implemented in `snek.py` as a large-world snake simulation. The project uses Pygame to render a 2560×2560 board inside a 640×640 window, spawn gradient food particles, and run autonomous snake agents.

The repository also includes `gettingstarted.py` as a separate Pygame reference example.

---

## ? Verified Features

- AI-controlled snakes using the `simplevectorai` steering mode
- Smooth acceleration and deceleration via delta-time movement
- Gradient-based food particle rendering with alpha transparency
- A 2560×2560 game world rendered inside a 640×640 display
- Snake growth when food is consumed
- Collision detection using `pygame.Rect.collidelistall`
- Snake death spawns new food particles from body segments

---

## ??? Controls

The codebase supports player input modes in `playerMovement`, but the default `snek.py` startup currently launches AI-controlled snakes only.

Available input modes in code:
- `key` — WASD keyboard input
- `mouse` — mouse-relative movement
- `random` — randomized walking behavior
- `simplevectorai` — AI steering using nearby objects

If a player-controlled snake is enabled, the movement behavior is:
- `W` / `A` / `S` / `D` for direction
- smooth acceleration while keys are held
- smooth deceleration when keys are released
- head rotation facing the movement direction

---

## ?? Installation

### Prerequisites
- Python 3.x
- `pygame`

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd pygamestuff
```

2. Install Pygame:
```bash
pip install pygame
```

3. Run the game:
```bash
python snek.py
```

---

## ?? Project Structure

```
pygamestuff/
+-- snek.py                      # Main game implementation
+-- gettingstarted.py            # Pygame example for image movement and collision
+-- tempCodeRunnerFile.py        # Temporary scratch file
+-- exanpleimage.jpeg            # Asset used by gettingstarted.py
+-- README.md                    # Project documentation
+-- .github/
¦   +-- prompts/
¦       +-- update-readme.md     # Documentation maintenance guide
+-- screenshots/
    +-- maingameplay.png         # Gameplay screenshot
    +-- snakehead.png            # Snake head close-up
```

### File Purposes

| File | Purpose |
|------|---------|
| `snek.py` | Main game with gameplay, AI, physics, rendering, and collision logic |
| `gettingstarted.py` | Separate Pygame demo for basic movement and collision |
| `tempCodeRunnerFile.py` | Temporary experimental code file |

---

## ?? Architecture

### Core Classes

#### `playerMovement`
Handles movement, input state, and physics for snakes.

Key responsibilities:
- `position` — world coordinates
- `speed` — four-directional speed array
- `maxspeed`, `acc` — movement parameters
- `move()` — calculates velocity from the current input mode
- `angleturn()` — computes the facing angle with `atan2`
- `updatepos_angle()` — applies delta-time movement each frame

Supported input modes in code:
- `key` for WASD input
- `mouse` for mouse-relative movement
- `random` for random wandering
- `simplevectorai` for AI steering

#### `sneks`
Inherits from `playerMovement` and adds game-specific snake behavior:
- Pre-renders the snake head with eyes
- Maintains body segment rectangles for collision detection
- Stores a body trail from past positions
- Updates body width and size as the snake grows
- Draws the head and body each frame
- Spawns food particles when a snake is removed

#### `circleobj`
Represents food particles with gradient rendering:
- Creates a radial gradient surface
- Stores a `pygame.Rect` for collision checks
- Draws itself onto the board surface

#### `gameboard`
Manages the world state:
- Creates a 2560×2560 board surface
- Generates snakes and food particles
- Tracks borders around the arena
- Updates and renders the game each frame
- Displays score text for the first snake

---

## ?? Runtime Behavior

- Default startup constructs `gameboard(screen, 20, 800)` and spawns `15` AI snakes with `simplevectorai`.
- The game world is `2560×2560`, shown in a `640×640` window.
- Food particles are generated without overlapping and rendered with gradients.
- Snake growth is triggered by head-food collision.
- Body collisions spawn additional food particles and remove the colliding snake.
- Score is displayed from the first snake's point total.

---

## ?? Screenshots

### Main Gameplay
![Main Gameplay](screenshots/maingameplay.png)
*Gameplay screenshot showing multiple AI snakes and scattered gradient food particles.*

### Snake Head Close-up
![Snake Head Close-up](screenshots/snakehead.png)
*Close-up view of the snake head graphic with eyes and pupils.*

---

## ?? Evidence Summary

| Claim | Source |
|---|---|
| Default startup uses AI snakes | `snek.py` with `game = gameboard(screen,20,800)` and `self.makesneks("simplevectorai",15)` |
| 2560×2560 world board | `self.width,self.height = (2560,2560)` in `gameboard.__init__` |
| 800 food particles | `gameboard(screen,20,800)` and `makecircles()` |
| Delta-time movement | `dt = clock.tick(60) / 1000` and position updates in `playerMovement.updatepos_angle()` |
| Gradient food rendering | `circleobj.__init__()` with `pygame.draw.aacircle` and alpha blending |
| Player/mouse input modes present | `playerMovement.move()` supports `key` and `mouse` modes |
| Screenshots present | `screenshots/maingameplay.png`, `screenshots/snakehead.png` |

# 🐍 Multiplayer Snake Arena

A modern, physics-based multiplayer snake game built with Pygame. Control your snake through a dynamic arena, compete against AI opponents, and grow by collecting food in this engaging real-time strategy game.

## 📋 Project Overview

**Multiplayer Snake Arena** is an enhanced take on the classic Snake game, featuring:
- **Physics-driven movement** with smooth acceleration and deceleration
- **Multiple control schemes** (keyboard, mouse, AI)
- **Procedurally generated food particles** with gradient rendering
- **Real-time collision detection** between snakes and food
- **Dynamic camera system** that follows the player

The game demonstrates advanced Python game development concepts including object-oriented design, vector mathematics, physics simulation, and real-time graphics rendering. Perfect for portfolio building and game development learning.

---

## ✨ Features

### Gameplay Features
- 🎮 **Player-controlled snake** with keyboard controls
- 🤖 **4 AI-controlled snakes** with autonomous movement patterns
- 🍔 **70 randomly placed food items** with collision-based collection
- 📏 **Growth mechanics** - snakes expand as they consume food
- 💥 **Multi-snake collision detection** system
- 📹 **Dynamic camera** that follows the player's snake
- 🎨 **Gradient-rendered particles** for visual polish

### Technical Highlights
- **Delta-time based physics** for frame-rate independent movement
- **Vector2 mathematics** for smooth directional movement
- **Inheritance hierarchy** using Python classes (`playerMovement` → `sneks`)
- **Surface rendering** with alpha transparency and rotation
- **Collision detection algorithms** (rect collisions, point collisions)
- **Procedural content generation** for food placement
- **Optimized rendering** pipeline

---

## 🕹️ Controls

### Keyboard Controls
| Key | Action |
|-----|--------|
| **W** | Move Up |
| **A** | Move Left |
| **S** | Move Down |
| **D** | Move Right |
| **ALT+F4** or **Close Window** | Exit Game |

**Movement Mechanics:** 
- Smooth acceleration when keys are pressed
- Smooth deceleration when keys are released
- Snake head rotates to face movement direction
- Direction arrow indicates intended direction of movement

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository** (or download the project)
```bash
git clone <repository-url>
cd pygamestuff
```

2. **Install dependencies**
```bash
pip install pygame
```

3. **Run the game**
```bash
python snek.py
```

### Optional: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install pygame
pip install pygame

# Run game
python snek.py
```

---

## 📦 Requirements

```
pygame==2.1.0+
python>=3.7
```

Install via:
```bash
pip install pygame
```

---

## 📁 Project Structure

```
pygamestuff/
├── snek.py                      # Main game file (production)
├── gettingstarted.py            # Learning/practice file (tutorial code)
├── tempCodeRunnerFile.py        # Temporary code snippet
└── README.md                    # This file
```

### File Descriptions

**`snek.py`** (Main Game - ~330 lines)
- Core game logic and loop
- All class definitions and game mechanics
- Fully playable multiplayer snake arena

**`gettingstarted.py`** (Tutorial/Demo - ~70 lines)
- Pygame fundamentals demonstration
- Image loading, scaling, collision detection
- Learning resource for Pygame basics

---

## 🔧 How the Game Works Internally

### Architecture Overview

The game uses **object-oriented design** with a clear class hierarchy:

```
playerMovement (Base Class)
    └── sneks (Game Snake Class)
         └── Player + 4 AI Snakes

circleobj (Food Particle Class)

gameboard (Game Manager - partially implemented)
```

### Core Classes

#### **`playerMovement` Class**
Handles all movement physics and input:
- **Attributes:** position, velocity, angle, speed array (WASD tracking)
- **Methods:**
  - `move()` - Processes input and calculates velocity
  - `accelmove(i)` - Accelerates in direction i
  - `decelmove(i)` - Decelerates in direction i
  - `angleturn()` - Rotates snake based on movement
  - `updatepos_angle()` - Updates position and angle each frame

**Input Modes:**
- `"key"` - WASD keyboard input
- `"mouse"` - Mouse-following movement
- `"random"` - AI autonomous movement

#### **`sneks` Class (Inherits from playerMovement)**
Extends movement with rendering and game logic:
- **Head Rendering:** 3D-like triangular head with eyes using vector mathematics
- **Body Trail:** Dynamic array of circles that follow the head
- **Collision Detection:** Head rectangle for food and body collisions
- **Growth Mechanics:** `increasecount()` increases snake size and width
- **Display:** `showsnek()` renders head, body, arrow, and handles rotation

**Key Methods:**
```python
drawhead()          # Creates triangular head shape with eyes
drawbody(position)  # Adds body segment
updatebody()        # Maintains body trail spacing
showsnek()          # Main render function (called each frame)
increasecount()     # Grows snake on food consumption
```

#### **`circleobj` Class**
Food particles with gradient rendering:
- Procedurally generates gradient circles
- Stores inner/outer colors for smooth visual effect
- Uses alpha blending for transparency

### Game Loop (Main)

```python
while running:
    # Input processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear screen
    board.fill("black")
    
    # Render food particles
    for food in cirobjects:
        food.drawparticle(board)
    
    # Update and render each snake
    for snake in snakes:
        snake.showsnek()
        
        # Collision detection: snake vs food
        food_collisions = snake.headrect.collidelistall(circles)
        if food_collisions:
            snake.increasecount()  # Grow
            # Remove eaten food
        
        # Collision detection: snake vs other snakes
        body_collisions = snake.headrect.collidelistall(snakebodies)
        if body_collisions:
            print(f"{snake.color} collided!")  # Debug output
    
    # Camera follows player (snake[0])
    camera_pos = board.get_rect(center=screen_center - player_position)
    screen.blit(board, camera_pos)
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000  # 60 FPS, delta time in seconds
```

### Physics Implementation

**Delta-Time Based Movement:**
```python
dt = clock.tick(60) / 1000  # Convert milliseconds to seconds
speed += acceleration * dt  # Frame-rate independent
position += speed * dt
```

This ensures smooth gameplay regardless of frame rate variations.

**Vector Mathematics:**
- Angle calculations using `math.atan2()`
- Direction vectors via `pygame.Vector2`
- Rotation via `pygame.transform.rotate()`

### Collision System

**Two Types of Collisions:**
1. **Rectangle Collision** - Snake head (rect) vs food (rect)
   ```python
   collisions = snake.headrect.collidelistall(food_rects)
   ```

2. **Circle Collision** - Snake head vs other snake bodies
   ```python
   collisions = snake.headrect.collidelistall(other_bodies)
   ```

---

## 🎯 Game Mechanics

### Snake Growth
- Each food consumed increases `count` by 1
- Every 10 foods consumed, width increases by 2 pixels
- Body segments are evenly spaced using distance-based tracking

### Movement Physics
```
Max Speed: 200 pixels/second
Acceleration: 500 pixels/second²
Angular Velocity: 15 degrees per frame
Deceleration: Same as acceleration
```

### AI Behavior
Random snakes choose new directions every 10 frames, simulating autonomous gameplay.

---

## 🌟 Code Quality Highlights

- **Modular Design:** Clear separation of concerns (movement, rendering, collision)
- **Reusable Components:** `playerMovement` base class used for player and AI
- **Efficient Rendering:** Only updates necessary game objects
- **Math-Heavy:** Demonstrates vector operations and angle calculations
- **Scalable Architecture:** Easy to add new snake types or game modes

---

## 📈 Future Improvements

### Gameplay Features
- [ ] **Game Over Detection** - Implement end conditions when player collides with body
- [ ] **Score System** - Display current score and high scores
- [ ] **Difficulty Levels** - Adjustable AI speed, more snakes, larger maps
- [ ] **Power-ups** - Speed boost, invincibility, etc.
- [ ] **Leaderboard** - Track high scores across sessions
- [ ] **Sound Effects** - Eating, collision, game over sounds
- [ ] **Music** - Background gameplay music

### Visual Enhancements
- [ ] **Particle Effects** - Explosion when food is eaten
- [ ] **Snake Skins** - Custom textures and patterns
- [ ] **Map Themes** - Different background styles
- [ ] **Animations** - Smooth transitions and UI polish
- [ ] **Shadows/Lighting** - Depth perception

### Technical Improvements
- [ ] **Settings Menu** - Adjust difficulty, controls, graphics
- [ ] **Pause Menu** - In-game pause and resume
- [ ] **Save System** - Save/load game state
- [ ] **Networking** - Multiplayer over network (future expansion)
- [ ] **Configuration File** - Load game settings from config
- [ ] **Logging System** - Better debug output organization

### Code Refactoring
- [ ] **Complete `gameboard` Class** - Finish partial implementation
- [ ] **Input Manager** - Centralized input handling
- [ ] **Event System** - Decouple game logic from rendering
- [ ] **Unit Tests** - Test collision detection, physics
- [ ] **Type Hints** - Add Python type annotations
- [ ] **Documentation** - Docstrings for all methods

---

## 📸 Screenshots

### Main Gameplay
![Main Game](https://via.placeholder.com/640x640?text=Main+Gameplay+Screenshot)
*Player (blue) snake competing against 4 AI snakes with collectible food particles*

### Game Arena Close-up
![Arena Detail](https://via.placeholder.com/640x640?text=Arena+Detail)
*Detailed view showing snake rendering, particle effects, and collision areas*

### Snake Design
![Snake Visual](https://via.placeholder.com/320x240?text=Snake+Head+Design)
*Custom-rendered snake head with eyes and directional arrow*

---

## 🧠 Learning Resources

This project demonstrates:
- **Object-Oriented Programming** - Class inheritance, polymorphism
- **Game Development Fundamentals** - Game loop, delta-time, rendering
- **Physics Simulation** - Acceleration, velocity, smooth movement
- **Vector Mathematics** - Direction, angle, normalization
- **Collision Detection** - AABB (rectangle) collisions, point collisions
- **Asset Generation** - Procedural graphics with Pygame

Great for:
- 🎓 Learning game development
- 📚 Building portfolio projects
- 💼 Internship/junior developer applications
- 🎮 Extending into more complex games

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

You are free to:
- ✅ Use in personal and commercial projects
- ✅ Modify and distribute
- ✅ Use for learning and educational purposes

Please include attribution if used professionally.

---

## 👤 Author

Created as a learning project in game development.

---

## 💬 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with improvements

---

## 🐛 Known Issues

- Collision end conditions not fully implemented (snakes don't "die" on collision)
- `gameboard` class partially implemented but not used
- No pause or game over screen
- No UI elements or menus

See [Future Improvements](#-future-improvements) for planned features.

---

## 📧 Feedback

Have suggestions or found a bug? Feel free to open an issue or reach out!

---

**Last Updated:** July 27, 2026  
**Status:** Active Development  
**Version:** 1.0

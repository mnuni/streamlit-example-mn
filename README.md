# Python Game Collection

A collection of classic games built with Python and Pygame, including Pong and a Stunt Car Racer-inspired racing game.

## Games Included

### 1. Pong Game
A classic Pong game where you play against an AI opponent. Control your paddle to hit the ball back and forth, trying to score points by making the ball pass your opponent's paddle.

### 2. Stunt Car Racer (Racing Game)
An adrenaline-pumping 3D racing game inspired by the classic Amiga game "Stunt Car Racer". Features wireframe vector graphics, elevated tracks with jumps and ramps, realistic physics, and challenging track design.

## Features

### Pong Game
- Player vs AI gameplay
- Real-time score tracking
- Smooth paddle and ball movement
- Simple and intuitive controls
- Classic Pong mechanics with bouncing physics

### Racing Game (Stunt Car Racer)
- 3D wireframe vector polygon graphics
- Elevated track system with support pillars
- Realistic car physics (acceleration, braking, gravity, momentum)
- Challenging track design featuring:
  - Steep ramps and elevation changes
  - Dramatic jumps and airborne sections
  - Banked turns
  - Hills and valleys
  - Multiple checkpoints
- Dynamic camera following the car with 3D perspective
- Boost system with recharge mechanic
- Real-time UI displaying:
  - Speedometer
  - Lap timer
  - Boost meter
  - Lap counter
  - Ground/airborne status
- Wireframe aesthetic faithful to the original Stunt Car Racer

## Requirements

- Python 3.7 or higher
- Pygame 2.5.0 or higher

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

### Pong Game
Run the Pong game using Python:

```bash
python pong_game.py
```

### Racing Game (Stunt Car Racer)
Run the racing game using Python:

```bash
python racing_game.py
```

## How to Play

---

### Pong Game

#### Controls

- **W** - Move paddle up
- **S** - Move paddle down
- **ESC** - Quit game

#### Gameplay

- Your paddle is on the left side of the screen
- The AI opponent's paddle is on the right side
- Use the W and S keys to move your paddle up and down
- Try to hit the ball with your paddle to send it toward your opponent
- If the ball passes your opponent's paddle, you score a point
- If the ball passes your paddle, your opponent scores a point
- The game continues indefinitely - play as long as you like!

#### Scoring

- Player score is displayed on the left side at the top
- AI score is displayed on the right side at the top
- Each time the ball passes a paddle, the opposing player scores one point

#### Tips

- Anticipate where the ball will be rather than reacting to where it is
- Try to hit the ball at different angles by positioning your paddle strategically
- The AI is programmed to follow the ball, but it's not perfect - exploit its weaknesses!

---

### Racing Game (Stunt Car Racer)

#### Controls

- **UP Arrow** - Accelerate/Throttle
- **DOWN Arrow** - Brake/Reverse
- **LEFT Arrow** - Steer left
- **RIGHT Arrow** - Steer right
- **SPACE Bar** - Activate boost (when available)
- **ESC** - Quit game

#### Gameplay

- Navigate the challenging elevated track with jumps, ramps, and banked turns
- Use throttle to accelerate and build speed
- Use brake to slow down before sharp turns or when landing from jumps
- Steer left and right to navigate the winding track
- Activate boost for extra speed when needed (boost meter must have charge)
- Stay on the track and avoid falling off the elevated sections
- Complete laps as fast as possible

#### Game Elements

- **Speed Display** - Shows your current velocity in the top-left corner
- **Boost Meter** - Blue bar showing available boost energy (recharges automatically)
- **Lap Timer** - Displays elapsed time in minutes and seconds
- **Lap Counter** - Shows which lap you're currently on
- **Status Indicator** - Shows whether you're on the ground or airborne
- **Checkpoints** - Red-tinted track sections mark progress milestones

#### Track Features

The track includes various challenging sections:
- **Launch Ramps** - Build speed to launch your car into the air
- **Elevated Sections** - High sections supported by pillars (don't fall off!)
- **Jumps** - Gaps in the track requiring precise speed and timing
- **Banked Turns** - Curved sections with banking for high-speed cornering
- **Hills** - Undulating terrain that affects speed and visibility

#### Physics & Strategy

- **Gravity** - Your car is affected by gravity when airborne
- **Momentum** - Speed carries through jumps and over hills
- **Air Control** - Limited steering while airborne
- **Boost Management** - Use boost strategically; it recharges slowly
- **Landing** - Land smoothly on the track to maintain speed
- **Track Position** - Stay centered on the track for optimal control

#### Tips

- Build up speed on straightaways before approaching jumps
- Brake before sharp turns to maintain control
- Use boost on uphill sections or long straights
- Time your jumps to land smoothly on the track
- Watch the track ahead to anticipate elevation changes
- Keep an eye on your boost meter - don't waste it all at once
- The wireframe view helps you see upcoming track features

---

## Technical Details

### Pong Game Mechanics

- The ball bounces off the top and bottom walls
- The ball bounces off paddles when they make contact
- The AI opponent automatically tracks and follows the ball
- The ball resets to the center after each point is scored

### Racing Game Technical Features

- **3D Perspective Projection** - Real 3D-to-2D projection with camera system
- **Vector Graphics** - All rendering uses wireframe polygon graphics
- **Physics Engine** - Custom physics including:
  - Gravity and vertical velocity
  - Friction and air resistance
  - Acceleration and momentum
  - Ground collision detection
- **Track System** - Procedurally positioned track segments with:
  - Curved sections using trigonometry
  - Elevation changes and banking
  - Support pillars for elevated sections
- **Camera System** - Dynamic 3D camera that follows the car with rotation
- **Checkpoint System** - Track progress monitoring for lap detection

### Graphics Style

The racing game captures the iconic wireframe aesthetic of the original Stunt Car Racer on the Amiga:
- Vector polygon rendering for all 3D objects
- Wireframe track with visible edges
- Simple geometric car representation
- Minimal but functional UI
- High-contrast color scheme (black background with bright colored lines)
- Visible support structures for elevated track sections

---

Enjoy playing both games!

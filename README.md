# Pong Game

A simple, playable implementation of the classic Pong game built with Python and Pygame.

## Description

This is a classic Pong game where you play against an AI opponent. Control your paddle to hit the ball back and forth, trying to score points by making the ball pass your opponent's paddle.

## Features

- Player vs AI gameplay
- Real-time score tracking
- Smooth paddle and ball movement
- Simple and intuitive controls
- Classic Pong mechanics with bouncing physics

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

Run the game using Python:

```bash
python pong_game.py
```

## How to Play

### Controls

- **W** - Move paddle up
- **S** - Move paddle down
- **ESC** - Quit game

### Gameplay

- Your paddle is on the left side of the screen
- The AI opponent's paddle is on the right side
- Use the W and S keys to move your paddle up and down
- Try to hit the ball with your paddle to send it toward your opponent
- If the ball passes your opponent's paddle, you score a point
- If the ball passes your paddle, your opponent scores a point
- The game continues indefinitely - play as long as you like!

### Scoring

- Player score is displayed on the left side at the top
- AI score is displayed on the right side at the top
- Each time the ball passes a paddle, the opposing player scores one point

## Game Mechanics

- The ball bounces off the top and bottom walls
- The ball bounces off paddles when they make contact
- The AI opponent automatically tracks and follows the ball
- The ball resets to the center after each point is scored

## Tips

- Anticipate where the ball will be rather than reacting to where it is
- Try to hit the ball at different angles by positioning your paddle strategically
- The AI is programmed to follow the ball, but it's not perfect - exploit its weaknesses!

Enjoy playing Pong!

# Super Mario Game
![Screenshot (2274)@2x](https://user-images.githubusercontent.com/63051195/127716242-92a7ad28-8fd3-4722-93c6-0a835db0761c.png)

Welcome to the Super Mario game, a Python-based 2D platformer where you control Mario. The game features classic gameplay with modern code! Mario has 3 lives, must avoid falling mushrooms, and dodge crabs moving across the screen. Can you help Mario survive?

## Table of Contents
- [Game Features](#game-features)
- [Gameplay](#gameplay)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Create and Activate a Virtual Environment](#step-2-create-and-activate-a-virtual-environment)
  - [Step 3: Install Dependencies](#step-3-install-dependencies)
  - [Step 4: Run the Game](#step-4-run-the-game)
- [Game Controls](#game-controls)
- [Code Structure](#code-structure)
- [Development Guidelines](#development-guidelines)
- [Future Features](#future-features)
- [Contributing](#contributing)
- [License](#license)
  
## Game Features
![start](https://user-images.githubusercontent.com/63051195/127716191-a9336c92-7711-4da4-9520-0d12ac0d14a4.png)
- **3 Lives**: Mario starts with 3 lives. Once all lives are lost, it's game over.
- **Falling Mushrooms**: Mushrooms fall from the sky at random positions. Avoid them to stay alive.
- **Moving Crabs**: Crabs move horizontally from left to right across the screen. Avoid getting hit by them.
- **Classic Controls**: Use arrow keys to move Mario left and right, and the spacebar to jump.
- **Dynamic Gameplay**: As you progress, the speed of falling mushrooms and moving crabs increases, making the game more challenging.
# Start Game

## Gameplay
![Screenshot (2276)@2x](https://user-images.githubusercontent.com/63051195/127716301-52eaf911-b35a-466b-ad95-22beeaf7504f.png)
The goal of the game is to avoid obstacles (mushrooms and crabs) for as long as possible. You start with 3 lives, and each time you hit a mushroom or crab, you lose a life. When all lives are lost, the game ends.

The game progressively becomes harder, with obstacles increasing in speed, testing your reflexes and timing.

## Installation

Follow the steps below to install and run the Super Mario game on your local machine.

### Prerequisites

- **Python 3.x**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **PyCharm**: (Optional but recommended) Use PyCharm IDE for better development experience. You can download it from [jetbrains.com](https://www.jetbrains.com/pycharm/download/).

### Step 1: Clone the Repository



Start by cloning the GitHub repository:

```bash
git clone https://github.com/elliot31878/SuperMarioGame.git
cd SuperMarioGame
pip install -r requirements.txt

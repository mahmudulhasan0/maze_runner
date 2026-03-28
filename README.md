Maze Runner

rack
Track 1 - Game (Pygame)

Project Title
Maze Runner

Project Description
Maze Runner is a Python Pygame-based maze escape game.  
The player must collect the key, avoid enemies and traps, and reach the exit door before time runs out.  
The game includes multiple levels, scoring, lives, top 10 score saving, bonus items, settings save, and menu screens.

Main Features
- Player movement using Arrow keys or WASD
- Maze walls with collision
- Key and door system
- Win condition
- Enemy patrol and smart chasing behavior
- Trap collision
- Lives system
- Bonus collectible item
- Timer
- Score system
- Top 10 score saving
- Settings save
- Start menu
- High score screen
- Settings screen
- Level progression across 3 levels
- Restart and exit options

OOP Classes Used
- `Player`
- `Enemy`
- `Trap`
- `KeyItem`
- `Door`
- `BonusItem`
- `Maze`
- `LevelManager`
- `Storage`
- `GameEngine`

Composition / OOP Design
The project uses Object-Oriented Programming with clear responsibility separation:
- `GameEngine` controls the full game flow
- `Player`, `Enemy`, `Trap`, `KeyItem`, `Door`, and `BonusItem` represent game objects
- `Maze` handles layout and wall collision
- `LevelManager` handles progression between levels
- `Storage` handles score and settings persistence

Persistence
The project saves:
- Top 10 scores in `data/highscore.json`
- Settings in `data/settings.json`

Controls
Menu
- `S` = Start Game
- `H` = View Top 10 Scores
- `G` = Open Settings
- `Q` = Quit

High Score Screen
- `B` = Back to Menu

Settings Screen
- `1` = Toggle Smart Enemy
- `2` = Toggle Show Hints
- `3` = Change Starting Lives
- `B` = Back to Menu

Gameplay
- `Arrow Keys` or `WASD` = Move
- `ESC` = Quit

 After Level Complete
- `N` = Next Level
- `R` = Restart Game
- `M` = Back to Menu

After Game Over / Final Win
- `R` = Restart Game
- `M` = Back to Menu

Setup Instructions
Create virtual environment
bash
python -m venv .venv
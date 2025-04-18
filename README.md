### Author
**Skwierczyński Konrad**

# Sokoban Game

The program is centered around using OOP paradigms to reconstruct the popular puzzle game, **Sokoban**. Sokoban is a puzzle game where the player controls a character tasked with pushing boxes onto designated target locations within a maze-like environment.  
The minor conceptual difference in this version is that there are **buttons** that need to be pressed instead of holding places, and boxes are represented as **barrels** for aesthetic purposes.

## Gameplay

The board has a maximum size of **16x16** and consists of squares representing **floor** (light grey) as well as **walls** (dark grey). On some of the floor tiles, there are **red squares**, which represent buttons. The number of these buttons corresponds to the number of boxes in each level.

The **Player** (represented by a **knight sprite**) uses the **WASD keys** to move around. They can only step on **stepable** (floor and button) tiles. The player can push a **box** (represented as a **barrel sprite**) by stepping on the tile containing the box. Boxes cannot be pushed out of bounds, onto walls, or another box.

The aim of the game is to complete all the levels. In order to pass to the next level, the player must position all the boxes on top of the buttons. To prevent softlock situations, the program includes a restart option (**R-key** or restart button), and to avoid tiresome repetitiveness, an undo option is available (**U-key** or undo button).

## Program Structure

The program is structured into three modules, each handling a specific aspect of the game:

1. **Model**:  
   - Handles the game logic, including tile representation, agents, and board management.
   - Includes classes for **Tiles**, **Agents**, **Board**, **Game** logic, and **Exceptions**.
  
2. **GUI**:  
   - The graphical interface consists of three views: the **menu screen**, **game window**, and **pass screen**. 
   - These are managed by an overarching widget responsible for switching screens.

3. **Load data**:  
   - Data is loaded from **JSON files** containing the level information.

### Tile Classes

**Tile Classes** represent the different types of tiles in the game:

- **InaccesibleTile**:  
  Represents a **wall** tile that cannot be stepped on.

- **StepableTile**:  
  Represents a **floor** tile that can be occupied.

- **ButtonTile**:  
  Represents a **button** tile that must contain a box to meet the level's completion conditions.

### Agent Class

The **Agent** class represents the player or a box. Each agent can move either through user input or game logic occurrences.

### Board Class

The **Board** class stores information about the game board, including tiles and buttons. It is responsible for handling non executive game logic (e.g., marking tiles as occupied, checking the validity of moves).

### Game Class

The **Game** class handles the main game logic, including storing game data (level id, title, board, player, boxes, number of moves), loading levels, and verifying completion conditions.

### Exceptions

Custom exceptions are raised to handle various errors in the game, particularly due to faulty level data:

- **InvalidTile**: Raised when a tile is invalid.
- **InvalidOccupation**: Raised when an agent attempts to move to an invalid tile.
- **AgentsOverlapping**: Raised when two agents overlap.
- **InvalidCoordinates**: Raised when coordinates are invalid or out of bounds.

## Level Data

In the `load_level.py` module, the `get_level()` function gathers level data from a JSON file and initializes respective game objects.

Level JSON files have to be named `{level_id}.json` where `level_id` are consecutive whole numberes starting from 0. Level files are NOT to be named by the level title. It can be freely set in the title section of the JSON file.
### Example of a Level File (e.g., '0.json')

```json
{
    "title": "Level 0 - Example",
    "tiles":[
        {"id":[0, 0], "type": "floor"},
        {"id":[1, 0], "type": "floor"},
        {"id":[0, 1], "type": "floor"},
        {"id":[1, 1], "type": "floor"},
        {"id":[1, 2], "type": "wall"},
        {"id":[0, 2], "type": "button"},
        {"id":[0, 3], "type": "floor"}
    ],
    "player_pos": [0, 0],
    "boxes": [
        {"id": 0, "position":[0, 1]}
    ]
}
```

## Use and Configuration
Program was written and tested on **Python 3.12**. 
It only supports **graphical user interface**.  

Before running the program install required packages.
```sh
pip install -r requirements.txt
```

To run the program simply run `main.py` with python while in the correct directory.
```sh
python main.py
```
or
```sh
python3 main.py
```

## Discussion
While the game functions as intended, there are some potential issues to adress:
- **Multiple player agents**: Initially considered adding support for multiple player agents (controlled by the same user) but decided against it to avoid unnecessary complexity.
- **Graphical Interface**: The GUI could be further refined. Adding custom assets would significantly improve the visual experience.
- **Window size and scaling**: Currently, the window has a minimal size to fit the sprites. Basic scaling options would improve the user experience.
- **Border Walls**: Condition to prevent agents from going out of bounds seems redundant as most Sokoban levels for aesthetic reasons are designed with walls all around.   
The upsides of not needing the walls as a border are: shorter files that represent levels, and leaving more space for puzzle design and player movement (a true **16x16** board instead of **14x14** when you take away the border).
- **Level representation as a file**: In hindsight JSON files seem a bit awkward and lengthly. Perhaps YAML representation would be more human friendly
- **Assets** were taken from `https://sethbb.itch.io/32rogues` (free assets by user Seth, license included in assets folder)

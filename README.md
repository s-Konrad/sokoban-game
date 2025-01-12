### Author
**Skwierczyński Konrad**,
Student id: 337 284

# Skokoban Game
The program is centered around using OOP paradigms to reconstruct popular puzzle game - Sokoban. The minor conceptiual difference is that in this version there are buttons that need to be pressed instead of holding places.

## Gameplay
The board has the maximum size of 16x16 and consists of squares representing floor (light grey) as well as walls (dark grey). On some of the floor tiles there are red squares. They represent buttons which number coresponds to the number of boxes in each level. 

Player uses WASD keys to move around. They can only step on stepable (floor and button) tiles. They can push a box (small beige square) by steping on the tile that contains said box. Boxes cannot be pushed out of bounds, on top of a wall or another box.  

The aim of the game is to complete all of the levels. In order to pass to the next level player has to position all of the presented boxes on top of the buttons. To prevent softlock situations, restart option is provided (R-key or restart button), and to prevent, tiresome repetitiveness undo option is facilicated (U-key or undo button).

# Program structure
The program is structured around three modules focused respectively on: loading level data from file, executing game logic, implementing GUI.

## Gui

Graphical interface consists of three views: menu screen, game window, pass screen. They are handled by an overarching widget that stores them and is responsible for switching screens.

## Model

#### Tile Classes
Responsible for implementing diferent types of tiles.

- **InaccesibleTile**:
Class representing a wall tile that cannot be stepped on.
- **StepableTile**:
Class rapresenting a floor tile that differs from a wall tile by having methods regarding its ocupation.
- **ButtonTile**:
Class representing a button tile that has to contain a box regarding level completion conditions.

#### Agent
Class which independed instances are able to move either by user input or game logic occuriences.

#### Board
Class that stores information about a board (tiles, buttons) and is respponsible for handling non executive game logic (marks tiles that have a box on them, checks board correctnes, checks if a move is valid).

#### Game
Main game logic class that stores game data (level id, title, board, player, boxes, number of moves made by the player) and renders avaliable methods responsible for loading a level, move handling and checking if level completion conditions are satisfied.

#### Exceptions
There is a number of custom exceptions that are raised when an error occurs usually because of faulty level data.
- InvalidTile
- InvalidOcupation
- AgentsOverlaping 
- InvalidCoordinates   

Each of them notifies the user with a short message regarding the issue.

## Get level data from files
In the `load_level.py` module there is one main function (`get_level`) that uses three helper function to gather level data from given .json file and initialize respective objects.

### Example of level file
#### '0.json'
``` JSON
{
    "title": "Level 0 - Example",
    "tiles":[
        {
            "id":[0, 0],
            "type": "floor"
        },
        {
            "id":[1, 0],
            "type": "floor"
        },
        {
            "id":[0, 1],
            "type": "floor"
        },
        {
            "id":[1, 1],
            "type": "floor"
        },
        {
            "id":[1, 2],
            "type": "wall"
        },
        {
            "id":[0, 2],
            "type": "button"
        },
        {
            "id":[0, 3],
            "type": "floor"
        }
    ],
    "player_pos": [0, 0],
    "boxes": [
        {
            "id": 0,
            "position":[0, 1]
        }
    ]
}
```


## Use and Configuration
Program was written and tested on Python 3.12. 
Program supports only graphical user interface.  
Level JSON files have to be named {level_id}.json where level_id are consecutive whole numberes starting from 0. Level files are NOT to be named by the level title. It can be freely set in the title section of the JSON file.

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
There are some potential issues to adress.  
- During the planning phase there was an idea regarding  support for multiple player agents (still controled by one user), but it was shelved as it was not requred and wolud cause some bloating to the code.
- Graphical user interface isn't polished and would greatly benefit from some assets.
- Another GUI related topic is one regarding size of the window and sliders. Currently minimal size of the winndow is set, to reserve space for 'sprites'. Basic scaling would be appreciated.
- Condition to prevent agents from going out of bounds seems redundant as most Sokoban levels for aesthetic reasons are designed with walls all around.   
The upsides of not needing the walls as a border are: shorter files that represent levels, and leaving more space for puzzle design and player movement (a true 16x16 board instead of 14x14 when you take away the border).
- In hindsight JSON files seem a bit awkward and lengthly. Perhaps YAML representation would be more human friendly

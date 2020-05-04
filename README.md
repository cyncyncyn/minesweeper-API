# Minesweeper API:
Local run:

1. Create virtualenv
2. `pip install -r requirements.txt`
3. Run server `python manage.py runserver`
4. Open `http://localhost:8000`
5. Enjoy!
6. Run tests `python manage.py test`

## The API
### Game status:
* PLY: Game still playing
* WON: Game won
* LST: Game lost


### Get existing board `GET /game/board/<board_id>/`
#### Request:

```bash
curl localhost:8000/game/board/<board_id>/
```
Parameters:
  * board_id: (UUID) Id of the board

#### Response examples:

* 200:
  * `{"model": "game.board", "pk": "954c7fd3-c982-4d25-a9fa-41937cf83ac3", "fields": {"width": 8, "height": 8, "amount_of_mines": 10, "status": "PLY"}}`
* 404:
  * `{"message": "Board does not exist"}`


### Create board `POST /game/board/`
#### Request:

```bash
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"width":5,"height":6, "mines": 4}' \
  localhost:8000/game/board/
```

Parameters:
  * width int (optional): Width of the board, default 8
  * height int (optional): Height of the board, default 8
  * mines int (optional): Amount of mines, default 10

#### Example responses:

* 200:
  * `{"model": "game.board", "pk": "647e5502-7f0a-4eb9-9e4b-082661fa84b3", "fields": {"width": 5, "height": 6, "amount_of_mines": 4, "status": "PLY"}`
    * pk(string): UUID of the generated board
    * fields (object): Field that returns the game config, as width, height, amount_of_mines and status of the game.


### Click cell `POST game/click/`
#### Request:
```bash
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"x":2,"y":7, "boardId": "647e5502-7f0a-4eb9-9e4b-082661fa84b3"}' \
  localhost:8000/game/click/
```

Parameters:
  * x int: x position of the cell
  * y int: y position of the cell
  * boardId uuid: id of the board

#### Example responses

* 200:
  * `{"adjacents_to_uncover": [], "game_status": "PLY"}`
    * `adjacents_to_uncover`: List of all adjacent neighbours until a mine is found, as x,y tuples
  * `game_status`: WON, LST or PLY
* 400:
  * `{"message": "x, y and boardId are required"}`
  * `{"game_status": "LST"}` Game Over!
* 404:
  * `{"message": "Cell does not exist for given board"}`
  * `{"message": "Board does not exist"}`



### Flag cell `POST game/flag/`
#### Request:
```bash
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"x":2,"y":7, "boardId": "647e5502-7f0a-4eb9-9e4b-082661fa84b3"}' \
  localhost:8000/game/flag/
```

Parameters:
  * x int: x position of the cell
  * y int: y position of the cell
  * boardId uuid: id of the board

#### Example responses

* 200:
  * `{"is_flagged": true, "is_uncovered": false}`
    * `is_flagged`: True if cell got flagged or is already flagged.
    * `is_uncovered`: True if cell is already uncovered.
* 400:
  * `{"message": "x, y and boardId are required"}`
* 404:
  * `{"message": "Cell does not exist for given board"}`
  * `{"message": "Board does not exist"}`


# Decisions made:

## Technologies
The game logic and API was developed in Python 3, using the Django framework for expediency.
The API client was developed in JavaScript (With HTML and CSS).

## The project

### V 1.5

Functionalities added:
* Ability to 'flag' a cell with a question mark or red flag (for time issues right now the flag is an orange cell)
* Detect when game is over
* Persistence
* Time tracking
* [Partial] Ability to start a new game and preserve/resume the old ones. Now you can get a non finished game. Frontend part is not yet implemented
* Ability to select the game parameters: number of rows, columns, and mines

### V 1.0
In order of arriving in time, the decision was to create a prototype of the game to be presented in a client meeting.
The first effort made was creating a hardcoded board that worked as expected (particularly the part of finding the adjacent cells with/without mines)

Once the logic of the game was working there were a refactor to pseudo-randomize the board.

As persistence was not implemented (because of short time) the decision was to generate 10 random boards and save them in the Django settings. Those would only change if the server is reset. However, every time you hit f5 in the website, you get a random board from those 10.

The part of losing the game is implemented, as it was trivial. However the winning part should have a little bit more of coding, in a future iteration (by calculating  `total_cells - total_mines` and validating onClick if that number matches the number of revealed cells).


## Suggested features:
* Number of adjacent mines on uncovered cells.
* Reveal board when game is finished.

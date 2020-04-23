# Minesweeper API:
Local run:

1. Create virtualenv
2. `pip install -r requirements.txt`
3. Run server `python manage.py runserver`
4. Open `http://localhost:8000`
5. Enjoy!
6. Run tests `python mange.py test`

## The API
### GET /game/board/
#### Request:

```bash
  curl localhost:8001/game/board/
```

#### Responses:

* 200: `{"boardSize": int, "boardId": int}`

boardSize (int):  is now hardcoded in 8, could be randomized in future iterations.

boardId(int): Until now there are 10 possible boards saved on the server, until persistence is implemented

### POST game/click/
#### Request:
```bash
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"x":2,"y":7, "boardId": 1}' \
  localhost:8001/game/click/
```

#### Responses

* 200: `[[]]` List of all adjacent neighbours until a mine is found 
* 400: `{}` Game OVER!

##### Example of 200 response:

```
[[1, 6], [1, 7], [0, 6], [0, 5], [0, 7], [1, 5], [2, 6], [3, 6], [3, 7], [4, 6], [4, 7], [5, 6], [5, 7], [6, 6], [6, 7], [7, 6], [6, 5], [7, 5], [6, 4], [7, 4], [6, 3], [5, 2], [5, 3], [5, 4], [6, 2], [5, 1], [6, 1], [7, 1], [7, 2], [7, 3], [7, 7]]
```

# Decisions made:

## Technologies
The game logic and API was developed in Python 3, using the Django framework for expediency.
The API client was developed in JavaScript (With HTML and CSS).

## The project
In order of arriving in time, the decision was to create a prototype of the game to be presented in a client meeting.
The first effort made was creating a hardcoded board that worked as expected (particularly the part of finding the adjacent cells with/without mines)

Once the logic of the game was working there were a refactor to pseudo-randomize the board.

As persistence was not implemented (because of short time) the decision was to generate 10 random boards and save them in the Django settings. Those would only change if the server is reset. However, every time you hit f5 in the website, you get a random board from those 10.

The part of losing the game is implemented, as it was trivial. However the winning part should have a little bit more of coding, in a future iteration (by calculating  `total_cells - total_mines` and validating onClick if that number matches the number of revealed cells).
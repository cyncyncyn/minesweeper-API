import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from game.models import Cell, Board, BOARD_SIZE, MINES_AMOUNT
from game.services import find_adjacents, validate_game_finished


def get_board(request, board_id):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return JsonResponse({"message": "Board does not exist"}, status=404,
                            safe=False)
    serialized_board = serializers.serialize("json", [board])

    return JsonResponse(
            json.loads(serialized_board)[0], safe=False)


@csrf_exempt
def create_board(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except (json.JSONDecodeError):
            data = {}

        width = int(data.get('width', BOARD_SIZE))
        height = int(data.get('height', BOARD_SIZE))
        amount_of_mines = int(data.get('mines', MINES_AMOUNT))

        board = Board(width=width, height=height,
                      amount_of_mines=amount_of_mines)
        board.save()
        board.generate_cells()
        serialized_board = serializers.serialize("json", [board])

        return JsonResponse(
                json.loads(serialized_board)[0], safe=False)


def index(request):
    return render(request, template_name="game/index.html")


def get_cell(body):
    data = json.loads(body.decode('utf-8'))
    x = int(data["x"])
    y = int(data["y"])
    board_id = data["boardId"]

    board = Board.objects.get(pk=board_id, status=Board.PLAYING)
    cell = board.cell_set.get(row=x, col=y)
    return cell


@csrf_exempt
def click(request):
    if request.method == 'POST':
        try:
            cell = get_cell(request.body)
        except (KeyError,  json.JSONDecodeError):
            return JsonResponse({"message": "x, y and boardId are required"},
             status=400, safe=False)
        except Cell.DoesNotExist:
            return JsonResponse({"message": "Cell does not exist for given board"},
             status=404, safe=False)
        except Board.DoesNotExist:
            return JsonResponse({"message": "Board does not exist"},
             status=404, safe=False)

        if cell.is_mine:
            cell.board.status = Board.LOST
            cell.board.save()
            return JsonResponse({"game_status": Board.LOST}, status=400,
                                safe=False)

        cell.is_uncovered = True
        cell.save()

        adjacents = find_adjacents(cell.board, cell.row, cell.col)
        is_game_won = validate_game_finished(cell.board)

        game_status = Board.WON if is_game_won else Board.PLAYING
        if is_game_won:
            cell.board.status = Board.WON
            cell.board.save()

        return JsonResponse({"adjacents_to_uncover": adjacents,
                            "game_status": game_status}, status=200,
                            safe=False)


@csrf_exempt
def flag(request):
    if request.method == 'POST':
        try:
            cell = get_cell(request.body)
        except (KeyError,  json.JSONDecodeError):
            return JsonResponse({"message": "x, y and boardId are required"}, status=400, safe=False)
        except Cell.DoesNotExist:
            return JsonResponse({"message": "Cell does not exist for given board"}, status=404, safe=False)
        except Board.DoesNotExist:
            return JsonResponse({"message": "Board does not exist"}, status=404, safe=False)

        if not cell.is_uncovered:
            cell.is_flagged = not cell.is_flagged
            cell.save()

        return JsonResponse({"is_flagged": cell.is_flagged,
                            "is_uncovered": cell.is_uncovered}, status=200,
                            safe=False)

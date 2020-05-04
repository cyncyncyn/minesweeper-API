import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from game.models import Board, Cell
from game.services import (board_to_list, create_game, find_adjacents,
                           get_cell, uncover_cells, validate_game_finished)


def index(request):
    return render(request, template_name="game/index.html")


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

        width = int(data.get('width', Board.DEFAULT_BOARD_SIZE))
        height = int(data.get('height', Board.DEFAULT_BOARD_SIZE))
        amount_of_mines = int(data.get('mines', Board.DEFAULT_MINES_AMOUNT))

        board = create_game(width, height, amount_of_mines)
        serialized_board = serializers.serialize("json", [board])

        return JsonResponse(
                json.loads(serialized_board)[0], safe=False)


@csrf_exempt
def click(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            cell = get_cell(data)
        except (KeyError,  json.JSONDecodeError):
            return JsonResponse({"message": "x, y and boardId are required"},
                                status=400, safe=False)
        except Cell.DoesNotExist:
            return JsonResponse(
                {"message": "Cell does not exist for given board"},
                status=404, safe=False)
        except Board.DoesNotExist:
            return JsonResponse({"message": "Board does not exist"},
                                status=404, safe=False)

        if cell.is_mine:
            cell.board.status = Board.LOST
            cell.board.save()
            return JsonResponse({"game_status": Board.LOST}, status=400,
                                safe=False)

        # TODO: move this to a service
        cell.is_uncovered = True
        cell.save()

        board = cell.board
        cells = cell.board.cell_set.all()

        list_board = board_to_list(board, cells)
        adjacents = find_adjacents(list_board, cell.row, cell.col)

        uncover_cells(cells, adjacents)

        is_game_won = validate_game_finished(board)

        game_status = Board.WON if is_game_won else Board.PLAYING
        if is_game_won:
            board.status = Board.WON
            board.save()

        return JsonResponse({"adjacents_to_uncover": adjacents,
                            "game_status": game_status}, status=200,
                            safe=False)


@csrf_exempt
def flag(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            cell = get_cell(data)
        except (KeyError,  json.JSONDecodeError):
            return JsonResponse(
                {"message": "x, y and boardId are required"}, status=400,
                safe=False)
        except Cell.DoesNotExist:
            return JsonResponse(
                {"message": "Cell does not exist for given board"}, status=404,
                safe=False)
        except Board.DoesNotExist:
            return JsonResponse(
                {"message": "Board does not exist"}, status=404, safe=False)

        if not cell.is_uncovered:
            cell.is_flagged = not cell.is_flagged
            cell.save()

        return JsonResponse({"is_flagged": cell.is_flagged,
                            "is_uncovered": cell.is_uncovered}, status=200,
                            safe=False)

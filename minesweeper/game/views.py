import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from game.models import Board
from game.services import find_adjacents, validate_game_finished


def get_board(request):
    # TODO: Check PK for exisitng game
    board = Board()
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

    # TODO: validate if id is not in request
    board_id = data.get("boardId", 0)

    board = get_object_or_404(Board, pk=board_id)
    cell = board.cell_set.get(row=x, col=y)

    return cell


@csrf_exempt
def click(request):
    if request.method == 'POST':
        cell = get_cell(request.body)
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
        cell = get_cell(request.body)
        if not cell.is_uncovered:
            cell.is_flagged = not cell.is_flagged
            cell.save()

        return JsonResponse({"is_flagged": cell.is_flagged,
                            "is_uncovered": cell.is_uncovered}, status=200,
                            safe=False)

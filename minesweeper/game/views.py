import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers
from django.shortcuts import get_object_or_404

from game.services import find_adjacents
from game.models import Board, Cell


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
            return JsonResponse({}, status=400, safe=False)
        adjacents = find_adjacents(cell.board, cell.row, cell.col)
        return JsonResponse(adjacents, status=200, safe=False)


@csrf_exempt
def flag(request):
    if request.method == 'POST':
        cell = get_cell(request.body)
        cell.is_flagged = not cell.is_flagged
        cell.save()

        return JsonResponse({"is_flagged": cell.is_flagged}, status=200,
                            safe=False)

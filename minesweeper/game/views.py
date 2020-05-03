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


@csrf_exempt
def click(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        x = int(data["x"])
        y = int(data["y"])

        # TODO: validate if id is not in request
        board_id = data.get("boardId", 0)

        board = get_object_or_404(Board, pk=board_id)
        cell = board.cell_set.get(row=x, col=y)

        if cell.is_mine:
            return JsonResponse({}, status=400, safe=False)
        adjacents = find_adjacents(board, x, y)
        return JsonResponse(adjacents, status=200, safe=False)

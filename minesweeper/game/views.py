import json
import random

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .services import BOARD_SIZE, find_adjacents, cell_has_mine


def get_board(request):
    return JsonResponse(
        {
            "boardSize": BOARD_SIZE,
            "boardId": random.randrange(len(settings.BOARDS))
        }, safe=False)


def index(request):
    return render(request, template_name="game/index.html")


@csrf_exempt
def click(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        x = int(data["x"])
        y = int(data["y"])

        board_id = int(data.get("boardId", 1))
        board = settings.BOARDS[board_id]

        if cell_has_mine(board, x, y):
            return JsonResponse({}, status=400, safe=False)
        adjacents = find_adjacents(board, x, y)
        return JsonResponse(adjacents, status=200, safe=False)

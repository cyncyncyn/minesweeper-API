import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .services import BOARD_SIZE, find_adjacents, cell_has_mine


def get_board(request):
    return JsonResponse({"size": BOARD_SIZE}, safe=False)

def index(request):
    return render(request, template_name="game/index.html")

@csrf_exempt
def click(request):
    if request.method == 'POST':
        coords = json.loads(request.body.decode('utf-8'))
        x = int(coords["x"])
        y = int(coords["y"])
        board = settings.BOARD
        if cell_has_mine(board, x, y):
            return JsonResponse({}, status=400, safe=False)
        adjacents = find_adjacents(board, x, y)
        return JsonResponse(adjacents, status=200, safe=False)

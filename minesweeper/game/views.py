import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def get_board(request):
    board = settings.BOARD
    return JsonResponse(board, safe=False)

def index(request):
    return render(request, template_name="game/index.html")

@csrf_exempt
def click(request):
    if request.method == 'POST':
        coords = json.loads(request.body.decode('utf-8'))
        board = settings.BOARD

        for cell in board:
            if cell["x"] == int(coords["x"]) and \
               cell["y"] == int(coords["y"]) and cell["mine"] is True:
                return JsonResponse({}, status=400, safe=False)
        return JsonResponse({}, status=200, safe=False)

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render

def get_board(request):
    board = settings.BOARD
    return JsonResponse(board, safe=False)

def index(request):
    return render(request, template_name="game/index.html")
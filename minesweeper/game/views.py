from django.http import JsonResponse
from django.conf import settings

def get_board(request):
    board = settings.BOARD
    return JsonResponse(board, safe=False)


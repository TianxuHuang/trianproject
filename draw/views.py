from django.shortcuts import render

def draw_index(request):
    return render(request, 'draw/index.html')

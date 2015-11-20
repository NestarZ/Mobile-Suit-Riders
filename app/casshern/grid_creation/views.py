from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import Grid

def index(request):
    return render(request, 'grid_creation/index.html')

def result(request):
    if request.method == 'POST' and request.POST.get('line_size', False):
        N = request.POST['line_size']
        M = request.POST['column_size']
        O = request.POST['obstacle_amount']
    else:
        N = 10
        M = 10
        O = 10
    grid = Grid(line_size=N,
                column_size=M,
                obstacle_amount=O,
                pub_date=timezone.now())
    grid.generate()
    grid.solve()
    grid.save()
    return render(request, 'grid_creation/result.html', {'grid': grid})

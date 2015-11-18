from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import Grid

def index(request):
    return render(request, 'grid_creation/index.html')

def result(request):
    grid = Grid(line_size=request.POST['line_size'],
                column_size=request.POST['column_size'],
                obstacle_amount=request.POST['obstacle_amount'],
                pub_date=timezone.now())
    grid.generate()
    grid.solve()
    grid.save()
    return render(request, 'grid_creation/result.html', {'grid': grid})

import os

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

# Create your views here.
from MovieListViewer import models
from MovieListViewer.forms import RequestForm


def relist_movies_lazy():
    dirs = os.listdir(".")
    for dir in dirs:
        if not models.Movie.objects.filter(directory=dir).exists():
            models.Movie.objects.create(name=os.path.basename(dir), directory=dir)

def relist_movies_full():
    dirs = os.listdir(".")
    models.Movie.objects.all().delete()
    for dir in dirs:
        models.Movie.objects.create(name=os.path.basename(dir), directory=dir)

relist_movies = {'lazy': relist_movies_lazy,
                 'full': relist_movies_full}


@user_passes_test(lambda user: user.is_authenticated)
def create_movie_list_view(request):
    if request.method == 'GET':
        relist = request.GET.get('relist', '')
        if relist and relist in relist_movies.keys():
            relist_movies[relist]()
    movies = list(models.Movie.objects.all())
    return render(request, 'movie_list.html', {'movies': movies})

@user_passes_test(lambda user: user.is_authenticated)
def create_request_view(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('request')
    else:
        form = RequestForm()
    return render(request, 'request.html', {'form': form})

@user_passes_test(lambda user: user.is_superuser)
def create_requests_view(request):
    requests = models.Request.objects.all()
    requests_groups = {}
    for r in requests:
        key = (r.user_id, models.User.objects.filter(id=r.user_id)[0].username)
        if key in requests_groups.keys():
            requests_groups[key].append(r)
        else:
            requests_groups[key] = [r]
    return render(request, 'requests.html', {'requests_group': requests_groups})
from django.shortcuts import render, redirect
from apps.dishes.models import Breeds



# Create your views here.
def renderBreeds(request):
    breeds = Breeds.objects.all()

    context = {
        'breeds': breeds
    }
    return render(request, 'breeds.html', context)


def breedDetail(request, pk):
    breed = Breeds.objects.get(id=pk)

    if request.method == 'POST':
        breed.name = request.POST['name']
        breed.breed_size = request.POST['breed_size']
        breed.life_span = request.POST['life_span']

        breed.save()
        return redirect('breeds')

    context = {
        'breed': breed
    }

    return render(request, 'breed-detail.html', context)
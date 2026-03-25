from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import GalleryImageForm
from .models import GalleryImage


def gallery_list(request):
    images = GalleryImage.objects.all()
    return render(request, 'gallery/index.html', {'images': images})

@login_required()
def upload(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = GalleryImageForm()

    return render(request, 'gallery/upload.html', {'form': form})

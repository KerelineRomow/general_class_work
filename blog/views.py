from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .forms import PostForm, LoginForm
from .models import Post, Category, Tag

def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2 + count % 2
    first_half = all[:half]
    second_half = all[half:]
    return {'cat_left': first_half, 'cat_right': second_half}

def get_tags():
    return {'all_tags': Tag.objects.all()}

def index(request):
    posts = Post.objects.all().order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    context.update(get_tags())
    return render (request, 'blog/index.html', context)


def contact(request):
    context = {}
    return render(request, 'blog/contact.html', context)

def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    context = {'post': post}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, 'blog/post.html', context)

def category(request, slug=None):
    c = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=c).order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, 'blog/index.html', context)

def tag_detail(request, slug=None):
    t = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=t).order_by("-published_date")
    context = {'posts': posts, 'current_tag': t}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, 'blog/index.html', context)


def search(request):
    query = request.GET.get("query")
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)

@login_required
def create_post(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():

            new_post = form.save(commit=False)
            new_post.published_date = now()
            new_post.user = request.user
            new_post.save()
            form.save_m2m() # only for many to many

            return index(request)
    form = PostForm()
    context = {'form': form}
    return render(request, 'blog/create.html', context)


def user_login(request, form=None):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")

    form = LoginForm()
    context = {'form': form}
    return render(request, 'registration/login.html', context)


def user_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect('home')

    context = {'post': post}
    context.update(get_categories())
    return render(request, 'blog/delete_confirm.html', {'post': post})
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.contrib import messages
from .forms import PostForm, LoginForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from .models import Post, Category, Tag, Profile, Subscription


def get_categories():
    all_cats = Category.objects.all()
    count = all_cats.count()
    half = count // 2 + count % 2
    first_half = all_cats[:half]
    second_half = all_cats[half:]
    return {'cat_left': first_half, 'cat_right': second_half}


def get_tags():
    return {'all_tags': Tag.objects.all()}



def index(request):
    posts = Post.objects.all().order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, 'blog/index.html', context)


def contact(request):
    context = {}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, 'blog/contact.html', context)


def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_date')

    if request.method == "POST":
        # Если не залогинен — отправляем на логин
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.username  # Автор — текущий юзер
            comment.save()
            messages.success(request, "Коментар додано!")
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
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
    query = request.GET.get("query", "")
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    context.update(get_tags())
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
            form.save_m2m()
            return redirect('home')
    else:
        form = PostForm()

    context = {'form': form} | get_categories() | get_tags()
    return render(request, 'blog/create.html', context)


def user_login(request):
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
    else:
        form = LoginForm()

    context = {'form': form} | get_categories() | get_tags()
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
    return render(request, 'blog/delete_confirm.html', {'post': post})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Аккаунт {user.username} создан!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    context = {'user': request.user}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, 'registration/profile.html', context)


@login_required
def profile_edit(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile)

    context = {'u_form': u_form, 'p_form': p_form}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, 'registration/profile_edit.html', context)


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            Subscription.objects.get_or_create(email=email)
            messages.success(request, "Дякуємо!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

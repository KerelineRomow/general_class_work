from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Favorite, Category

def product_list(request):
    products = Product.objects.all().order_by("-created_at")
    categories = Category.objects.all()
    user_favorite_ids = []
    if request.user.is_authenticated:
        user_favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': None,
        'user_favorite_ids': user_favorite_ids
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'is_favorite': is_favorite,
        'categories': categories
    })

def category_products(request, slug):
    c = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=c).order_by("-created_at")
    categories = Category.objects.all()
    user_favorite_ids = []
    if request.user.is_authenticated:
        user_favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': c,
        'user_favorite_ids': user_favorite_ids
    })

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
        messages.info(request, "Товар видалено з обраного.")
    else:
        messages.success(request, "Товар додано в обране!")
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    categories = Category.objects.all()
    return render(request, 'shop/favorites.html', {
        'favorites': favorites,
        'categories': categories
    })

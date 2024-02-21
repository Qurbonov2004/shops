from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Card, CardProduct, Category, Product, ProductImage, ProductReview, WishList


def index(request):
    card = Card.objects.all() 
    cardproduct = CardProduct.objects.all() 
    category = Category.objects.all() 
    product = Product.objects.all() 
    productimage = ProductImage.objects.all() 
    productreview = ProductReview.objects.all()
    
    user_slug = request.user.slug
    if request.user.is_authenticated:
        # Assuming you have a specific product instance, replace 'specific_product' with the actual product instance
        specific_product = Product.objects.get(pk=1)  # Replace '1' with the actual product slug
        objects = WishList.objects.filter(user=request.user, product=specific_product)
        
        is_saved = None
        if objects:
            is_saved = objects.first().slug
        else:
            is_saved = False



    is_saved = None
    # WishList uchun is_saved qiymati olish
    # if request.user.is_authenticated:  # Foydalanuvchining tizimga kirganligini tekshirish
    #     objects = WishList.objects.filter(user=request.user)
    #     if objects.product.slug==product.slug:
    #         is_saved = objects.first().slug
    #     else:
    #         is_saved = False


    context = {
        'card': card,
        'cardproduct': cardproduct,
        'category': category,
        'product': product,
        'productimage': productimage,
        'wishList': WishList.objects.filter(user=request.user),
        'productreview': productreview,
        'user': request.user,
        'is_saved': is_saved,
        'user_slug':user_slug
    }

    return render(request, 'index.html', context)







def card_product(request):
    card_products = CardProduct.objects.all()
    return render(request, 'index.html', {'card_products': card_products})


def categories(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})


def products(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})




#vazifaga



from django.shortcuts import get_object_or_404

def detail(request, slug):
    products = Product.objects.all()
    product = get_object_or_404(Product, slug=slug)

    # Check if the product has a category before accessing its slug
    category_slug = product.category.slug if product.category else None
    
    images = ProductImage.objects.filter(product_slug=product.slug)
    recomendation = Product.objects.filter(category_slug=category_slug).exclude(slug=product.slug)[:3]
    objects = WishList.objects.filter(user=request.user, product=product)
    is_saved = None
    if objects:
        is_saved = objects.first().slug
    else:
        is_saved = False

    user_review = ProductReview.objects.filter(user=request.user, product=product).first()
    baho = user_review.mark if user_review else 0
    context = {
        'products': products,
        'product': product,
        'images': images,
        'range': range(baho+1),
        'recomendation': recomendation,
        'is_saved': is_saved
    }

    return render(request, 'single.html', context)









def product_image(request):
    product_images = ProductImage.objects.all()
    return render(request, 'index.html', {'product_images': product_images})


def product_review(request):
    product_reviews = ProductReview.objects.all()
    return render(request, '.html', {'product_reviews': product_reviews})


def wishlist(request):
    wishlists = WishList.objects.all()
    return render(request, '.html', {'wishlists': wishlists})







#carts



def carts(request):
    active=Card.objects.filter(is_active=True,user=request.user)
    in_active=Card.objects.filter(is_active=False,user=request.user)
    context={
        'active':active,
        'in_active':in_active
    }
    return render(request,'cart/carts.html',context)


def cart_detail(request,slug):
    cart=Card.objects.get(slug=slug)
    items=CardProduct.objects.filter(card=cart)

    context={
        'cart':cart,
        'items':items
    }
    return render(request,'cart/cart_detail.html',context)


def cart_detail_delete(request):
    item_slug = request.GET['items_slug']
    item = CardProduct.objects.get(slug=item_slug)
    cart_slug = item.card.slug
    item.delete()
    return redirect('main:cart_detail', cart_slug)






def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    user = request.user
    active_card = Card.objects.filter(user=user, is_active=True).first()

    if not active_card:
        active_card = Card.objects.create(user=user)


    existing_product = CardProduct.objects.filter(card=active_card, product=product).first()

    if existing_product:
        existing_product.quantity += 1
        existing_product.save()
    else:
        CardProduct.objects.create(card=active_card, product=product, quantity=1)
    return redirect('main:carts')





def buy_cart(request, slug):
    cart=Card.objects.get(slug=slug , is_active=True)
    cart_products=CardProduct.objects.filter(card=cart)
    for cart_product in cart_products:
        product=cart_product.product
        product.quantity-=cart_product.quantity
        product.save()
    cart.is_active = False
    cart.save()
    return redirect('main:carts')



def create_wishlist(request):
    WishList.objects.create(
        user=request.user,
        product_slug=request.GET['product_slug']
    )

    return redirect('main:index')


def list_wishlist(request):
    objects=WishList.objects.filter(user=request.user)
    return render(request, 'wish/list.html', {'objects':objects})

from django.shortcuts import get_object_or_404, redirect

def delete_wish(request, slug):
    user = request.user
    wish = get_object_or_404(WishList, product_slug=slug, user=user)
    wish.delete()
    return redirect('main:detail')

















    








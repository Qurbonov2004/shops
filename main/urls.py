from django.urls import path
from .views import *

app_name='main'

urlpatterns=[
    path('',index, name='index'),
    path('detail/<str:slug>',detail, name='detail'),
    path('carts',carts,name='carts'),
    path('cart_detail/<str:slug>',cart_detail,name='cart_detail'),
    path('cart_detail_delete/<str:slug>',cart_detail_delete,name='cart_detail_delete'),
    path('add_to_cart/<str:slug>/', add_to_cart, name='add_to_cart'),
    path('add_to_cart/<str:slug>/', add_to_cart, name='add_to_cart'),
    path('buy_cart/<str:slug>/', buy_cart, name='buy_cart'),
    path('list_wishlist', list_wishlist, name='list_wishlist'),
    path('create_wishlist/', create_wishlist, name='create_wishlist'),
    path('delete_wish/', delete_wish, name='delete_wish'),

]
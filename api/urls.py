from django.urls import path
from . import views

urlpatterns=[
    #product
    path('product/',views.listproduct),
    path('product_detail/<str:slug>',views.product_detail),
    #category
    path('category/',views.listcategory),
    path('category/<str:slug>',views.categorydetail),
    #review
    path('review/',views.review_product),
    #cart
    path('card/',views.listcard),
    path('cardproduct/',views.listcardproduct),
    path('enterproduct/',views.listenterproduct),
    path('active-cart/',views.active_cart),
    path('inactive-cart/',views.active_cart),
    #wishlist
    path('wishlist/',views.listwishlist),
    #enter
    path('enter/',views.listenterproduct),
    #login
    path('login',views.login)
]
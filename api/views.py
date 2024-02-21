from main import models
from .serializers import *
from django.contrib.auth import authenticate

from collections import defaultdict


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token


#product
@api_view(["GET"])
def listproduct(request): #product list
    
    products=models.Product.objects.all()
    serialazer=ProductSerializer(products, many=True)
    return Response(serialazer.data)

@api_view(["GET"])
def product_detail(request, slug):
    product = models.Product.objects.get(slug=slug)
    product_ser = ProductSerializer(product)
    product_data = product_ser.data

    images = models.ProductImage.objects.filter(product=product)
    images_ser = ProductImageSerializer(images, many=True)  # Fix the typo here
    images_ser_data = images_ser.data
    product_data['images'] = {'images': images_ser_data}
    return Response(product_data)






#category
@api_view(["GET"])
def listcategory(request):#category list
    categories=models.Category.objects.all()
    serialazer=CategorySerializer(categories, many=True)
    return Response(serialazer.data)


@api_view(["GET"])
def categorydetail(request, slug):  # category detail
    products = models.Product.objects.filter(category__slug=slug)
    serializer = CategoryDetailSerializer(products, many=True)
    return Response(serializer.data)






#review
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])

def review_product(request):
    product_id = request.data.get('product_id')  # Assuming 'product_id' is in request data
    user_id = request.data.get('user_id')  # Assuming 'user_id' is in request data
    mark = request.data.get('mark')
    if product_id and user_id and mark is not None:
        try:
            review = models.ProductReview.objects.get(product_id=product_id, user_id=user_id, mark=mark)
            review.mark = mark
            review.save()
            serializer = serializers.ReviewSer(review)
            return Response(serializer.data)
        except models.ProductReview.DoesNotExist:
            review = models.ProductReview.objects.create(product_id=product_id, user_id=user_id, mark=mark)
            serializer = serializers.ReviewSer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'product_id, user_id, and mark are required fields'}, status=400)




#card
@api_view(["GET"])
def listcard(request):
    cards=models.Card.objects.all()
    serialazer=CardSerializer(cards, many=True)
    return Response(serialazer.data)



@api_view(["GET"])
def listcardproduct(request):
    cardproducts=models.CardProduct.objects.all()
    serialazer=CardProductSerializer(cardproducts, many=True)
    return Response(serialazer.data)




@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def active_cart(request):
    product = models.CartProduct.objects.filter(cart__is_active=True)
    serializer = serializers.CartSer(product, many=True)
    return Response(serializer.data)

@api_view(['GET']) 
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def inactive_cart(request):
    product = models.CartProduct.objects.filter(cart__is_active=False)
    serializer = serializers.CartSer(product, many=True)
    return Response(serializer.data)




@api_view(["GET"])
def listenterproduct(request):
    enterproducts=models.EnterProduct.objects.all()
    serialazer=EnterProductSerializer(enterproducts, many=True)
    return Response(serialazer.data)



#wishlist
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def listwishlist(request):
    product_id = request.data.get('product_id')
    user_id = request.data.get('user_id')  
    
    if product_id and user_id:
        try:
            like = models.Wishlist.objects.get(product_id=product_id, user_id=user_id)
            like.delete()
            return Response(status=status.HTTP_200_OK)
        except models.Wishlist.DoesNotExist:
            serializer = serializers.WishlistSer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Product ID and user ID are required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)
    




@api_view(['GET'])
def login(request):
    username=request.data.get('username')
    password=request.data.get('password')
    user=authenticate(username=username,password=password)
    if user:
        token,_ = Token.objects.get_or_create(user=user)
        print(token.key)
        data={
            'token':token.key
        }

    return Response(data)
    





from rest_framework import serializers
from main import models


#product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Product
        fields='__all__'



class ProductImageSerilalizer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductImage
        fields=['image']


# class ProductDetailSerializer(serializers.ModelSerializer):
#     images=serializers.ProductImageSerializer(many=True, read_only=True)
#     class Meta:
#         model=models.Product










#Categoriya
class CategorySerializer(serializers.ModelSerializer): #category list
    class Meta:
        model=models.Category
        fields='__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):#category detail
    class Meta:
        model=models.Product
        fields='__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductImage
        fields='__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductReview
        fields='__all__'


class CardSerializer(serializers.ModelSerializer):
    depth = 2
    class Meta:
        model=models.Card
        fields='__all__'


class CardProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CardProduct
        fields='__all__'


class EnterProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.EnterProduct
        fields='__all__'
        


class WishListSerializer(serializers.ModelSerializer):
    depth=2
    class Meta:
        model=models.WishList
        fields='__all__'


class   ReviewSer(serializers.ModelSerializer):
    depth = 2   
    class Meta:
        model = models.ProductReview
        fields = '__all__'
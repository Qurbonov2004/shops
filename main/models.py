from django.db import models
from django.contrib.auth.models import User
from functools import reduce
from django.db.models import Sum
from django.utils.text import slugify
from unidecode import unidecode
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super(Category, self).save(*args, **kwargs)



class Product(models.Model):
    name = models.CharField(max_length=255)
    slug=models.SlugField(blank=True)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.SmallIntegerField(
        choices=(
            (1,'Dollar'), 
            (2, 'So`m')
            )
    ) 
    discount_price = models.DecimalField(
        decimal_places=2, 
        max_digits=10, 
        blank=True, 
        null=True
        )
    baner_image = models.ImageField(upload_to='baner/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


    @property
    def review(self):
        reviews = ProductReview.objects.filter(product_id=self.id)
        result = reduce(lambda result, x: result +x.mark, reviews, 0)
        try: 
            result = round(result / reviews.count())

        except  ZeroDivisionError:
            result=0
        return result
    
    @property 
    def is_discount(self):
        return self.discount_price > 0
    
    @property 
    def is_active(self):
        return self.quantity > 0
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.slug=slugify(unidecode(self.name))
        super(Product,self).save(*args,**kwargs)



class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    slug=models.SlugField(blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
    
    def save(self,*args,**kwargs):
        self.slug=slugify(unidecode(self.product.name))
        super(ProductImage,self).save(*args,**kwargs)


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug=models.SlugField(blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def sava(self,*args,**kwargs):
        self.slug = slugify(unidecode(f"{self.user.username}-{self.product.name}"))
        super(WishList,self).save(*args,**kwargs)


class ProductReview(models.Model):
    slug=models.SlugField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mark = models.SmallIntegerField()

    def sava(self,*args,**kwargs):
        self.slug = slugify(unidecode(f"{self.user.username}-{self.product.name}"))
        super(ProductReview,self).save(*args,**kwargs)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug=models.SlugField(blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def quantity(self):
        return CardProduct.objects.filter(card=self).aggregate(Sum('quantity'))['quantity__sum'] 

    @property
    def total_price(self):
        result = 0
        for i in CardProduct.objects.filter(card_id=self.id):
            result +=(i.product.price)*i.quantity
        return result
    
    def sava(self,*args,**kwargs):
        self.slug=slugify(unidecode(self.user))
        super(Card,self).save(*args,**kwargs)


class CardProduct(models.Model):
    slug=models.SlugField(blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    
    @property
    def price(self):
        # print(self.product.is_discount)
        # if self.product.is_discount :
        #     result = self.product.discount_price * self.quantity
        # else:
        result = self.product.price * self.quantity
        return result
    
    def sava(self,*args,**kwargs):
        self.slug = slugify(unidecode(f"{self.quantity}-{self.product.name}"))
        super(CardProduct,self).save(*args,**kwargs)
    

    
class EnterProduct(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}"
    
    def save(self, *args, **kwargs):
        if self.product:
            self.product_name = self.product.name
            if self.pk:
                enter = EnterProduct.objects.get(pk=self.pk)
                product = enter.product
                product.quantity -= enter.quantity
                product.quantity += self.quantity
                product.save()
            else:
                self.product.quantity += self.quantity
                self.product.save()
        super(EnterProduct, self).save(*args, **kwargs)









    



    


    
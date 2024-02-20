from django.contrib import admin
from . import models

admin.site.register(models.Card)
admin.site.register(models.CardProduct)
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.ProductReview)
admin.site.register(models.WishList)
admin.site.register(models.EnterProduct)
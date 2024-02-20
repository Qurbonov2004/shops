from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.exceptions import FieldError
from . funcs import search_with_fields, pagenator_page,filter_product

import pandas as pd
from collections import defaultdict

from main.models import  Category, Product, ProductImage,EnterProduct,Card,CardProduct



#dashboard



def dashboard(request):
    category=Category.objects.all()
    product=Product.objects.all()

    context={
        'category':category,
        'product':product
    }

    return render(request,'dashboard/index.html',context)




def category_list(request):
    if request.method=='GET':
        categoriess=Category.objects.all()
        categoriess=pagenator_page(categoriess,2,request)
        return render(request,'dashboard/category/list.html',{'categoriess':categoriess})



def category_create(request):
    if request.method=='POST':
        Category.objects.create(
            name=request.POST['name']
        )
        return redirect('category_list')
    return render(request,'dashboard/category/create.html')


def category_update(request,id):
    category=Category.objects.get(id=id)
    if request.method=='POST':
        category.name = request.POST['name']
        category.save()
        return redirect('category_list')
    return render(request,'dashboard/category/update.html',{'category':category})



def category_delete(request,id):
    category=Category.objects.get(id=id)
    category.delete()

    return redirect('category_list')





def list_enter(request):
    if request.method == 'GET':
        result = search_with_fields(request)
        enters=EnterProduct.objects.all()
         

        context = {'enters': pagenator_page(enters,2,request)}
        return render(request, 'dashboard/enter/list.html', context)
def product(request):
    # 1st approach
    if request.method == 'GET':
        result = filter_product(request)
        products_all = Product.objects.all()
        products_filter = Product.objects.filter(**result) if result else None

        if products_filter:
            products = pagenator_page(products_filter, 1, request)
        else:
            products = pagenator_page(products_all, 1, request)




#2-yo'l
    
    # name = request.GET.get('name')
    # quantity = request.GET.get('quantity')
    # price=request.GET.get('price')
    # if name and quantity and price :
    #     products = Product.objects.filter(
    #         name=name,
    #         quantity=quantity,
    #         price=price  

    #     )
        
    # else:
    #     products = Product.objects.all()
    #     print(products)



#3-yo'l
    
    # name = request.GET.get('name')
    # quantity = request.GET.get('quantity')
    # price = request.GET.get('price')

    # # Create an empty Q object to build the dynamic filter
    # filter_conditions = Q()

    # if name:
    #     filter_conditions &= Q(name__icontains=name)

    # if quantity:
    #     filter_conditions &= Q(quantity=quantity)

    # if price:
    #     filter_conditions &= Q(price=price)

    # # Apply the dynamic filter
    # if filter_conditions:
    #     products = Product.objects.filter(filter_conditions)
    # else:
    #     products = Product.objects.all()

    return render(request, 'dashboard/product/list.html', {'products': products})






def product_create(request):
    categorys = Category.objects.all()
    context = {
        'categorys':categorys
    }
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        quantity = request.POST['quantity']
        price = request.POST['price']
        currency = request.POST['currency']
        baner_image = request.FILES['image']
        category_id = request.POST['category_id']
        images = request.FILES.getlist('images')
        product = Product.objects.create(
            name=name,
            description = description,
            quantity=quantity,
            price=price,
            currency=currency,
            baner_image=baner_image,
            category_id=category_id
        )
        for image in images:
            ProductImage.objects.create(
                image=image,
                product=product
            )


    return render(request, 'dashboard/product/create.html', context)


def product_update(request, id):
    product = Product.objects.get(id=id)
    old_banner_image = product.baner_image
    
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        quantity = request.POST.get('quantity', '')
        product.quantity = int(quantity) if quantity.isdigit() and quantity != '' else 0
        new_images = request.FILES.getlist('images')       
        if  request.POST['discount_price']:
            product.discount_price = request.POST['discount_price']

        for new_image in new_images:
            ProductImage.objects.create(
                image=new_image,
                product=product
            )
        old_images = ProductImage.objects.filter(product=product)
        for old_image in old_images:
            old_image.delete()
        if 'image' in request.FILES:
            product.baner_image = request.FILES['image']
        else:
            product.baner_image = old_banner_image

        product.category_id = request.POST['category_id']
        
        product.save()
        

        return redirect('product')
    
    category = Category.objects.all()

    context = {
        'product': product,
        'category': category
    }

    return render(request, 'dashboard/product/update.html', context)


def product_delete(request,id):
    product=Product.objects.get(id=id)
    product.delete()

    return redirect('product')




#entrerproduct
def list_enter(request):
    if request.method == 'GET':
        result = search_with_fields(request)
        enters=EnterProduct.objects.all()
         

        context = {'enters': pagenator_page(enters,2,request)}
        return render(request, 'dashboard/enter/list.html', context)





def create_enter(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        quantity = int(request.POST['quantity'])
        EnterProduct.objects.create(
            product_id=product_id,
            quantity=quantity
        )
        return redirect('list_enter')
    return render(request, 'dashboard/enter/create.html', {'products':Product.objects.all()})


def update_enter(request, id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        enter = EnterProduct.objects.get(id=id)
        enter.quantity = quantity
        enter.save()
    return redirect('list_enter')


def delete_enter(request, id):
    EnterProduct.objects.get(id=id).delete()

    return redirect('list_enter')












def write(request):
    products = Product.objects.all()
    data = {
        'Name': [product.name for product in products],
        'Price': [product.price for product in products],
        'Quantity': [product.quantity for product in products],
        'Price': [product.price for product in products],
        'P/B': [product.currency for product in products],
    }
    df = pd.DataFrame(data)
    excel_file_path = 'products.xlsx'
    df.to_excel(excel_file_path, sheet_name='Products', index=False)
    with open(excel_file_path, 'rb') as excel_data:
        content = excel_data.read()

    response = HttpResponse(content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'

    return response





def enter_write(request):
    enters = EnterProduct.objects.all()
    print(enters)

    data = {       
        'Maxsulot soni': [enter.quantity for enter in enters],
            'Maxsulot nomi': [enter.product.name if enter.product and enter.product.name else enter.product_name for enter in enters],
        'Maxsulot qo\'shilgan sana': [enter.created_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S') for enter in enters],
    }

    result = pd.DataFrame(data)
    path = 'enter.xlsx'
    result.to_excel(path, sheet_name="Enter", index=False)

    with open(path, 'rb') as excel_data:
        content = excel_data.read()

    response = HttpResponse(content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=enter.xlsx'
    
    # Qator uzunligi uchun
    response['Maxsulot qator uzunligi'] = f'{max(map(len, data.values())) * 10}px' if data else '0px'
    return response







def expenditure(request):
    cartproducts = CardProduct.objects.filter(card__is_active=False)
    
    dict1 = defaultdict(int)
    for cartproduct in cartproducts:
        dict1[cartproduct.product.name] += cartproduct.quantity
    result_list = [{'name': name, 'total_quantity': total_quantity, 'user': cartproduct.card.user} for name, total_quantity in dict1.items()]

    return render(request, 'dashboard/chiqim/list.html', {'result_list': result_list})


def expenditure_excel(request):
    carts = Card.objects.filter(is_active=False)
    cartproducts = CardProduct.objects.filter(card__in=carts)
    data = {
        "Number": [cartproduct.id for cartproduct in cartproducts],
        "Maxsulot nomi": [cartproduct.product.name for cartproduct in cartproducts],
        "Number": [cartproduct.quantity for cartproduct in cartproducts]
    }

    result = pd.DataFrame(data)
    path = 'chiqim.xlsx'  # Fayl nomini o'zgartirish
    result.to_excel(path, sheet_name='Chiqim', index=False)

    with open(path, 'rb') as chiqim:
        content = chiqim.read()

    response = HttpResponse(content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=chiqim.xlsx'  # Fayl nomini o'zgartirish

    return response






@csrf_exempt


def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel']:
        excel_file = request.FILES['excel']
        file = request.FILES['excel'].name

        with open(file, 'wb+') as destination:
            for chunk in excel_file.chunks():
                destination.write(chunk)

        excel_data = pd.read_excel(file)
        for index, row in excel_data.iterrows():
            quantity = row['Maxsulot soni']
            product_name = row['Maxsulot nomi']
            created_at = row['Maxsulot qo\'shilgan sana']
            enter_product = EnterProduct.objects.create(
                quantity=quantity,
                product_name=product_name,
                created_at=created_at
            )

        return redirect('list_enter')
    else:
        return redirect('upload_excel')
    






# def list_enter(request):
#     enters = EnterProduct.objects.all()

#     # Fetching data from the expenditure view
#     cartproducts = CardProduct.objects.filter(card__is_active=False)
#     dict1 = defaultdict(int)
#     for cartproduct in cartproducts:
#         dict1[cartproduct.product.name] += cartproduct.quantity
#     result_list = [{'name': name, 'total_quantity': total_quantity} for name, total_quantity in dict1.items()]

#     # Combining data into a single list
#     combined_list = [{'type': 'enter', 'data': enter} for enter in enters] + [{'type': 'expenditure', 'data': result} for result in result_list]

#     return render(request, 'dashboard/enter/list.html', {'combined_list': combined_list})



        










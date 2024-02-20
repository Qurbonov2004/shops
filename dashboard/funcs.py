from django.core.paginator import (Paginator, 
                                   EmptyPage, 
                                   PageNotAnInteger)


def search_with_fields(request):
    result = {}
    for key, value in request.GET.items():
        if value:
            if key == 'name':
                key = 'product__name__icontains'
            elif key == 'created_at_start':
                key = 'created_at__gte'
            elif key == 'created_at_end':
                key = 'created_at__lte'
            
            result[key] = value

    return result


def filter_product(request):
    result={}
    for key,value in request.GET.items():
        if value:
            if key=='name':
                key='name__icontains'
            elif key=='quantity_min':
                key='quantity__gte'
            elif key=='quantity_max':
                key='quantity__lte'
            elif key=='price_min':
                key='price__gte'
            elif key=='price_max':
                key='price__lte'
            result[key]=value

        if 'page' in request.GET:
            del result['page']
    return result


def pagenator_page(list, num, request):
    paginator = Paginator(list, num)
    pages = request.GET.get('page')
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list
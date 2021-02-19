from django.shortcuts import render

from .models import *

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib import messages

from django.http import JsonResponse
import json
import datetime

from .utils import cookieCart, cartData, guestOrder

# Create your views here.
def store(request):
    data = cartData(request)
    order = data['order']
    cartItems = data['cartItems']
    
   
    '''
    products = Product.objects.all()


    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {'page_obj': page_obj, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)
    '''
    queryset_list = Product.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(name__icontains=query)

    paginator = Paginator(queryset_list, 6)

    page_number = request.GET.get('page')
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "products": queryset, 'cartItems': cartItems, 'query':query}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)



def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else:
        print('User is not logged in')   
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )


    return JsonResponse('Payment subbmitted..', safe=False)


def get_products_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        products = Product.objects.filter(name__icontains=q).distinct()

        queryset.extend(products)
    
    return list(set(queryset))
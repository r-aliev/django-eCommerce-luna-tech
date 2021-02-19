import json
from .models import *

def cookieCart(request):

    #Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    #print('CART:',cart)

    #Create empty cart for now for non-logged in user
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:

        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id = i);
            
            total = cart[i]['quantity'] * product.price
            
            order['get_cart_total'] +=  total
            order['get_cart_items'] += cart[i]['quantity']

            if product.digital == False:
                order['shipping'] = True;

            #orderitems part
            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            };
            items.append(item);
        except:
            pass

    return {'items': items, 'order': order, 'cartItems': cartItems}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
    return {'items': items, 'order': order, 'cartItems': cartItems}


def guestOrder(request, data):
    #print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    
    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product = product,
            quantity = item['quantity'],
            order = order
        )

    return customer, order
    

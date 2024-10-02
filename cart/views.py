from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# from activities.models import Activities

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

#Single Item add
def add_to_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, user=current_user)
            print(cart_items)
            item = CartItem.objects.get(product=product, user=current_user)
            item.quantity += 1
            item.save()
            
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
                user = current_user
            )
            cart_item.save()
        return redirect('cart')
    else:
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
        
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity  += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                )
            cart.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart/cart.html', context)



@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart/checkout.html', context)



""" from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, user=current_user)
            print(cart_items)
            item = CartItem.objects.get(product=product, user=current_user)
            item.quantity += 1
            item.save()
            
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
                user = current_user
            )
            cart_item.save()
        return redirect('cart')
    else:
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
        
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity  += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                )
            cart.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart/cart.html', context) """






""" from django.shortcuts import render,redirect
from store.models import Product
from .models import Cart,CartItem
from django.db.models import Q 
# Create your views here.

def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

# def cart(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         pass
#     session_id = request.session.session_key # session  id ke niye aslam 
#     cartid =Cart.objects.get(cart_id=session_id) # model k ber kore niye anlam 
#     #print(type(cartid))
#     #print(type(session_id))
#     cart_id=Cart.objects.filter(cart_id=session_id).exists() # ei session id wala kono card database e ache ki na 
#     # print(session_id)
#     cart_items=None
#     tax=0
#     total=0
#     grand_total=0
#     if cart_id:
#         #pass
#         cart_items=CartItem.objects.filter(cart=cartid)
#         # print(cart_item)
#         for item in cart_items:
#             total+=item.product.price+item.quantity
#     tax=(2*total)/100 # 2 % vat
#     grand_total=total+tax
#     return render(request,'cart/cart.html',{'cart_items':cart_items,'tax':tax,'total':total,'grand_total':grand_total})


# phitron theke dewa
# def Cart(request):
#     cart = get_create_session(request)
#     cart_items = CartItem.objects.filter(cart=cart, is_active=True)

#     total = sum(item.product.price * item.quantity for item in cart_items)
#     tax = (2 * total) / 100
#     grand_total = total + tax

#     return render(request, 'cart/cart.html', {'cart_items': cart_items, 'tax': tax, 'total': total, 'grand_total': grand_total})




def cart(request):
    cart_items=None
    tax=0
    total=0
    grand_total=0
    if request.user.is_authenticated:
        cart_items=CartItem.objects.filter(user=request.user)
        # print(cart_item)
        for item in cart_items:
            total+=item.product.price*item.quantity
    else:
        session_id = get_create_session(request) # session  id ke niye aslam 
        cartid =Cart.objects.get(cart_id=session_id) # model k ber kore niye anlam 
        #print(type(cartid))
        #print(type(session_id))
        cart_id=Cart.objects.filter(cart_id=session_id).exists() # ei session id wala kono card database e ache ki na 
        # print(session_id)
        if cart_id:
            #pass
            cart_items=CartItem.objects.filter(cart=cartid)
            # print(cart_item)
            for item in cart_items:
                total+=item.product.price * item.quantity
    tax=(2*total)/100 # 2 % vat
    grand_total=total+tax
    return render(request,'cart/cart.html',{'cart_items':cart_items,'tax':tax,'total':total,'grand_total':grand_total})



# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     session_id = get_create_session(request) # session id ke ber kore anlam

#     if request.user.is_authenticated: # logged in
#         cart_item = CartItem.objects.filter(product=product, user = request.user).exists()
#         if cart_item:
#             item = CartItem.objects.get(product=product)
#             item.quantity += 1
#             item.save()
#         else :
#             cartid = Cart.objects.get(cart_id = session_id)
#             item = CartItem.objects.create(
#                 cart = cartid,
#                 product = product,
#                 quantity = 1,
#                 user = request.user
#             )
#             item.save()
#     else:
#         # print(session_id)
#         cart_id = Cart.objects.filter(cart_id = session_id).exists() # session id wala kono cart id ache kina check kortechi,Thakle True dibe naile False
#         if cart_id: # jodi cart id thake 
#             # cartid = Cart.objects.get(cart_id = session_id)
#             cart_item = CartItem.objects.filter(product=product, cart = cartid).exists()
#             if cart_item:
#                 item = CartItem.objects.get(product=product, cart= cartid)
#                 item.quantity += 1
#                 item.save()
#             else :
#                 cartid = Cart.objects.get(cart_id = session_id)
#                 print("adfasdf ", cartid, session_id)
#                 item = CartItem.objects.create(
#                     cart = cartid,
#                     product = product,
#                     quantity = 1
#                 )
#                 item.save()
#         else:
#             cart = Cart.objects.create(
#             cart_id = session_id
#             )
#             cart.save()
    
#     return redirect('cart')


# phitron theke dewa 
# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     session_id = get_create_session(request)

#     if request.user.is_authenticated:
#         # Check if the user already has a cart, if not, create one
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
#         if not item_created:
#             cart_item.quantity += 1
#             cart_item.save()
#     else:
#         # Check if the session cart exists, if not, create one
#         cart, created = Cart.objects.get_or_create(cart_id=session_id)
#         cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
#         if not item_created:
#             cart_item.quantity += 1
#             cart_item.save()

#     return redirect('cart')





# eta amar nijer kora 
def add_to_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    # print('add to cart',product)
    # session_id=request.session.session_key
    session_id=get_create_session(request) # session id ber kore anlam 
    # print(session_id)
    if request.user.is_authenticated: # ljodi logged in user hoi
        cart_item=CartItem.objects.filter(product=product, user=request.user).exists()
        if cart_item:
            # print('ache')
            item=CartItem.objects.get(product=product)
            item.quantity += 1
            item.save()
        else:
            # print('nie')
            cartid=Cart.objects.get(cart_id=session_id)
            item=CartItem.objects.create(
                cart=cartid,
                product=product,
                quantity=1,
                user=request.user
            )
            item.save()
    else:
        # print('nie')
        cart_id=Cart.objects.filter(cart_id=session_id).exists() # session id wala kono cart ache kina
        # seta check kortechi .. thakle true dibe naile false 
        if cart_id: # jodi cart id thake 
            #cart ache 
            cartid = Cart.objects.get(cart_id = session_id)
            cart_item=CartItem.objects.filter(product=product,cart=cartid).exists()
            if cart_item:
                # print('ache')
                item=CartItem.objects.get(product=product,cart=cartid)
                item.quantity+=1
                item.save()
            else:
                # print('nie')
                cartid=Cart.objects.get(cart_id=session_id)
                item=CartItem.objects.create(
                    cart=cartid,
                    product=product,
                    quantity=1,
                )
                item.save()
        else:
            cart=Cart.objects.create(
            cart_id=session_id
            )
            cart.save()
    return redirect('cart')


def remove_cart_item(request,product_id):
    # print(product_id)
    product=Product.objects.get(id=product_id)
    session_id=request.session.session_key
    cartid=Cart.objects.get(cart_id=session_id) #cart id search korlam
    cart_item=CartItem.objects.get(cart=cartid,product=product)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    print(cart_item)
    return redirect('cart')

def remove_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    session_id=request.session.session_key
    cartid=Cart.objects.get(cart_id=session_id) #cart id search korlam
    cart_item=CartItem.objects.get(cart=cartid,product=product)
    # cart item filter korbo cartid ar product id er upor filter  korbo 
    cart_item.delete()
    return redirect('cart')



 """
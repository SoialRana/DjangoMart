from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from .forms import OrderForm
from .ssl import sslcommerz_payment_gateway
from .models import Payment, OrderProduct, Order
from store.models import Product
# Create your views here.
from .ssl import sslcommerz_payment_gateway
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch') # here disable the csrf
def success_view(request):
    data = request.POST # we try to print the data of success URL
    print('data -------', data)
    user_id = int(data['value_b'])  # Retrieve the stored user ID as an integer
    user = User.objects.get(pk=user_id)
    payment = Payment(
        user = user,
        payment_id =data['tran_id'],
        payment_method = data['card_issuer'],
        amount_paid = int(data['store_amount'][0]),
        status =data['status'], # we take track_id,card_issuer,store amount,status from data and save it 
    )
    payment.save()
    
    # working with order model
    order = Order.objects.get(user=user, is_ordered=False, order_number=data['value_a'])
    order.payment = payment
    order.is_ordered = True
    order.save()
    cart_items = CartItem.objects.filter(user = user)
    
    for item in cart_items:
        orderproduct = OrderProduct()
        product = Product.objects.get(id=item.product.id)
        orderproduct.order = order # As order is a model so we only pass a object
        orderproduct.payment = payment
        orderproduct.user = user
        orderproduct.product = product
        orderproduct.quantity = item.quantity
        orderproduct.ordered = True
        orderproduct.save()

        # Reduce the quantity of the sold products
        
        product.stock -= item.quantity # As order complete so we reduce the quantity from stock
        product.save() 

    # Clear cart
    CartItem.objects.filter(user=user).delete()
    return redirect('cart')
    



def order_complete(request):
    return render(request, 'orders/order_complete.html')

def place_order(request):
    print(request.POST)
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    # 1 --- 100
    # 5 --- 100*5
    cart_items = CartItem.objects.filter(user = request.user)
    
    if cart_items.count() < 1:
        return redirect('store') # If we don't cart any item then we don't pay for this 
    
    for item in cart_items:
        total += item.product.price * item.quantity
    print(cart_items)  
    tax = (2*total)/100 # 2 % vat
    grand_total = total + tax
    if request.method == 'POST':
        form = OrderForm(request.POST) # If request method is POST then we save the data from form
        if form.is_valid():
            # As first/last name we received from form but others data as ip/tax/payment we can't receive from form so we take it 
            form.instance.user = request.user
            form.instance.order_total = grand_total
            form.instance.tax = tax
            form.instance.ip = request.META.get('REMOTE_ADDR')
            form.instance.payment = 2
            saved_instance = form.save()  # Save the form data to the database
            form.instance.order_number = saved_instance.id # First we save the form then we get order number. We save the first form to get the id and we save next time for all save
            
            form.save()
            print('form print', form)
            return redirect(sslcommerz_payment_gateway(request,  saved_instance.id, str(request.user.id), grand_total))

    return render(request, 'orders/place-order.html',{'cart_items' : cart_items, 'tax' : tax,'total' : total, 'grand_total' : grand_total})
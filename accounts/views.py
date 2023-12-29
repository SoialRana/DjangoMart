# Updated Code
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm,UserForm,UserProfileForm
from .models import Account,UserProfile
from orders.models import Order, OrderProduct
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from cart.views import _cart_id
from cart.models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist


def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            user=Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number=phone_number
            user.save()
            
            # user ACTIVATION
            current_site=get_current_site(request)
            mail_subject='Please activate your account'
            message=render_to_string('accounts/account_verification_email.html', {'user':user, 'domain':current_site, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token' : default_token_generator.make_token(user),})
            to_email=email
            send_email=EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form=RegistrationForm()
    context={
        'form': form,
    }
    return render(request, 'accounts/register.html', context)
    
    
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists= CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user=user
                        item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user=None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active= True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('register')
    


@login_required(login_url='login')
def dashboard(request):
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id, id_ordered=True)
    orders_count=orders.count()
    
    try:
        userprofile=UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        userprofile=UserProfile.objects.create(user=request.user)
    context={
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)



@login_required(login_url='login')
def my_orders(request):
    orders=Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context={
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile=get_object_or_404(UserProfile, user=request.user)
    if request.method=='POST':
        user_form=UserForm(request.POST, request.FILES, instance=userprofile)
        profile_form=UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
        else:
            user_form=UserForm(instance=request.user)
            profile_form=UserProfileForm(instance=userprofile)
        context={
            'user_form': user_form,
            'profile_form': profile_form,
            'userprofile': userprofile
        }
        return render(request, 'accounts/edit_profile.html', context)



 
""" from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from cart.models import Cart, CartItem
from .forms import RegistrationForm

def _cart_id(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart_id = request.session.session_key
        request.session['cart_id'] = cart_id
    return cart_id

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cart')
    return render(request, 'accounts/register.html', {'form': form})

def profile(request):
    return render(request, 'accounts/dashboard.html')

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=user_name, password=password)

        if user:
            cart_id = _cart_id(request)
            cart, created = Cart.objects.get_or_create(cart_id=cart_id)

            # Update the user for cart items
            if not created:
                cart_item = CartItem.objects.filter(cart=cart)
                for item in cart_item:
                    item.user = user
                    item.save()

            login(request, user)
            return redirect('profile')
    return render(request, 'accounts/signin.html')

def user_logout(request):
    logout(request)
    return redirect('login') """



""" from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib.auth import login,logout,authenticate
from cart.models import Cart,CartItem
# Create your views here.

# def get_create_session(request):
#     if not request.session.session_key:
#         request.session.create()
#     return request.session.session_key

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def register(request):
    form=RegistrationForm()
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            # print(form)
            return redirect('cart')
    return render(request,'accounts/register.html',{'form':form})


def profile(request):
    return render(request,'accounts/dashboard.html')

def user_login(request):
    if request.method=='POST':
        user_name=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=user_name,password=password)
        # print(user)
        #ekhono login hoi nie 
        # session_key=get_create_session(request)
        # cart=Cart.objects.get(cart_id=session_key)
        cart=Cart.objects.get(cart_id=_cart_id)
        is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(cart=cart)
            for item in cart_item:
                item.user=user
                item.save()
                
        login(request,user)
        #login hoye geche 
        return redirect('profile')
        # print(request.POST)
    return render(request,'accounts/signin.html')

def user_logout(request):
    logout(request)
    return redirect('login') """
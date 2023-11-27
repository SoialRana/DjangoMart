from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
from django.core.paginator import Paginator

# Create your views here.
def store(request,category_slug=None):
    # products=Product.objects.all() # is_available=True diye kebol jei product gulo thakbe sei product gullo dekhabe 
    # for item in products:
    #     print(item.product_name,item.price,item.is_available)
    # products=Product.objects.filter(is_available=True) # jokhon is available use korbo tokhon filter use korbo 
    # products=None
    # category=None
    # all tokhon use kortechi jokhon sobgulo product use korte cacchi ...filter tokhon use korbo jokhon specific kisu product dekhte chaibo 
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)# jodi amra userer dewa nam onujayi search korte chay 
        products=Product.objects.filter(is_available=True,category=category) # category wise products
        page=request.GET.get('page')
        paginator=Paginator(products,1) # Paginator(products, per page koto gulo product dekhte chay)
        paged_product=paginator.get_page(page)
    else:
        products=Product.objects.filter(is_available=True) # all products
        page=request.GET.get('page')
        paginator=Paginator(products,2) # Paginator(products, per page koto gulo product dekhte chay)
        paged_product=paginator.get_page(page)
        for i in paged_product:
            print(i)
        print(paged_product.has_next(),paged_product.has_previous(),paged_product.next_page_number,paged_product.previous_page_number)
    
    
    # print(page_product)
    # print(category)
    # products=Product.objects.filter(is_available=True)
    # for item in products:
    #     print(item.product_name,item.price,item.is_available)
    # return render(request,'store/store.html',{'products':products})
    
    
    categories=Category.objects.all()
    # context={'products':products,'categories':categories}
    context={'products':paged_product,'categories':categories}
    # amra jodi vairious data pass kori then evabeo context er moddheo data pass kora jai 
    return render(request,'store/store.html',context)
    # amra jodi frontend er moddhe dekhte chay taile amader context er moddhe pass kore dite hobe 

def product_detail(request,category_slug,product_slug):
    single_product=Product.objects.get(slug=product_slug,category__slug=category_slug)
    # jodi amader kase multiple product thake tahole sekhan theke kono product/object access korte get function use korbo 
    
    return render(request,'store/product_detail.html',{'product': single_product})


# def product_detail(request):
#     return render(request,'store/product_detail.html')


# ami currently achi product model e kintu ki kore category model er slug k access korte parbo 
# category slug k access korte chaile category__slug diye access korte hobe jehetu foreign key ..
# amra first e category model e gechi jehetu eta different model tie setake access korar jonno double __ use korchi 
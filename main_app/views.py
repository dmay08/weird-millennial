from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, LineItemForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from .models import Product, Order, LineItem
from django.db.models import Sum, F, FloatField
from django.contrib.auth.decorators import login_required

# Create your views here. 
class ProductList(ListView):
    model = Product
    # inside of template will be a 'product_list'
    template_name = 'products/product_list.html'

# def PRODUCT_DETAIL = IMPORTANT FOR ASSESSMENT 2 (and "def add_to_cart")
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    line_item_form = LineItemForm()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'form': line_item_form # in "product_detail.html" > use "form"!!
    })

@login_required
def add_to_cart(request, product_id): # product_id = URLS.PY <int:___>
    # get order
    order = Order.cart(request.user)
    line_item, created = LineItem.objects.get_or_create(order=order, product_id=product_id)
    if not created:
        line_item.quantity += int(request.POST['quantity'])
        line_item.save()
    return redirect('/cart')

def checkout(request):
    cart = Order.cart(request.user)
    cart.paid = True
    cart.save()
    return render(request, 'checkout.html')

def cart_detail(request):
    cart = Order.cart(request.user)
    result = LineItem.objects.filter(order=cart).aggregate(total=Sum(F('quantity') * F('product__price'), output_field=FloatField())) # the order here is 'cart' (line above) (& 'order' is a field in "LineItem" model)
        # 'filter' = grabs line items of ONLY this 'Order' (vs. 'all' would grab EVERY lineitem every made)
    return render(request, 'cart.html', {
        'cart': cart, # 'cart' = key name (i choose name here) ; this is a PYTHON dictionary
        'total': result['total'] # result comes from above (in method) and ['total'] comes from blue total (same line above)
    }) 

# increase quantity button (cart)
def increase_qty(request, line_item_id): # line_item_id = needs to match the (already written) url in URLS.PY <int:___>
    item = LineItem.objects.get(id=line_item_id) # have to go through objects to query (search)
        #'get' allows me to get a single object (row) out of the database
        # we want to 'query' like we do in JS to find the object(?) then name it to alter it in the function
    item.quantity += 1 # quantity is a 'field' in LineItem model - so I can access it here
    item.save()
    return redirect('/cart')

def decrease_qty(request, line_item_id): # 2 parameters for the function; like function (a, b)
    item = LineItem.objects.get(id=line_item_id) # join table doing its job here too
    if item.quantity <= 1:
        item.delete()
    else:
        item.quantity -= 1 # aka LineItem.product.quantity (b/c Product model has 'quantity' & LineItem has 'Product's' foreign key)
        item.save()
    return redirect('/cart')

def index(request):
    products = Product.objects.all() # this allows me to view product list on index.html
    return render(request, 'index.html', { 'products': products })

def about(request):
    return render(request, 'about.html')

def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
                    return HttpResponseRedirect('/')
            else:
                print("The username and/or password is incorrect.")
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else: # added this to get rid of error page when SIGNUP info doesn't meet requirements
            return redirect('/signup/')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

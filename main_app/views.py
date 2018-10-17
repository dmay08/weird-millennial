from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, LineItemForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from .models import Product, Order, LineItem

# Create your views here. 

# def PRODUCT_DETAIL = IMPORTANT FOR ASSESSMENT 2 (and "def add_to_cart")
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    line_item_form = LineItemForm()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'form': line_item_form # in "product_detail.html" > use "form"!!
    })
    
class ProductList(ListView):
    model = Product
    # inside of template will be a 'product_list'
    template_name = 'products/product_list.html'

def add_to_cart(request, product_id): # product_id = URLS.PY <___>
    # get order
    order = Order.cart(request.user)
    
    line_item, created = LineItem.objects.get_or_create(order=order, product_id=product_id)
    print(line_item.size)
    if not created:
        line_item.quantity += int(request.POST['quantity'])
        line_item.size = request.POST['size']
        line_item.save()
    return redirect('/cart')

def cart_detail(request):
    cart = Order.cart(request.user)
    return render(request, 'cart.html', {'cart': cart})

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

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from .models import Product, Order

# Create your views here.
class ProductDetail(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

class ProductList(ListView):
    model = Product
    # inside of template will be a 'product_list'
    template_name = 'products/product_list.html'

#not sure about this one
def add_to_cart(request, product_id): # product_id = URLS.PY <___>
    # code for adding to cart
    return redirect('/cart')

def cart_detail(request):
    cart = Order.cart(request.user)
    return render(request, 'cart.html', {'cart': cart})

def index(request):
    return render(request, 'index.html')

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

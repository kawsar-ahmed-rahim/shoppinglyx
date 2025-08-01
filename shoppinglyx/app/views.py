from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


class ProductView(View):
 def get(self, request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'laptops': laptops})


class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/productdetail.html', {'product': product})
 

def add_to_cart(request):
  user = request.user
  product_id = request.GET.get('prod_id')
  product = Product.objects.get(id=product_id)
  Cart(user=user, product=product).save()
  return redirect('/cart')

def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    totalamount = amount + shipping_amount
   return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount' : totalamount, 'amount': amount})
  else:
   return render(request, 'app/emptycart.html')
 

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount

  data = {
      'quantity': c.quantity,
      'amount':amount,
      'totalamount': amount + shipping_amount
     }
  return JsonResponse(data)
 
def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount
    

  data = {
      'quantity': c.quantity,
      'amount':amount,
      'totalamount':amount + shipping_amount
     }
  return JsonResponse(data)
 
def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount

  data = {
      'amount':amount,
      'totalamount':amount + shipping_amount
     }
  return JsonResponse(data)


def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0 
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount
  totalamount = amount + shipping_amount
 return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount})

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
  add = Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})



def orders(request):
 return render(request, 'app/orders.html')

def mobile(request, data=None):
  if data == None:
   mobiles = Product.objects.filter(category='M')
  elif data == 'samsung' or data == 'MI' or data == 'IPhone':
   mobiles = Product.objects.filter(category="M").filter(brand=data)
  elif data == 'below':
   mobiles = Product.objects.filter(category="M").filter(discounted_price__lt=40000)
  elif data == 'above':
   mobiles = Product.objects.filter(category="M").filter(discounted_price__gt=40000)
  return render(request, 'app/mobile.html', {'mobiles': mobiles})


def laptop(request, data=None):
  if data == None:
   laptops = Product.objects.filter(category='L')
  elif data == 'HP' or data == 'Acer':
   laptops = Product.objects.filter(category="L").filter(brand=data)
  elif data == 'below':
   laptops = Product.objects.filter(category="L").filter(discounted_price__lt=75000)
  elif data == 'above':
   laptops = Product.objects.filter(category="L").filter(discounted_price__gt=75000)
  return render(request, 'app/laptop.html', {'laptops': laptops})


def top_wear(request, data=None):
  if data == None:
   top_wears = Product.objects.filter(category='TW')
  elif data == 'HTR' or data == 'Lee' or data == 'BPT' or data == 'Heavy-Metal':
   top_wears = Product.objects.filter(category="TW").filter(brand=data)
  elif data == 'below':
   top_wears = Product.objects.filter(category="TW").filter(discounted_price__lt=1100)
  elif data == 'above':
   top_wears = Product.objects.filter(category="TW").filter(discounted_price__gt=1100)
  return render(request, 'app/top-wear.html', {'top_wears': top_wears})


def bottom_wear(request, data=None):
  if data == None:
   bottom_wears = Product.objects.filter(category='BW')
  elif data == 'STPT' or data == 'Lee' or data == 'BPT' or data == 'avocado':
   bottom_wears = Product.objects.filter(category="BW").filter(brand=data)
  elif data == 'below':
   bottom_wears = Product.objects.filter(category="BW").filter(discounted_price__lt=550)
  elif data == 'above':
   bottom_wears = Product.objects.filter(category="BW").filter(discounted_price__gt=550)
  return render(request, 'app/bottom-wear.html', {'bottom_wears': bottom_wears})


class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form': form})
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations! Registered successfully.')
   form.save()
  return render(request, 'app/customerregistration.html', {'form': form})
 

class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
 
 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr, name=name, locality=locality, city=city, zipcode=zipcode)
   reg.save()
   messages.success(request, 'Congratulations!! Profile Updated Successfully')
  return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import Product
from django.contrib.auth import login as auth_login
from .cart import Cart
from . forms import CheckoutForm, ContactForm
from django.core.mail import send_mail
from .models import Order, OrderItem
# Create your views here.

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to the homepage or any other page
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')  # Redirect back to login on failure
    return render(request, 'login.html')  

def cart(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart')
#checkout view

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Save the form data to create an Order instance
            order = form.save()

            # Redirect to the order confirmation page, passing the order ID
            return redirect('order_confirmation', order_id=order.id)
    else:
        # If not a POST request, display an empty form
        form = CheckoutForm()

    # Render the checkout page with the form
    return render(request, 'checkout.html', {'form': form})
    
#order confirmation view
from .models import Order, OrderItem

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    total_cost = order.get_total_cost()  # Calculated in your Order model
    
    print(f"Order ID: {order_id}")
    print(f"Order Items: {order_items}")
    print(f"Total Cost: {total_cost}")
    
    return render(request, 'order_confirmation.html', {
        'order': order,
        'order_items': order_items,
        'total_cost': total_cost,
    })

    
def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Send the email
            send_mail(
                subject=f'Contact Form Submission from {name}',
                message=message,
                from_email=email,
                recipient_list=['suppor12@gmail.com'],  # Replace with your email
            )
            
            # Redirect after successful submission
            return redirect('contact_success')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})


        
            

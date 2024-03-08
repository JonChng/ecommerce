from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Item, Cart, OrderItem, Order
from django.contrib import messages
from .forms import UpdateQuantityForm, CheckoutForm
from django.contrib.auth import login, authenticate, forms

# Create your views here.

def signup(request):
    form = forms.UserCreationForm()

    if request.method == 'POST':

        form = forms.UserCreationForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('/') 
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = forms.AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request)
                messages.success(request, f'Welcome {username}! You are now logged in.')
                return redirect('/') 
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = forms.AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def item_catalog(request):
    items = Item.objects.all()
    return render(request, 'item_catalog.html', {'items': items})

def add_to_cart(request, item_id):
    # Assuming a simple user ID for now
    user_id = 1
    item = Item.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity', 1))  # Default quantity is 1
    cart_item, created = Cart.objects.get_or_create(user_id=user_id, item=item)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
        cart_item.unit_price = item.price
        cart_item.name = item.name
    
        print(f"Cart Item: {cart_item}, Quantity: {cart_item.quantity}, Price: {cart_item.unit_price}")

    cart_item.save()
    
    return redirect("/")

def update_cart(request):
    if request.method == 'POST':
        # Retrieve the form data
        form_data = request.POST.copy()
        
        # Get the cart items for the current user
        cart_items = Cart.objects.filter(user_id=request.user.id)
        
        # Loop through each cart item and update its quantity
        for item in cart_items:
            quantity_key = f'quantity_{item.id}'
            if quantity_key in form_data:
                new_quantity = form_data.get(quantity_key)
                if new_quantity:
                    item.quantity = new_quantity
                    item.save()
        
        return redirect('view_cart')
    else:
        return redirect('view_cart')

def view_cart(request):
    # Get the cart items for the current user
    cart_items = Cart.objects.filter(user_id=request.user.id)
    final_price = 0
    for item in cart_items:
        item.total_price = item.unit_price * item.quantity
        final_price += item.total_price
    
    context = {
        'cart_items': cart_items,
        'final_price': final_price,
    }
    
    return render(request, 'cart.html', context)

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create a new order
            order = Order(user=request.user, total_amount=0) 
            order.save()

            cart_items = Cart.objects.filter(user_id=request.user.id)
            total_amount = 0
            for item in cart_items:
                order_item = OrderItem(order=order, item=item.item, quantity=item.quantity, item_price=item.unit_price)
                order_item.save()
                total_amount += item.unit_price * item.quantity

           
            order.total_amount = total_amount
            order.save()
            print(order.items)

            cart_items.delete()
            

            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    
    return render(request, 'order_confirmation.html', {'order': order})
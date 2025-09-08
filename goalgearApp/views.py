from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .utils import user_login_required
import uuid
from .models import CustomUser,Product,Category,ProductImage,Cart,Order,OrderItem,PaymentMethod,OrderPayment,Contact,Address


def signup_fun(request):
    if request.method == "POST":
        custom_obj=CustomUser()
        custom_obj.username=request.POST.get("username")
        custom_obj.email=request.POST.get("email")
        custom_obj.phone_number=request.POST.get("phone")
        custom_obj.password=request.POST.get("password")
        custom_obj.save()
        return redirect("/")
    return render(request,"signup.html")


def login_fun(request):
    if request.method=="POST":
        name=request.POST.get("username")
        password=request.POST.get("password")
        data=CustomUser.objects.filter(username=name,password=password)
        
        if data:
            request.session['user']=name
            return redirect("/")
    return render(request,"login.html")

def logout_fun(request):
    if 'user' in request.session:
        # Clear the session
        request.session.flush()
        # Alternative: del request.session['user']
    return redirect('/')


def home(request):
    # Get the latest 8 products and categories for all users
    new_arrivals = Product.objects.order_by('-created_at')[:8]
    categories = Category.objects.all()
    
    # Check if user is logged in to display user-specific data
    if 'user' in request.session:
        username = request.session['user']  
        # if request.method == "POST":
        #     search=request.POST.get("search")
        #     data=Product.objects.filter(name=search)
        try:
            user_data = CustomUser.objects.get(username=username)
            return render(request, "home.html", {
                "data1": user_data,
                "new_arrivals": new_arrivals,
                "categories": categories,
                "logged_in": True,
                # "search":data
            })
        except CustomUser.DoesNotExist:
            pass
    
    # For non-logged-in users
    return render(request, "home.html", {"new_arrivals": new_arrivals,"categories": categories,"logged_in": False})
    


def product_fun(request):
    products=Product.objects.all()
    return render(request, "products.html", {"products": products})



def product_view(request, product_id):
    product = Product.objects.get(id=product_id)
    images = ProductImage.objects.filter(product=product)
    return render(request, "product_view.html", {"product": product,"images": images})


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    context = {'products': products,'category': category,}
    return render(request, 'products.html', context)


@user_login_required
def add_to_cart(request, product_id):
    if 'user' not in request.session:
        return redirect("/Login")

    user = CustomUser.objects.get(username=request.session['user'])
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{product.name} added to cart!")
    return redirect("/bag")



@user_login_required
def bag(request):
    if 'user' not in request.session:
        return redirect("/Login")

    user = CustomUser.objects.get(username=request.session['user'])
    cart_items = Cart.objects.filter(user=user)

    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    total = sum(item.total_price for item in cart_items)
    return render(request, "bag.html", {"cart_items": cart_items,"total": total})


@user_login_required
@csrf_exempt
def update_cart_quantity(request, item_id):
    if 'user' not in request.session:
        return redirect("/Login")

    cart_item = get_object_or_404(Cart, id=item_id)
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()

    return redirect('/bag/')



@user_login_required
def remove_from_cart(request, item_id):
    if 'user' not in request.session:
        return redirect("/Login")
    cart_item = get_object_or_404(Cart, id=item_id)
    cart_item.delete()
    return redirect('/bag/')


def About_fun(request):
    return render(request,"about.html")


def Contact_fun(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            Contact.objects.create(name=name, email=email, message=message)
            return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')


@user_login_required
def add_address(request):
    if 'user' not in request.session:
        return redirect("/Login")

    user = CustomUser.objects.get(username=request.session['user'])

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")
        address_line = request.POST.get("address_line")
        city = request.POST.get("city")
        state = request.POST.get("state")

        address = Address.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            pincode=pincode,
            address_line=address_line,
            city=city,
            state=state
        )

        # Redirect to place_order view with address id
        return redirect(f'/place_order/{address.id}/')

    return render(request, "add_address.html")


@user_login_required
def place_order(request, address_id):
    if 'user' not in request.session:
        return redirect("/Login")

    user = CustomUser.objects.get(username=request.session['user'])
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('/bag')  # if cart is empty

    total = sum(item.product.price * item.quantity for item in cart_items)

    # Create Order
    order = Order.objects.create(
        user=user,
        total_amount=total,
        status='Pending'
    )

    # Create OrderItems from cart
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    # Optional: clear cart
    cart_items.delete()

    # return render(request, 'order_success.html', {'order': order})
    return redirect(f'/pay/{order.id}/')




@user_login_required
def order_status_view(request):
    if 'user' not in request.session:
        return redirect("/Login")

    user = CustomUser.objects.get(username=request.session['user'])
    orders = Order.objects.filter(user=user).order_by('-created_at')

    order_data = []
    for order in orders:
        items = OrderItem.objects.filter(order=order)
        order_data.append({
            'order': order,
            'items': items,
        })

    return render(request, "order_status.html", {"order_data": order_data})





@user_login_required
def demo_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    payment_methods = PaymentMethod.objects.all()

    if request.method == "POST":
        payment_method_id = request.POST.get("payment_method")
        selected_method = get_object_or_404(PaymentMethod, id=payment_method_id)

        # Create dummy payment
        payment = OrderPayment.objects.create(
            order=order,
            payment_method=selected_method,
            amount=order.total_amount,
            status='Completed',
            transaction_id=str(uuid.uuid4())
        )

        # Update order status
        order.status = "Processing"
        order.save()

        #  Show your existing success page
        # return render(request, 'order_success.html', {'order': order})
        return render(request, "payment_success.html", {"payment": payment})


    return render(request, "payment_page.html", {"order": order, "payment_methods": payment_methods})



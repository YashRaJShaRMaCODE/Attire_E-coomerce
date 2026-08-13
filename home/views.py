from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from home.models import (
    Address,
    CartItem,
    Category,
    Contact,
    Feedback,
    Order,
    OrderItem,
    Product,
)


def index(request):
    products = Product.objects.filter(is_active=True)[:6]
    categories = Category.objects.all()
    context = {"products": products, "categories": categories}
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def product_list(request):
    products = Product.objects.filter(is_active=True)
    category_slug = request.GET.get("category")
    query = request.GET.get("q")

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if query:
        products = products.filter(name__icontains=query)

    categories = Category.objects.all()
    return render(request, "product_list.html", {"products": products, "categories": categories})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "product_detail.html", {"product": product})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Contact.objects.create(name=name, email=email, message=message)
        messages.success(request, "Thanks for reaching out! We'll get back to you soon.")

    return render(request, "contact.html")


def feedback(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Feedback.objects.create(name=name, email=email, message=message)
        messages.success(request, "Thank you for your feedback!")

    return render(request, "feedback.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully. Welcome!")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("product")
    total_price = sum((item.total_price for item in cart_items), Decimal("0"))
    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect("cart")


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
        except ValueError:
            quantity = 1

        if quantity < 1:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("cart")


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("product")
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    total_price = sum((item.total_price for item in cart_items), Decimal("0"))
    addresses = Address.objects.filter(user=request.user)
    return render(request, "checkout.html", {"cart_items": cart_items, "total_price": total_price, "addresses": addresses})


@login_required
def place_order(request):
    if request.method != "POST":
        return redirect("checkout")

    cart_items = CartItem.objects.filter(user=request.user).select_related("product")
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    address_id = request.POST.get("address")
    address = Address.objects.filter(id=address_id, user=request.user).first() if address_id else None

    total_price = sum((item.total_price for item in cart_items), Decimal("0"))
    order = Order.objects.create(user=request.user, address=address, total_price=total_price)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
        )

    cart_items.delete()
    messages.success(request, "Your order has been placed successfully!")
    return redirect("order_success", order_id=order.id)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_success.html", {"order": order})


@login_required
def my_account(request):
    recent_orders = Order.objects.filter(user=request.user).order_by("-created_at")[:5]
    return render(request, "my_account.html", {"recent_orders": recent_orders})


@login_required
def profile_settings(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", "")
        user.email = request.POST.get("email", "")
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile_settings")

    return render(request, "profile_settings.html")


@login_required
def account_settings(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        user = authenticate(request, username=request.user.username, password=old_password)
        if user is None:
            messages.error(request, "Current password is incorrect.")
        elif new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
        elif not new_password1:
            messages.error(request, "New password cannot be empty.")
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully.")
        return redirect("account_settings")

    return render(request, "account_settings.html")


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_orders.html", {"orders": orders})


@login_required
def purchase_history(request):
    orders = Order.objects.filter(user=request.user, status="delivered").order_by("-created_at")
    return render(request, "purchase_history.html", {"orders": orders})


@login_required
def saved_addresses(request):
    if request.method == "POST":
        Address.objects.create(
            user=request.user,
            label=request.POST.get("label", "Home"),
            line1=request.POST.get("line1", ""),
            line2=request.POST.get("line2", ""),
            city=request.POST.get("city", ""),
            state=request.POST.get("state", ""),
            zip_code=request.POST.get("zip_code", ""),
        )
        messages.success(request, "Address saved.")
        return redirect("saved_addresses")

    addresses = Address.objects.filter(user=request.user)
    return render(request, "saved_addresses.html", {"addresses": addresses})


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, "Address removed.")
    return redirect("saved_addresses")


@login_required
def settings(request):
    return render(request, "settings.html")

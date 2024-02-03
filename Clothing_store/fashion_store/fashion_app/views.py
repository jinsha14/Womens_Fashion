from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, UserProfile, Cart, Order, OrderItem, Category
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import user_passes_test
import os


# Create your views here.


def index(request):
    return render(request, 'index.html')


def newhome(request):
    products = Product.objects.all()  # Fetch your products here
    return render(request, 'newhome.html', {'products': products})


def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        adduser = UserProfile(firstname=firstname, lastname=lastname, phone=phone, email=email,
                              username=username, password=password)

        auth_user = User(username=username, first_name=firstname, last_name=lastname, email=email)
        auth_user.set_password(password)
        auth_user.save()
        adduser.save()
        return redirect(user_login)

    return render(request, 'signup.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('newhome')
        else:
            return render(request, 'user_login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'user_login.html')


def account(request):
    logged_in_user = request.user

    if request.method == 'POST':

        logged_in_user.first_name = request.POST.get('firstname', '')
        logged_in_user.last_name = request.POST.get('lastname', '')
        logged_in_user.phone = request.POST.get('phone', '')
        logged_in_user.email = request.POST.get('email', '')
        logged_in_user.username = request.POST.get('username', '')
        new_password = request.POST.get('password', '')

        if new_password:
            logged_in_user.set_password(new_password)
        logged_in_user.save()
        messages.success(request, 'User details updated successfully!')
        return redirect('account')

    return render(request, 'account_view.html', {'user': logged_in_user})


def edit_profile(request):

    if not request.user.is_authenticated:
        return HttpResponse('User not authenticated')

    if request.method == 'POST':
        ed = request.user
        ed.first_name = request.POST.get('firstname', '')
        ed.last_name = request.POST.get('lastname', '')
        ed.phone = request.POST.get('phone', '')
        ed.username = request.POST.get('username', '')
        new_password = request.POST.get('password', '')

        if new_password:
            ed.set_password(new_password)

        ed.save()
        messages.success(request, 'User details updated successfully!')
        return redirect('newhome')

    return render(request, 'edit_profile.html', {'ed': request.user})


def womens(request):
    womens_products = Product.objects.filter(category__name="Womens Fashion")
    return render(request, 'womens.html', {'womens': womens_products})


def accessories(request):
    accessories = Product.objects.filter(category__name="Accessories")
    return render(request, 'accessories.html', {'accessories': accessories})


def brides(request):
    brides_products = Product.objects.filter(category__name="Brides Gown")
    return render(request, 'brides.html', {'brides': brides_products})


def lg_out(request):
    logout(request)
    return redirect('/')


def add_to_cart(request, product_id):
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    return redirect('cart')


def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.calculate_total() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def update_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_item = Cart.objects.get(user=request.user, product=product)
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, id=product_id)
        Cart.objects.filter(user=request.user, product=product).delete()

    return redirect('cart')


def checkout(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.calculate_total() for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price)
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity,
                                     price=cart_item.product.price)
            cart_item.delete()
        return redirect('order_confirmation')
    else:
        return render(request, 'checkout.html')


def order_confirmation(request):
    return render(request, 'order_confirmation.html')


def product_view(request):
    women_products = Product.objects.all()
    accessory_products = Product.objects.all()
    bride_products = Product.objects.all()

    all_products = list(women_products) + list(accessory_products) + list(bride_products)

    context = {
        'all_products': all_products
    }

    return render(request, 'product_view.html', context)


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        photo = request.FILES.get('photo')
        size = request.POST.get('size')
        quantity = request.POST.get('quantity')
        category_id = request.POST.get('category')

        if Category.objects.filter(pk=category_id).exists():
            category = Category.objects.get(pk=category_id)
            new_product = Product(name=name, price=price, photo=photo, size=size, quantity=quantity,
                                  category_id=category_id)
            new_product.save()
            return redirect('product_view')
        else:
            pass

    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product successfully deleted.')
        return redirect('product_view')

    return render(request, 'delete_product.html', {'product': product})


def update_product(request, product_id):
    pro = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            return HttpResponse('<script>alert("Name is required"); window.location="/update_product/' + str(
                product_id) + '";</script>')
        pro.name = name
        price = request.POST.get('price')
        if not price:
            return HttpResponse('<script>alert("Price is required"); window.location="/update_product/' + str(
                product_id) + '";</script>')
        pro.price = price
        if 'photo' in request.FILES:
            if pro.photo:
                os.remove(pro.photo.path)
            pro.photo = request.FILES.get('photo')
        pro.size = request.POST.get('size')
        pro.quantity = request.POST.get('quantity')
        pro.save()
        return HttpResponse('<script>alert("Successfully updated"); window.location="/product_view";</script>')

    return render(request, 'update_prod.html', {'upt': pro})


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

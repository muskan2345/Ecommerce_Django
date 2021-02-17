from django.shortcuts import render,redirect
from .models import Cart
from orders.models import Order
from mysite.models import Product, GuestEmail
from mysite.forms import LoginForm,GuestForm
from billing.models import BillingProfile

# def cart_create(user=None):
#     cart_obj=Cart.objects.create(user=None)
#     print('New Cart created')


def cart_home(request):
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    # products=cart_obj.products.all()
    # total=0
    # for x in products:
    #     total += x.price
    # print(total)
    # cart_obj.total=total
    # cart_obj.save()
    return render(request,"carts/home.html",{"cart": cart_obj})
def cart_update(request):
    print(request.POST)
    product_id=request.POST.get('product_id')
    if product_id is not None:
        # try:
        #     product_id=request.POST.get('product_id')
        # except Product.DoesNotExit:
        #     print("show message to user,product is gone?")
        #     return redirect("cart:home")
        #product_id=1
        product_obj=Product.objects.get(id=product_id)
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
    #cart_obj.products.add(product_obj)
    #return redirect(products_obj.get_absolute_url())
    return redirect("cart:home")

def checkout_home(request):
    cart_obj,cart_created=Cart.objects.new_or_get(request)
    order_obj=None
    if  cart_created or cart_obj.products.count()==0:
        return redirect("cart:home")
    else:
        order_obj,new_order_obj=Order.objects.get_or_create(cart=cart_obj,active=True)
    user=request.user
    billing_profile=None
    login_form=LoginForm()
    guest_form=GuestForm()
    guest_email_id=request.session.get('guest_email_id')
    if user.is_authenticated:
        billing_profile,billing_profile_created=BillingProfile.objects.get_or_create(user=user,email=user.email)
    elif guest_email_id is not None:
        guest_email_obj=GuestEmail.objects.get(id=guest_email_id)
        billing_profile,billing_guest_profile_created=BillingProfile.objects.get_or_create(user=user,email=guest_email_obj.email)
    else:
        pass
    if billing_profile is not None:
        order_qs=Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True)
        if order_qs.count()==1:
            order_obj=order_qs.first()
        else:
            # old_order_qs=Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
            # if old_order_qs.exists():
            #     old_order_qs=qs.update(active=False)
            order_obj= Order.objects.create(billing_profile=billing_profile,cart=cart_obj)

    context={
      "object":order_obj,
      "billing_profile":billing_profile,
      "login_form":login_form,
      "guest_form":guest_form

    }
    return render(request,"carts/checkout.html",context)

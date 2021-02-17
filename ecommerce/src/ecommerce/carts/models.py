from django.db import models
from django.conf import settings
from mysite.models import Product

from django.db.models.signals import pre_save,post_save,m2m_changed
# Create your models here.
User=settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self,request):
    #     cart_id=request.session.get("cart_id",None)
    #     qs=self.get_queryset().filter(id=cart_id)
    #     if qs.count()==1:
    #         new_obj=False
    #         print('cart ID exits')
    #         cart_obj=qs.first()
    #         if request.user.is_authenticated and cart_obj.user is None:
    #             cart_obj.user=request.user
    #             cart_obj.save()
    #     else:
    #         cart_obj=Cart.objects.new(user=request.user)
    #         new_obj=True
    #         request.session['cart_id']=cart_obj.id
    #     return cart_obj,new_obj
        if request.user.is_authenticated:
            qs = self.get_queryset().filter(user=request.user)

            if qs.count() == 1:
                cart_obj = qs.first()
                new_obj = False
                request.session["cart_items"] = cart_obj.products.count()
                request.session['cart_id'] = cart_obj.id
            else:
                cart_obj = Cart.objects.new(user=request.user)
                new_obj = True
                request.session['cart_id'] = cart_obj.id

            return cart_obj, new_obj
        else:
            cart_id = request.session.get("cart_id")
            qs = self.get_queryset().filter(id=cart_id)
            if qs.count() == 1:
                cart_obj = qs.first()
                new_obj = False
                if request.user.is_authenticated and cart_obj.user is None:
                    cart_obj.user = request.user
                    cart_obj.save()
            else:
                cart_obj = Cart.objects.new(user=request.user)
                new_obj = True
                request.session['cart_id'] = cart_obj.id
            return cart_obj, new_obj


    def new(self,user=None):
         print(user)
         user_obj=None
         if user is not None:
             if user.is_authenticated:
                 user_obj=user
         return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product,blank=True)
    updated=models.DateTimeField(auto_now=True)
    subtotal=models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    total=models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    objects=CartManager()
    def __int__(self):
        return (self.id)

#@signals.receiver(signals.m2m_changed, sender=Cart.m2m_relationship.through)
def m2m_changed_cart_receiver(sender,instance,action,*args,**kwargs):
    #print(action)
    if action =='post_add' or action=='post_remove' or action=='post_clear':
    #print(instance.)
        products=instance.products.all()
        total=0
        for x in products:
            total+=x.price
        print(total)
        if instance.subtotal!=total:

            instance.subtotal=total
            instance.save()
m2m_changed.connect(m2m_changed_cart_receiver,sender=Cart.products.through)





def pre_save_cart_receiver(sender,instance,*args,**kwargs):
    if instance.subtotal>0:
        instance.total=instance.subtotal
    else:
        instance.total=0.0
    #instance.total=instance.subtotal
pre_save.connect(pre_save_cart_receiver,sender=Cart)

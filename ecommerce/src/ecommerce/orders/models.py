from django.db import models
from carts.models import Cart
from django.db.models.signals import pre_save,post_save
import decimal
from ecommerce.utils import unique_order_id_generator
from billing.models import BillingProfile
# database store  value in left and display value in right
ORDER_STATUS_CHOICES=(('created','Created'),
('paid','Paid'),('shipped','Shipped'),('refunded','Refunded'),)

# random generate order_id unique


class Order(models.Model):
    billing_profile=models.ForeignKey(BillingProfile,on_delete=models.CASCADE,blank=True,null=True)
    order_id=models.CharField(max_length=120,blank=True)

    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    status=models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    shipping_total=models.DecimalField(default=5.99,max_digits=100,decimal_places=2)
    #shipping_total price based on the addre4ss
    # assume thay u ship product
    total=models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.order_id
    def update_total(self):
        cart_total=self.cart.total
        shipping_total=self.shipping_total
        new_total=decimal.Decimal(cart_total) + decimal.Decimal(shipping_total)
        self.total=new_total
        self.save()
        return new_total

# generate order id
def pre_save_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_id_generator(instance)
    qs=Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)    
pre_save.connect(pre_save_create_order_id,sender=Order)


def post_save_cart_total(sender,instance,*args,**kwargs):
    cart_obj=instance
    cart_total=cart_obj.total
    cart_id=cart_obj.id
    qs=Order.objects.filter(cart_id=cart_id)
    if qs.exists()==1:
        order_obj=qs.first()
        order_obj.update_total()
post_save.connect(post_save_cart_total,sender=Cart)


def post_save_order(sender,instance,created,*args,**kwargs):
    print('running')
    if created:
        print('updating')
        instance.update_total()
post_save.connect(post_save_order,sender=Order)

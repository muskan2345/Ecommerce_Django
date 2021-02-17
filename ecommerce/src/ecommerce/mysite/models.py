import random
from django.db import models
from django.urls import reverse

# def upload_image_path(instance,filename):
#     print(instance)
#     print(filename)
#     new_filename=random.randint(1,3910209312)

# Create your models here.
class ProductManager(models.Manager):
    def get_by_id(self,id):
        qs=self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()
        return None


class Product(models.Model):
    title=models.CharField(max_length=120)
    slug=models.SlugField(blank=True,unique=True)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=20,default=True)
    image=models.ImageField(upload_to='mysite/',null=True,blank=True)
    objects=ProductManager()
    active=models.BooleanField(default=True)

    objects=ProductManager()
    def get_absolute_url(self):
        # return "/mysite/{slug}/".format(slug=self.slug)
         return reverse('detail', kwargs={'slug': self.slug, 'id':self.id})
    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title

class GuestEmail(models.Model):
    email=models.EmailField()
    active=models.BooleanField(default=True)
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email






# def prodeuct_pre_save_reciever(sender,instance,*args,**kwargs):
#     if not instance.slug:
#         instance.slug='abc'
# pre_save.connect(product_pre_save,sender=Product)

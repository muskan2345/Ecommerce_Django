from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404
from django.views.generic import ListView,DetailView
from django.shortcuts import render,redirect
from .forms import ContactForm,LoginForm,RegisterForm,GuestForm
from django.contrib.auth import authenticate ,login,get_user_model,logout
from.models import Product
from carts.models import Cart
from django.utils.http import is_safe_url
from .models import GuestEmail
# Create your views here.
class ProductListView(ListView):
    queryset=Product.objects.all()
    template_name='mysite/list.html'
    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.all()


def product_list_view(request):
    queryset=Product.objects.all()
    context={'object_list':queryset}
    return render(request,'mysite/list.html',context)



class ProductDetailSlugView(DetailView):
    queryset=Product.objects.all()
    template_name='mysite/detail.html'
    def get_context_data(self,*args,**kwargs):
        context=super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        cart_obj,new_obj=Cart.objects.new_or_get(self.request)
        context['cart']=cart_obj
        return context

    def get_object(self,*args,**kwargs):
        request=self.request
        slug=self.kwargs.get('slug')
        try:
            instance=Product.objects.get(slug=slug)
        # except Product.DoesNotExit:
        #     raise Http404('Not found')
        except Product.MultipleObjectsReturned:
            qs=Product.objects.filter(slug=slug,active=True)
            instance=qs.first()
        except:
            raise Http404('uhhh')
        return instance

        # instance=get_object_or_404(Product,slug=slug,active=True)
        # return instance



class ProductDetailView(DetailView):
    #queryset=Product.objects.all()
    template_name='mysite/detail.html'
    def get_context_data(self,*args,**kwargs):

        context=super(ProductDetailView,self).get_context_data(*args,**kwargs)
        return context



    def get_object(self,*args,**kwargs):
        request=self.request
        pk=self.kwargs.get('pk')
        instance=Product.objects.get_by_id(pk)

        if instance is None:
            raise Http404('product doesnt exit')
        return instance

def product_detail_view(request,pk=None,*args,**kwargs):

     qs=Product.objects.filter(id=pk)
     if qs.exits() and qs.count()==1:
         instance=qs.first()
     else:
         raise Http404('product doesnt exit')
     context={
         'object':instance
     }
     return render(request,"mysite/detail.html",context)




def home_page(request):
    context={
      "title":"hello World",
      "content":"Welcome to homepage"
    }
    return render(request,"home_page.html",context)
def about_page(request):
    context={
    "title":"hello World",
     "content":"Welcome to aboutpage"
    }
    return render(request,"home_page.html",context)
def contact_page(request):
    contact_form=ContactForm(request.POST)
    context={
    "title":"hello World",
     "content":"Welcome to contact_page",
     "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        # print(request.POST)
        # print(request.POST.get('fullname'))
        # print(request.POST.get('email'))
    return render(request,"contact/view.html",context)
def guest_register_view(request):
    form=GuestForm(request.POST or None)
    #print(request.user.is_authenticated())
    context={

       "form":form
    }
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path= next_ or next_post or None
    if form.is_valid():
        email=form.cleaned_data.get("email")
        new_guest_email=GuestEmail.objects.create(email=email)
        request.session['guest_email_id']=new_guest_email.id
        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("register")
                #return redirect("/"))

    return redirect("register")

def logout_page(request):
    logout(request)
    return redirect("home_page")






def login_page(request):
    form=LoginForm(request.POST)
    #print(request.user.is_authenticated())
    context={

       "form":form
    }
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path= next_ or next_post or None
    if form.is_valid():
        print(form.cleaned_data)
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
                #return redirect("/")
        else:
            print("Error")

    return render(request,"mysite/login.html",context)
User=get_user_model()
def register_page(request):
    form=RegisterForm(request.POST)
    context={

       "form":form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username=form.cleaned_data.get("username")
        email=form.cleaned_data.get("email")
        password=form.cleaned_data.get("password")
        new_user=User.objects.create_user(username,email,password)
        print(new_user)

    return render(request,"auth/register.html",context)

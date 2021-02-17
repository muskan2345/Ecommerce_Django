from django.http import HttpResponse
from django.shortcuts import render


from .forms import ContactForm

def contact_page(request):
    contact_form=ContactForm(request.POST or NONE)
    context={
    "title":"hello World",
     "content":"Welcome to contact_page",
     "form": contact_form
    }
    if request.method=='POST':
        print(request.POST)
        print(request.POST.get('first_name'))
        print(request.POST.get('last_name'))
        print(request.POST.get('email'))
    return render(request,"contact/view.html",context)

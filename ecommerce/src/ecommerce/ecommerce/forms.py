from django import forms


class ContactForm(forms.Form):
    fullname=forms.Charfield()
    email=forms.EmailField()
    content=forms.CharField()

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=10)
    email = forms.EmailField()
    desc = forms.CharField(max_length=1000, widget=forms.Textarea)
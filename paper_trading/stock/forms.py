from django import forms

class PostForm(forms.Form):
    company = forms.CharField(max_length=500)
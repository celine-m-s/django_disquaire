from django.forms import ModelForm, TextInput, EmailInput
from .models import Contact

from django.forms.utils import ErrorList
class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email"]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'})
        }




# First solution to be explained:
# from django import forms
#
# class ContactForm(forms.Form):
#     name = forms.CharField(
#         label='Nom',
#         max_length=100,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True
#         )
#     email = forms.EmailField(
#         label='Email',
#         widget=forms.EmailInput(attrs={'class': 'form-control'}),
#         required=True)

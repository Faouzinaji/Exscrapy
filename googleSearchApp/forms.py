from django import forms
from captcha.fields import CaptchaField
class MyForm(forms.Form):
    # You can add other form fields here!
    captcha = CaptchaField()
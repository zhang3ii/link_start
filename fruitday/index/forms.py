from django import forms
from .models import *


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['uphone','upwd']
        labels = {
            'uphone':'电话',
            'upwd':'登录密码',
        }

        widgets = {
            'uphone':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'upwd':forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':'请输入密码'
            }),
        }
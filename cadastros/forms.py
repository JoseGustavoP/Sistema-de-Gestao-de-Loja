from django import forms
from .models import Produto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms



class XMLUploadForm(forms.Form):
    xml_file = forms.FileField(label='Selecione um arquivo XML')

class MeuFormularioDeLogin(forms.Form):
    username = forms.CharField(label='Usuário:', max_length=100)
    password = forms.CharField(label='Senha:', widget=forms.PasswordInput())

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    is_staff = forms.BooleanField(required=False, help_text='Marque para criar um administrador.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'tipo',
            'codigo_barras',
            'preco_compra',
            'porcentagem_lucro',
            'preco_venda',   # agora aparece no form
            'imagem'
        ]

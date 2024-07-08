from django import forms
from .models import Persona, Mancuerna, CarritoItem, Pedido, DetallePedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PersonaForm(forms.ModelForm):
    rut = forms.CharField(help_text="Ingrese rut sin puntos y con guión")
    fnacto = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de Nacimiento")

    class Meta:
        model = Persona
        fields = ['rut', 'nombre', 'apellido', 'foto', 'fnacto', 'correo', 'sexo']

class UpdatePersonaForm(forms.ModelForm):
    fnacto = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de Nacimiento")

    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'foto', 'fnacto', 'correo', 'sexo']

class MancuernaForm(forms.ModelForm):
    class Meta:
        model = Mancuerna
        fields = '__all__'

class CarritoItemForm(forms.ModelForm):
    class Meta:
        model = CarritoItem
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion_entrega']

    direccion_entrega = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingresa la dirección completa'
    }))

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
        
class PagoForm(forms.Form):
    numero_tarjeta = forms.CharField(max_length=16, widget=forms.TextInput(attrs={
        'placeholder': 'Número de tarjeta'
    }))
    mes_vencimiento = forms.CharField(max_length=2, widget=forms.TextInput(attrs={
        'placeholder': 'MM'
    }))
    ano_vencimiento = forms.CharField(max_length=2, widget=forms.TextInput(attrs={
        'placeholder': 'YY'
    }))
    cvv = forms.CharField(max_length=3, widget=forms.TextInput(attrs={
        'placeholder': 'CVV'
    }))

class UpdatePedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
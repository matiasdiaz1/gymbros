from django import forms
from .models import Persona, Mancuerna, CarritoItem, Pedido, DetallePedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'

class UpdatePersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'

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
    rut_dueno_tarjeta = forms.CharField(max_length=12, widget=forms.TextInput(attrs={
        'placeholder': 'RUT dueño de tarjeta'
    }))
    
    
class UpdatePedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
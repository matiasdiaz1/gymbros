from django import forms
from .models import Persona, Mancuerna, CarritoItem, Pedido, DetallePedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    REGION_CHOICES = [
        ('', 'Selecciona una región'),
        ('BioBio', 'Región del Biobío'),
        ('Santiago', 'Región Metropolitana de Santiago'),
    ]

    COMUNA_CHOICES = [
        ('', 'Selecciona una comuna'),
        ('Concepcion', 'Concepción'),
        ('Talcahuano', 'Talcahuano'),
        ('Hualpén', 'Hualpén'),
        ('SanPedro', 'San Pedro de la Paz'),
        ('Coronel', 'Coronel'),
        ('Lota', 'Lota'),
        ('Chiguayante', 'Chiguayante'),
        ('Hualqui', 'Hualqui'),
        ('Penco', 'Penco'),
        ('Tome', 'Tomé'),
        ('SantaJuana', 'Santa Juana'),
        ('SantiagoCentro', 'Santiago Centro'),
        ('LasCondes', 'Las Condes'),
        ('Providencia', 'Providencia'),
        ('Ñuñoa', 'Ñuñoa'),
        ('LaFlorida', 'La Florida'),
        ('PuenteAlto', 'Puente Alto'),
        ('Maipu', 'Maipú'),
        ('SanBernardo', 'San Bernardo'),
        ('LaCisterna', 'La Cisterna'),
        ('LaGranja', 'La Granja'),
        ('LoEspejo', 'Lo Espejo'),
        ('PedroAguirreCerda', 'Pedro Aguirre Cerda'),
        ('SanMiguel', 'San Miguel'),
        ('Independencia', 'Independencia'),
        ('Recoleta', 'Recoleta'),
        ('Quilicura', 'Quilicura'),
        ('Renca', 'Renca'),
        ('Conchali', 'Conchalí'),
        ('Huechuraba', 'Huechuraba'),
        ('QuintaNormal', 'Quinta Normal'),
        ('LoPrado', 'Lo Prado'),
        ('CerroNavia', 'Cerro Navia'),
        ('Pudahuel', 'Pudahuel'),
        ('EstacionCentral', 'Estación Central'),
        ('LoBarnechea', 'Lo Barnechea'),
        ('Vitacura', 'Vitacura'),
        ('LaReina', 'La Reina'),
        ('Peñalolen', 'Peñalolén'),
        ('Macul', 'Macul'),
        ('SanJoaquin', 'San Joaquín'),
        ('LaPintana', 'La Pintana'),
        ('ElBosque', 'El Bosque'),
        ('SanRamon', 'San Ramón'),
    ]

    region = forms.ChoiceField(choices=REGION_CHOICES, widget=forms.Select(attrs={
        'placeholder': 'Selecciona una región',
        'onchange': 'habilitar_comuna()'
    }), label="Región")

    comuna = forms.ChoiceField(choices=COMUNA_CHOICES, widget=forms.Select(attrs={
        'placeholder': 'Selecciona una comuna',
        'disabled': 'disabled'
    }), label="Comuna")

    calle = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingresa el nombre de la calle y número'
    }), label="Calle")

    numero = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingresa el número de la calle'
    }), label="Número")

    dpto_casa_oficina = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Ejem. Casa 3, Dpto 101.'
    }), label="Dpto. / Casa / Oficina / Condominio (opcional)")

    class Meta:
        model = Pedido
        fields = ['region', 'comuna', 'calle', 'numero', 'dpto_casa_oficina']

    direccion_entrega = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingresa la dirección completa'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].widget.attrs.update({'onchange': 'habilitar_comuna()'})

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
        
class PagoForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Nombre'
    }))
    
    numero_tarjeta = forms.CharField(max_length=16, widget=forms.TextInput(attrs={
        'placeholder': 'Número de tarjeta'
    }))
    

    MESES = [(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)]
    

    AÑOS = [(str(i)[-2:], str(i)) for i in range(2024, 2055)]
    
    mes_vencimiento = forms.ChoiceField(choices=MESES, widget=forms.Select(attrs={
        'placeholder': 'MM'
    }))
    
    año_vencimiento = forms.ChoiceField(choices=AÑOS, widget=forms.Select(attrs={
        'placeholder': 'YY'
    }))
    
    cvv = forms.CharField(max_length=3, widget=forms.TextInput(attrs={
        'placeholder': 'CVV'
    }))

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not nombre.isalpha():
            raise ValidationError('El nombre solo puede contener letras.')
        return nombre

    def clean_numero_tarjeta(self):
        numero_tarjeta = self.cleaned_data['numero_tarjeta']
        if not numero_tarjeta.isdigit() or len(numero_tarjeta) != 16:
            raise ValidationError('El número de tarjeta debe contener 16 dígitos.')
        return numero_tarjeta

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not cvv.isdigit() or len(cvv) != 3:
            raise ValidationError('El CVV debe contener 3 dígitos.')
        return cvv
class UpdatePedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
        
        
        
        

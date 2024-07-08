from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date

TIPO_SEXO = (
    ("F", "FEMENINO"),
    ("M", "MASCULINO"),
    ("O", "OTRO")
)

class Persona(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    fnacto = models.DateField(default=date.today)
    correo = models.EmailField(verbose_name='E-mail')
    sexo = models.CharField(max_length=1, choices=TIPO_SEXO)
    foto = models.ImageField(upload_to='personas', null=True)
    
    def __str__(self):
        return f"{self.rut} -  {self.nombre} {self.apellido}"

class Mancuerna(models.Model):
    id = models.AutoField(primary_key=True)
    peso = models.IntegerField(validators=[MinValueValidator(1)])
    precio = models.IntegerField(validators=[MinValueValidator(1)])
    stock = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"Mancuerna de {self.peso} kg - ${self.precio} (Stock: {self.stock})"

class CarritoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mancuerna = models.ForeignKey(Mancuerna, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.mancuerna.peso}kg mancuerna"

    @property
    def total_price(self):
        return self.mancuerna.precio * self.quantity

class Pedido(models.Model):
    ESTADO_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    
    region = models.CharField(max_length=100, default='Región Desconocida')
    comuna = models.CharField(max_length=100, default='Comuna Desconocida')
    calle = models.CharField(max_length=100, default='Calle Desconocida')
    numero = models.CharField(max_length=10, default='0')
    dpto_casa_oficina = models.CharField(max_length=100, blank=True, null=True, default='')

    def __str__(self):
        return f"Pedido {self.id} - {self.user.username}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    mancuerna = models.ForeignKey(Mancuerna, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"{self.cantidad} x {self.mancuerna.peso}kg en Pedido {self.pedido.id}"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario